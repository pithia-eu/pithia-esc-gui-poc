from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from bson.objectid import ObjectId
from common.mongodb_models import AcquisitionRevision, ComputationRevision, CurrentAcquisition, CurrentComputation, CurrentDataCollection, CurrentIndividual, CurrentInstrument, CurrentOperation, CurrentOrganisation, CurrentPlatform, CurrentProcess, CurrentProject, DataCollectionRevision, IndividualRevision, InstrumentRevision, OperationRevision, OrganisationRevision, PlatformRevision, ProcessRevision, ProjectRevision

# Create your views here.
def _create_resource_url(namespace, resource_type, localid):
    return f'https://resources.pithia.eu/2.2/{namespace}/{resource_type}/{resource_type.capitalize()}_{localid}'

def _get_projects_referencing_party_url(party_url):
    return CurrentProject.find({
        'relatedParty.ResponsiblePartyInfo.party.@xlink:href': party_url
    })

def _get_platforms_referencing_party_url(party_url):
    return CurrentPlatform.find({
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

def _get_resources_linked_through_resource_id(resource_id, resource_type, resource_mongodb_model):
    individuals = []
    projects = []
    platforms = []
    instruments = []
    operations = []
    acquisitions = []
    computations = []
    processes = []
    data_collections = []

    linked_resources = []
    resource = resource_mongodb_model.find_one({
        '_id': ObjectId(resource_id)
    })
    resource_pithia_identifier = resource['identifier']['pithia:Identifier']
    resource_url = _create_resource_url(resource_pithia_identifier['namespace'], resource_type, resource_pithia_identifier['localID'])
    print(resource_url)
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
        instruments = _get_instruments_referencing_party_url(resource_url)
        data_collections = _get_data_collections_referencing_party_url(resource_url)
    elif resource_mongodb_model == CurrentProject:
        # Referenced by: Data Collection
        # Data Collection references it via the project prop.
        data_collections = CurrentDataCollection.find({
            'project.@xlink:href': resource_url
        })
        return
    elif resource_mongodb_model == CurrentPlatform:
        # Referenced by: Acquisition
        # Acquisition references it via the platform prop.
        return
    elif resource_mongodb_model == CurrentInstrument:
        # Referenced by: Acquisition (from instrument prop
        # and instrumentModePair.instrument prop)
        return
    elif resource_mongodb_model == CurrentOperation:
        # Operation is part of the Instrument resource
        # as the operationalMode prop. This prop is referenced by
        # Acquisition via the instrumentModePair.mode
        # prop. Operation is NOT ITS OWN resource.
        return
    elif resource_mongodb_model == CurrentAcquisition:
        # Acquisition is referenced by Process via
        # the acquisitionComponent prop.
        return
    elif resource_mongodb_model == CurrentComputation:
        # Referenced by Process via the computationComponent.
        return
    elif resource_mongodb_model == CurrentProcess:
        # Referenced by Data Collection via the om:procedure
        # prop.
        return
    # Data Collection is not included as no other resources
    # (including other data collections) reference this.
    individuals = list(individuals)
    projects = list(projects)
    platforms = list(platforms)
    instruments = list(instruments)
    data_collections = list(data_collections)
    print(len(individuals))
    print(len(projects))
    print(len(platforms))
    print(len(instruments))
    print(len(data_collections))

    return linked_resources

def delete(request, resource_id, resource_mongodb_model, resource_revision_mongodb_model, redirect_view):
    # Find the resource to delete, so it can be referenced later when deleting from
    # the revisions collection
    resource_to_delete = resource_mongodb_model.find_one({
        '_id': ObjectId(resource_id)
    })

    # Delete the current version of the resource
    resource_revision_mongodb_model.delete_one({
        '_id': ObjectId(resource_id)
    })

    # Delete revisions stored as version control
    resource_revision_mongodb_model.delete_many({
        'identifier.pithia:Identifier.localID': resource_to_delete['identifier']['pithia:Identifier']['localID'],
        'identifier.pithia:Identifier.namespace': resource_to_delete['identifier']['pithia:Identifier']['namespace'],
    })

    # Delete resources that are referencing the resource to be deleted. These should not
    # be able to exist without the resource being deleted.
    

    return HttpResponseRedirect(reverse(redirect_view))

@require_POST
def organisation(request, organisation_id):
    _get_resources_linked_through_resource_id(organisation_id, 'organisation', CurrentOrganisation)
    return HttpResponseRedirect(reverse('resource_management:organisations'))
    # return delete(request, organisation_id, CurrentOrganisation, OrganisationRevision)

@require_POST
def individual(request, individual_id):
    return delete(request, individual_id, CurrentIndividual, IndividualRevision)

@require_POST
def project(request, project_id):
    return delete(request, project_id, CurrentProject, ProjectRevision)

@require_POST
def platform(request, platform_id):
    return delete(request, platform_id, CurrentPlatform, PlatformRevision)

@require_POST
def instrument(request, instrument_id):
    return delete(request, instrument_id, CurrentInstrument, InstrumentRevision)

@require_POST
def operation(request, operation_id):
    return delete(request, operation_id, CurrentOperation, OperationRevision)

@require_POST
def acquisition(request, acquisition_id):
    return delete(request, acquisition_id, CurrentAcquisition, AcquisitionRevision)

@require_POST
def computation(request, computation_id):
    return delete(request, computation_id, CurrentComputation, ComputationRevision)

@require_POST
def process(request, process_id):
    return delete(request, process_id, CurrentProcess, ProcessRevision)

@require_POST
def data_collection(request, data_collection_id):
    return delete(request, data_collection_id, CurrentDataCollection, DataCollectionRevision)