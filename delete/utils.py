from functools import cmp_to_key
from common.mongodb_models import (
    AcquisitionCapabilityRevision,
    AcquisitionRevision,
    CatalogueRevision,
    CatalogueEntryRevision,
    CatalogueDataSubsetRevision,
    ComputationCapabilityRevision,
    ComputationRevision,
    CurrentAcquisition,
    CurrentAcquisitionCapability,
    CurrentCatalogue,
    CurrentCatalogueEntry,
    CurrentCatalogueDataSubset,
    CurrentComputation,
    CurrentComputationCapability,
    CurrentDataCollection,
    CurrentDataCollectionInteractionMethod,
    CurrentIndividual,
    CurrentInstrument,
    CurrentOperation,
    CurrentOrganisation,
    CurrentPlatform,
    CurrentProcess,
    CurrentProject,
    DataCollectionInteractionMethodRevision,
    DataCollectionRevision,
    IndividualRevision,
    InstrumentRevision,
    OperationRevision,
    PlatformRevision,
    ProcessRevision,
    ProjectRevision,
    OriginalMetadataXml,
)
from common.helpers import (
    create_resource_url,
    create_catalogue_related_resource_url,
)
from bson import ObjectId

# Getters for resources referencing "parties" - Organisations and/or Individuals
def _get_projects_referencing_party_url(party_url):
    return CurrentProject.find({
        'relatedParty.ResponsiblePartyInfo.party.@xlink:href': party_url
    })

def _get_platforms_referencing_party_url(party_url):
    return CurrentPlatform.find({
        'relatedParty.ResponsiblePartyInfo.party.@xlink:href': party_url
    })

def _get_operations_referencing_party_url(party_url):
    return CurrentOperation.find({
        'relatedParty.ResponsiblePartyInfo.party.@xlink:href': party_url
    })

def _get_instruments_referencing_party_url(party_url):
    return CurrentInstrument.find({
        'relatedParty.ResponsiblePartyInfo.party.@xlink:href': party_url
    })

def _get_data_collections_referencing_party_url(party_url):
    return CurrentDataCollection.find({
        'relatedParty.ResponsiblePartyInfo.party.@xlink:href': party_url
    })

def sort_resource_list(resource_list):
    def get_weight_of_resource_type(resource_type):
        if resource_type == 'organisation':
            return 1
        elif resource_type == 'individual':
            return 2
        elif resource_type == 'project':
            return 3
        elif resource_type == 'platform':
            return 4
        elif resource_type == 'operation':
            return 5
        elif resource_type == 'instrument':
            return 6
        elif resource_type == 'acquisitionCapabilities':
            return 7
        elif resource_type == 'acquisition':
            return 8
        elif resource_type == 'computationCapabilities':
            return 9
        elif resource_type == 'computation':
            return 10
        elif resource_type == 'process':
            return 11
        elif resource_type == 'collection':
            return 12
        elif resource_type == 'catalogue':
            return 13
        elif resource_type == 'catalogue entry':
            return 14
        elif resource_type == 'catalogue data subset':
            return 15
        return 15
    def compare_resource_type_weight(item1, item2):
        item1_weight = get_weight_of_resource_type(item1[1])
        item2_weight = get_weight_of_resource_type(item2[1])
        if item1_weight < item2_weight:
            return -1
        elif item1_weight > item2_weight:
            return 1
        else:
            return 0
    resource_list.sort(key=cmp_to_key(compare_resource_type_weight))

    return resource_list

