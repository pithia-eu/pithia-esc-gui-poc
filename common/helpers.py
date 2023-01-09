from bson import ObjectId

from .mongodb_models import (
    CurrentDataCollectionInteractionMethod,
    CurrentDataCollection,
    CurrentAcquisitionCapability,
    CurrentInstrument,
    CurrentOrganisation,
    CurrentIndividual,
    CurrentProject,
    CurrentPlatform,
    CurrentOperation,
    CurrentAcquisition,
    CurrentComputationCapability,
    CurrentComputation,
    CurrentProcess,
    CurrentCatalogue,
    CurrentCatalogueEntry,
    CurrentCatalogueDataSubset,
)

def _map_id_property(resource):
    return resource['_id']

def get_revision_ids_for_resource_id(resource_id, resource_mongodb_model, resource_revision_mongodb_model):
    resource = resource_mongodb_model.find_one({
        '_id': ObjectId(resource_id)
    }, projection={ 'identifier': 1 })
    return list(map(_map_id_property, list(resource_revision_mongodb_model.find({
        'identifier.PITHIA_Identifier.localID': resource['identifier']['PITHIA_Identifier']['localID'],
        'identifier.PITHIA_Identifier.namespace': resource['identifier']['PITHIA_Identifier']['namespace'],
    }, projection={ '_id': 1 }))))

def get_interaction_methods_linked_to_data_collection_id(data_collection_id):
    data_collection = CurrentDataCollection.find_one({
        '_id': ObjectId(data_collection_id)
    })
    linked_interaction_methods = []
    linked_interaction_methods.extend(list(CurrentDataCollectionInteractionMethod.find({
        'data_collection_localid': data_collection['identifier']['PITHIA_Identifier']['localID']
    })))
    return linked_interaction_methods

def create_resource_url(resource_type, namespace, localid):
    if resource_type.lower() == 'computationcapabilities' and not localid.startswith('ComputationCapabilities_'):
        localid = f'ComputationCapabilities_{localid}'
    if resource_type.lower() == 'acquisitioncapabilities' and not localid.startswith('AcquisitionCapabilities_'):
        localid = f'AcquisitionCapabilities_{localid}'
    if resource_type.lower() == 'process' and not localid.startswith('CompositeProcess_'):
        localid = f'CompositeProcess_{localid}'
    if not resource_type.lower() == 'computationcapabilities' and not resource_type.lower() == 'acquisitioncapabilities' and not  resource_type.lower() == 'process' and not localid.startswith(f'{resource_type.capitalize()}_'):
        localid = f'{resource_type.capitalize()}_{localid}'
    return f'https://metadata.pithia.eu/resources/2.2/{resource_type}/{namespace}/{localid}'

def get_acquisition_capability_sets_referencing_instrument_operational_ids(instrument_id: ObjectId) -> list:
    instrument = CurrentInstrument.find_one({
        '_id': ObjectId(instrument_id)
    }, {
        'identifier': True,
        'operationalMode': True
    })
    if 'operationalMode' not in instrument:
        return []
    instrument_url = create_resource_url('instrument', instrument['identifier']['PITHIA_Identifier']['namespace'], instrument['identifier']['PITHIA_Identifier']['localID'])
    instrument_urls_with_operational_mode_ids = []
    for om in instrument['operationalMode']:
        iom = om['InstrumentOperationalMode']
        instrument_urls_with_operational_mode_ids.append(f'{instrument_url}#{iom["id"]}')
    current_acquisition_capability_sets_referencing_instrument_operational_ids = list(CurrentAcquisitionCapability.find({
        'instrumentModePair.InstrumentOperationalModePair.mode.@xlink:href': {
            '$in': instrument_urls_with_operational_mode_ids
        }
    }))

    return current_acquisition_capability_sets_referencing_instrument_operational_ids

def get_mongodb_model_by_resource_type_from_resource_url(resource_type):
    if resource_type == 'organisation':
        return CurrentOrganisation
    elif resource_type == 'individual':
        return CurrentIndividual
    elif resource_type == 'project':
        return CurrentProject
    elif resource_type == 'platform':
        return CurrentPlatform
    elif resource_type == 'operation':
        return CurrentOperation
    elif resource_type == 'instrument':
        return CurrentInstrument
    elif resource_type == 'acquisitionCapabilities':
        return CurrentAcquisitionCapability
    elif resource_type == 'acquisition':
        return CurrentAcquisition
    elif resource_type == 'computationCapabilities':
        return CurrentComputationCapability
    elif resource_type == 'computation':
        return CurrentComputation
    elif resource_type == 'process':
        return CurrentProcess
    elif resource_type == 'collection':
        return CurrentDataCollection
    elif resource_type == 'catalogue':
        return CurrentCatalogue
    return 'unknown'

def get_mongodb_model_from_catalogue_related_resource_url(resource_url):
    localid = resource_url.split('/')[-1]
    if localid.startswith('Catalogue_'):
        return CurrentCatalogue
    elif localid.startswith('CatalogueEntry_'):
        return CurrentCatalogueEntry
    elif localid.startswith('CatalogueDataSubset_'):
        return CurrentCatalogueDataSubset
    return 'unknown'
