from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from bson.objectid import ObjectId
from common.mongodb_models import AcquisitionRevision, ComputationRevision, CurrentAcquisition, CurrentComputation, CurrentDataCollection, CurrentIndividual, CurrentInstrument, CurrentOperation, CurrentOrganisation, CurrentPlatform, CurrentProcess, CurrentProject, DataCollectionRevision, IndividualRevision, InstrumentRevision, OperationRevision, OrganisationRevision, PlatformRevision, ProcessRevision, ProjectRevision

# Create your views here.
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
    return delete(request, organisation_id, CurrentOrganisation, OrganisationRevision, )

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