# Gets all resources referencing a given resource id. This changes depending on the type of
# resource.
def get_data_collection_related_resources_linked_through_resource_id(resource_id, resource_type, resource_mongodb_model):
    individuals = []
    projects = []
    platforms = []
    instruments = []
    operations = []
    acquisition_capability_sets = []
    acquisitions = []
    computation_capability_sets = []
    computations = []
    processes = []
    data_collections = []

    linked_resources = []
    resource = resource_mongodb_model.find_one({
        '_id': ObjectId(resource_id)
    })
    resource_pithia_identifier = resource['identifier']['PITHIA_Identifier']
    resource_url = create_resource_url(resource_type, resource_pithia_identifier['namespace'], resource_pithia_identifier['localID'])
    if resource_mongodb_model == CurrentOrganisation:
        # Referenced by: Individual, Project, Platform?, Instrument?, Data Collection
        # Individual references it via the organisation prop.
        # Project references it via the relatedParty.party prop.
        # Data Collection references it via the relatedParty.party
        # prop.
        # Platform and instrument have the same props (relatedParty.party)
        # but do not have arrows pointing to Organisation and Individual.
        # Maybe these are mistakes?
        individuals = CurrentIndividual.find({
            'organisation.@xlink:href': resource_url
        })
        projects = _get_projects_referencing_party_url(resource_url)
        platforms = _get_platforms_referencing_party_url(resource_url)
        operations = _get_operations_referencing_party_url(resource_url)
        instruments = _get_instruments_referencing_party_url(resource_url)
        data_collections = _get_data_collections_referencing_party_url(resource_url)
    elif resource_mongodb_model == CurrentIndividual:
        # Referenced by: Project, Platform?, Instrument?, Data Collection
        # Project references it via the relatedParty.party prop.
        # Data Collection references it via the relatedParty.party
        # prop.
        # Platform and instrument have the same props (relatedParty.party)
        # but do not have arrows pointing to Organisation and Individual.
        # Maybe these are mistakes?
        projects = _get_projects_referencing_party_url(resource_url)
        platforms = _get_platforms_referencing_party_url(resource_url)
        operations = _get_operations_referencing_party_url(resource_url)
        instruments = _get_instruments_referencing_party_url(resource_url)
        data_collections = _get_data_collections_referencing_party_url(resource_url)
    elif resource_mongodb_model == CurrentProject:
        # Referenced by: Data Collection
        # Data Collection references it via the project prop.
        data_collections = CurrentDataCollection.find({
            'project.@xlink:href': resource_url
        })
    elif resource_mongodb_model == CurrentPlatform:
        # Referenced by: Operation, other Platforms
        # Operations references it via the platform.@xlink:href prop.
        # Acquisition references it via the platform prop.
        operations = CurrentOperation.find({
            'platform.@xlink:href': resource_url
        })
        platforms = CurrentPlatform.find({
            'childPlatform.@xlink:href': resource_url
        })

    # Operations don't seem to be referenced by any other resource.

    elif resource_mongodb_model == CurrentInstrument:
        # Get the operational mode IDs of the Instrument
        # so Acquisition Capabilities just referencing the
        # Instrument's operational mode IDs can also be
        # deleted.
        operational_mode_urls = []
        if 'operationalMode' in resource:
            instrument_operational_modes = resource['operationalMode']
            for om in instrument_operational_modes:
                om_id = om['InstrumentOperationalMode']['id']
                operational_mode_urls.append(f'{resource_url}#{om_id}')

        # Referenced by: Acquisition (from instrument prop)
        acquisitions = CurrentAcquisition.find({
            'instrument.@xlink:href': resource_url
        })
        # Referenced by: AcquisitionCapability (from
        # instrumentModePair.InstrumentOperationalModePair.instrument prop and
        # instrumentModePair.InstrumentOperationalModePair.mode prop)
        acquisition_capability_sets = CurrentAcquisitionCapability.find({
            '$or': [
                {
                    'instrumentModePair.InstrumentOperationalModePair.instrument.@xlink:href': resource_url
                },
                {
                    'instrumentModePair.InstrumentOperationalModePair.mode.@xlink:href': resource_url
                },
                {
                    'instrumentModePair.InstrumentOperationalModePair.instrument.@xlink:href': {
                        '$in': operational_mode_urls
                    }
                },
                {
                    'instrumentModePair.InstrumentOperationalModePair.mode.@xlink:href': {
                        '$in': operational_mode_urls
                    }
                },
            ]
        })
    elif resource_mongodb_model == CurrentAcquisitionCapability:
        # AcquisitionCapability is referenced by Acquisition via
        # the acquisitionCapabilities prop.
        acquisitions = CurrentAcquisition.find({
            'capabilityLinks.capabilityLink.acquisitionCapabilities.@xlink:href': resource_url
        })
    elif resource_mongodb_model == CurrentAcquisition:
        # Acquisition is referenced by Process via
        # the acquisitionComponent prop.
        processes = CurrentProcess.find({
            'acquisitionComponent.@xlink:href': resource_url
        })
    elif resource_mongodb_model == CurrentComputationCapability:
        # ComputationCapability is referenced by Computation via the computationCapabilities
        # prop.
        # ComputationCapabilities can reference other ComputationCapabilities via the
        # childComputation prop.
        computation_capability_sets = CurrentComputationCapability.find({
            'childComputation.@xlink:href': resource_url
        })
        computations = CurrentComputation.find({
            'capabilityLinks.capabilityLink.computationCapabilities.@xlink:href': resource_url
        })
    elif resource_mongodb_model == CurrentComputation:
        # Referenced by Process via the computationComponent.
        processes = CurrentProcess.find({
            'computationComponent.@xlink:href': resource_url
        })
    elif resource_mongodb_model == CurrentProcess:
        # Referenced by Data Collection via the om:procedure
        # prop.
        data_collections = CurrentDataCollection.find({
            'om:procedure.@xlink:href': resource_url
        })
    # Data Collection is not included as no other resources
    # (including other data collections) reference this.
    individuals = list(individuals)
    for i in range(len(individuals)):
        individuals[i] = (individuals[i], 'individual', CurrentIndividual, IndividualRevision)
        linked_resources.extend(get_data_collection_related_resources_linked_through_resource_id(str(individuals[i][0]['_id']), 'individual', individuals[i][2]))
    projects = list(projects)
    for i in range(len(projects)):
        projects[i] = (projects[i], 'project', CurrentProject, ProjectRevision)
        linked_resources.extend(get_data_collection_related_resources_linked_through_resource_id(str(projects[i][0]['_id']), 'project', projects[i][2]))
    platforms = list(platforms)
    for i in range(len(platforms)):
        platforms[i] = (platforms[i], 'platform', CurrentPlatform, PlatformRevision)
        linked_resources.extend(get_data_collection_related_resources_linked_through_resource_id(str(platforms[i][0]['_id']), 'platform', platforms[i][2]))
    operations = list(operations)
    for i in range(len(operations)):
        operations[i] = (operations[i], 'operation', CurrentOperation, OperationRevision)
        linked_resources.extend(get_data_collection_related_resources_linked_through_resource_id(str(operations[i][0]['_id']), 'operation', operations[i][2]))
    instruments = list(instruments)
    for i in range(len(instruments)):
        instruments[i] = (instruments[i], 'instrument', CurrentInstrument, InstrumentRevision)
        linked_resources.extend(get_data_collection_related_resources_linked_through_resource_id(str(instruments[i][0]['_id']), 'instrument', instruments[i][2]))
    acquisition_capability_sets = list(acquisition_capability_sets)
    for i in range(len(acquisition_capability_sets)):
        acquisition_capability_sets[i] = (acquisition_capability_sets[i], 'acquisitionCapabilities', CurrentAcquisitionCapability, AcquisitionCapabilityRevision)
        linked_resources.extend(get_data_collection_related_resources_linked_through_resource_id(str(acquisition_capability_sets[i][0]['_id']), 'acquisitionCapabilities', acquisition_capability_sets[i][2]))
    acquisitions = list(acquisitions)
    for i in range(len(acquisitions)):
        acquisitions[i] = (acquisitions[i], 'acquisition', CurrentAcquisition, AcquisitionRevision)
        linked_resources.extend(get_data_collection_related_resources_linked_through_resource_id(str(acquisitions[i][0]['_id']), 'acquisition', acquisitions[i][2]))
    computation_capability_sets = list(computation_capability_sets)
    for i in range(len(computation_capability_sets)):
        computation_capability_sets[i] = (computation_capability_sets[i], 'computationCapabilities', CurrentComputationCapability, ComputationCapabilityRevision)
        linked_resources.extend(get_data_collection_related_resources_linked_through_resource_id(str(computation_capability_sets[i][0]['_id']), 'computationCapabilities', computation_capability_sets[i][2]))
    computations = list(computations)
    for i in range(len(computations)):
        computations[i] = (computations[i], 'computation', CurrentComputation, ComputationRevision)
        linked_resources.extend(get_data_collection_related_resources_linked_through_resource_id(str(computations[i][0]['_id']), 'computation', computations[i][2]))
    processes = list(processes)
    for i in range(len(processes)):
        processes[i] = (processes[i], 'process', CurrentProcess, ProcessRevision)
        linked_resources.extend(get_data_collection_related_resources_linked_through_resource_id(str(processes[i][0]['_id']), 'process', processes[i][2]))
    data_collections = list(data_collections)
    for i in range(len(data_collections)):
        data_collections[i] = (data_collections[i], 'collection', CurrentDataCollection, DataCollectionRevision)
    linked_resources.extend(individuals)
    linked_resources.extend(projects)
    linked_resources.extend(platforms)
    linked_resources.extend(operations)
    linked_resources.extend(instruments)
    linked_resources.extend(acquisition_capability_sets)
    linked_resources.extend(acquisitions)
    linked_resources.extend(computation_capability_sets)
    linked_resources.extend(computations)
    linked_resources.extend(processes)
    linked_resources.extend(data_collections)
    # Following line ensures that each dict in the linked_resources list is unique
    linked_resources = list({ str(v[0]['_id']):v for v in linked_resources }.values())

    return linked_resources

# Catalogue deletion

def get_catalogue_for_catalogue_entry(catalogue_entry):
    catalogue_identifier_xlink_href = catalogue_entry['catalogueIdentifier']['@xlink:href']
    catalogue_localid = catalogue_identifier_xlink_href.split('/')[-1]
    return CurrentCatalogue.find_one({
        'identifier.PITHIA_Identifier.localID': catalogue_localid
    })

def get_catalogue_for_catalogue_data_subset(catalogue_data_subset):
    catalogue_entry_identifier_xlink_href = catalogue_data_subset['entryIdentifier']['@xlink:href']
    catalogue_entry_localid = catalogue_entry_identifier_xlink_href.split('/')[-1]
    catalogue_entry = CurrentCatalogueEntry.find_one({
        'identifier.PITHIA_Identifier.localID': catalogue_entry_localid
    })
    return get_catalogue_for_catalogue_entry(catalogue_entry)

def get_catalogue_related_resources_linked_through_resource_id(resource_id, resource_mongodb_model, event=None):
    catalogues = []
    catalogue_entries = []
    catalogue_data_subsets = []

    linked_resources = []
    resource = resource_mongodb_model.find_one({
        '_id': ObjectId(resource_id)
    })
    resource_pithia_identifier = resource['identifier']['PITHIA_Identifier']
    resource_url = None
    if resource_mongodb_model == CurrentDataCollection:
        resource_url = create_resource_url('collection', resource_pithia_identifier['namespace'], resource_pithia_identifier['localID'])
    else:
        if event is None:
            catalogue = None
            if resource_mongodb_model == CurrentCatalogue:
                catalogue = resource
            elif resource_mongodb_model == CurrentCatalogueEntry:
                catalogue = get_catalogue_for_catalogue_entry(resource)
            elif resource_mongodb_model == CurrentCatalogueDataSubset:
                catalogue = get_catalogue_for_catalogue_data_subset(resource)
            event = catalogue['name']

        resource_url = create_catalogue_related_resource_url(resource_pithia_identifier['namespace'], event, resource_pithia_identifier['localID'])

    if resource_mongodb_model == CurrentDataCollection:
        # Referenced by Catalogue Data Subsets
        catalogue_data_subsets = CurrentCatalogueDataSubset.find({
            'dataCollection.@xlink:href': resource_url
        })
    if resource_mongodb_model == CurrentCatalogue:
        # Referenced by Catalogue Entries
        catalogue_entries = CurrentCatalogueEntry.find({
            'catalogueIdentifier.@xlink:href': resource_url
        })
    elif resource_mongodb_model == CurrentCatalogueEntry:
        # Referenced by Catalogue Data Subsets
        catalogue_data_subsets = CurrentCatalogueDataSubset.find({
            'entryIdentifier.@xlink:href': resource_url
        })
    # Catalogue Data Subsets are not included as they
    # are not referenced by any other resource type.
    catalogues = list(catalogues)
    for i in range(len(catalogues)):
        catalogues[i] = (catalogues[i], 'catalogue', CurrentCatalogue, CatalogueRevision)
        linked_resources.extend(get_catalogue_related_resources_linked_through_resource_id(str(catalogues[i][0]['_id']), catalogues[i][2], event=event))
    catalogue_entries = list(catalogue_entries)
    for i in range(len(catalogue_entries)):
        catalogue_entries[i] = (catalogue_entries[i], 'catalogue entry', CurrentCatalogueEntry, CatalogueEntryRevision)
        linked_resources.extend(get_catalogue_related_resources_linked_through_resource_id(str(catalogue_entries[i][0]['_id']), catalogue_entries[i][2], event=event))
    catalogue_data_subsets = list(catalogue_data_subsets)
    for i in range(len(catalogue_data_subsets)):
        catalogue_data_subsets[i] = (catalogue_data_subsets[i], 'catalogue data subset', CurrentCatalogueDataSubset, CatalogueDataSubsetRevision)
        linked_resources.extend(get_catalogue_related_resources_linked_through_resource_id(str(catalogue_data_subsets[i][0]['_id']), catalogue_data_subsets[i][2], event=event))
    linked_resources.extend(catalogues)
    linked_resources.extend(catalogue_entries)
    linked_resources.extend(catalogue_data_subsets)
    # Following line ensures that each dict in the linked_resources list is unique
    linked_resources = list({ str(v[0]['_id']):v for v in linked_resources }.values())

    return linked_resources

def delete_current_versions_and_revisions_of_data_collection_interaction_methods(data_collection_id, session=None):
    data_collection_to_delete = CurrentDataCollection.find_one({
        '_id': ObjectId(data_collection_id)
    })
    CurrentDataCollectionInteractionMethod.delete_many({
        'data_collection_localid': data_collection_to_delete['identifier']['PITHIA_Identifier']['localID']
    }, session=session)
    DataCollectionInteractionMethodRevision.delete_many({
        'data_collection_localid': data_collection_to_delete['identifier']['PITHIA_Identifier']['localID']
    }, session=session)

def delete_current_version_and_revisions_and_xmls_of_resource_id(resource_id, resource_mongodb_model, resource_revision_mongodb_model, session=None):
    # Find the resource to delete, so it can be referenced later when deleting from
    # the revisions collection
    resource_to_delete = resource_mongodb_model.find_one({
        '_id': ObjectId(resource_id)
    })

    resource_revisions_to_delete = resource_revision_mongodb_model.find({
        'identifier.PITHIA_Identifier.localID': resource_to_delete['identifier']['PITHIA_Identifier']['localID'],
        'identifier.PITHIA_Identifier.namespace': resource_to_delete['identifier']['PITHIA_Identifier']['namespace'],
    })


    resource_ids_to_delete = [resource_id] + [resource['_id'] for resource in resource_revisions_to_delete]
    delete_original_metadata_xmls_of_resource_ids(resource_ids_to_delete, session=session)

    # Delete the current version of the resource
    resource_mongodb_model.delete_one({
        '_id': ObjectId(resource_id)
    }, session=session)

    # Delete revisions stored as version control
    resource_revision_mongodb_model.delete_many({
        'identifier.PITHIA_Identifier.localID': resource_to_delete['identifier']['PITHIA_Identifier']['localID'],
        'identifier.PITHIA_Identifier.namespace': resource_to_delete['identifier']['PITHIA_Identifier']['namespace'],
    }, session=session)

def delete_original_metadata_xmls_of_resource_ids(resource_ids, session=None):
    resource_ids = [ObjectId(resource_id) for resource_id in resource_ids]
    return OriginalMetadataXml.delete_many({
        'resourceId': {
            '$in': resource_ids
        }
    }, session=session)