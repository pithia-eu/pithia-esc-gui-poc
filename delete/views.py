from functools import cmp_to_key
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from bson.objectid import ObjectId
from common.mongodb_models import AcquisitionCapabilityRevision, AcquisitionRevision, ComputationCapabilityRevision, ComputationRevision, CurrentAcquisition, CurrentAcquisitionCapability, CurrentComputation, CurrentComputationCapability, CurrentDataCollection, CurrentIndividual, CurrentInstrument, CurrentOperation, CurrentOrganisation, CurrentPlatform, CurrentProcess, CurrentProject, DataCollectionRevision, IndividualRevision, InstrumentRevision, OperationRevision, OrganisationRevision, PlatformRevision, ProcessRevision, ProjectRevision
from django.views.generic import TemplateView
from resource_management.views import _INDEX_PAGE_TITLE

# Create your views here.
def _create_resource_url(resource_type, namespace, localid):
    if not localid.startswith(f'{resource_type.capitalize()}_'):
        localid = f'{resource_type.capitalize()}_{localid}'
    return f'https://metadata.pithia.eu/resources/2.2/{resource_type}/{namespace}/{localid}'

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

def _get_resources_linked_through_resource_id(resource_id, resource_type, resource_mongodb_model):
    individuals = []
    projects = []
    platforms = []
    instruments = []
    operations = []
    acquisition_capabilities = []
    acquisitions = []
    computation_capabilities = []
    computations = []
    processes = []
    data_collections = []

    linked_resources = []
    resource = resource_mongodb_model.find_one({
        '_id': ObjectId(resource_id)
    })
    resource_pithia_identifier = resource['identifier']['PITHIA_Identifier']
    resource_url = _create_resource_url(resource_type, resource_pithia_identifier['namespace'], resource_pithia_identifier['localID'])
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
        # Referenced by: Acquisition
        # Acquisition references it via the platform prop.
        acquisitions = CurrentAcquisition.find({
            'platform.@xlink:href': resource_url
        })
    elif resource_mongodb_model == CurrentInstrument:
        # Referenced by: Acquisition (from instrument prop)
        acquisitions = CurrentAcquisition.find({
            'instrument.@xlink:href': resource_url
        })
        # Referenced by: AcquisitionCapability (from
        # instrumentModePair.InstrumentOperationalModePair.instrument prop and
        # instrumentModePair.InstrumentOperationalModePair.mode prop)
        acquisition_capabilities = CurrentAcquisitionCapability.find({
            '$or': [
                {
                    'instrumentModePair.InstrumentOperationalModePair.instrument.@xlink:href': resource_url
                },
                {
                    'instrumentModePair.InstrumentOperationalModePair.mode.@xlink:href': resource_url
                }
            ]
        })
    # elif resource_mongodb_model == CurrentOperation:
    #     # Operation is part of the Instrument resource
    #     # as the operationalMode prop. This prop is referenced by
    #     # Acquisition via the instrumentModePair.mode
    #     # prop. Operation is NOT ITS OWN resource.
    #     acquisitions = CurrentAcquisition.find({
    #         'instrumentModePair.mode': resource_url
    #     })
    #     return
    elif resource_mongodb_model == CurrentAcquisitionCapability:
        # AcquisitionCapability is referenced by Acquisition via
        # the acquisitionCapabilities prop.
        acquisitions = CurrentAcquisition.find({
            'capabilityLinks.capabilityLink.acquisitionCapabilities.@xlink.href': resource_url
        })
    elif resource_mongodb_model == CurrentAcquisition:
        # Acquisition is referenced by Process via
        # the acquisitionComponent prop.
        processes = CurrentProcess.find({
            'acquisitionComponent.@xlink.href': resource_url
        })
    elif resource_mongodb_model == CurrentComputationCapability:
        # ComputationCapability is referenced by Computation via the computationCapabilities
        # prop.
        # ComputationCapabilities can reference other ComputationCapabilities via the
        # childComputation prop.
        computation_capabilities = CurrentComputationCapability.find({
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
        linked_resources.extend(_get_resources_linked_through_resource_id(str(individuals[i][0]['_id']), 'individual', individuals[i][2]))
    projects = list(projects)
    for i in range(len(projects)):
        projects[i] = (projects[i], 'project', CurrentProject, ProjectRevision)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(projects[i][0]['_id']), 'project', projects[i][2]))
    platforms = list(platforms)
    for i in range(len(platforms)):
        platforms[i] = (platforms[i], 'platform', CurrentPlatform, PlatformRevision)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(platforms[i][0]['_id']), 'platform', platforms[i][2]))
    operations = list(operations)
    for i in range(len(operations)):
        operations[i] = (operations[i], 'operation', CurrentOperation, OperationRevision)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(operations[i][0]['_id']), 'operation', operations[i][2]))
    instruments = list(instruments)
    for i in range(len(instruments)):
        instruments[i] = (instruments[i], 'instrument', CurrentInstrument, InstrumentRevision)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(instruments[i][0]['_id']), 'instrument', instruments[i][2]))
    acquisition_capabilities = list(acquisition_capabilities)
    for i in range(len(acquisition_capabilities)):
        acquisition_capabilities[i] = (acquisition_capabilities[i], 'acquisition capability', CurrentAcquisitionCapability, AcquisitionCapabilityRevision)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(acquisition_capabilities[i][0]['_id']), 'acquisition capability', acquisition_capabilities[i][2]))
    acquisitions = list(acquisitions)
    for i in range(len(acquisitions)):
        acquisitions[i] = (acquisitions[i], 'acquisition', CurrentAcquisition, AcquisitionRevision)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(acquisitions[i][0]['_id']), 'acquisition', acquisitions[i][2]))
    computation_capabilities = list(computation_capabilities)
    for i in range(len(computation_capabilities)):
        computation_capabilities[i] = (computation_capabilities[i], 'computation capability', CurrentComputationCapability, ComputationCapabilityRevision)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(computation_capabilities[i][0]['_id']), 'computation capability', computation_capabilities[i][2]))
    computations = list(computations)
    for i in range(len(computations)):
        computations[i] = (computations[i], 'computation', CurrentComputation, ComputationRevision)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(computations[i][0]['_id']), 'computation', computations[i][2]))
    processes = list(processes)
    for i in range(len(processes)):
        processes[i] = (processes[i], 'process', CurrentProcess, ProcessRevision)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(processes[i][0]['_id']), 'process', processes[i][2]))
    data_collections = list(data_collections)
    for i in range(len(data_collections)):
        data_collections[i] = (data_collections[i], 'collection', CurrentDataCollection, DataCollectionRevision)
    linked_resources.extend(individuals)
    linked_resources.extend(projects)
    linked_resources.extend(platforms)
    linked_resources.extend(operations)
    linked_resources.extend(instruments)
    linked_resources.extend(acquisition_capabilities)
    linked_resources.extend(acquisitions)
    linked_resources.extend(computation_capabilities)
    linked_resources.extend(computations)
    linked_resources.extend(processes)
    linked_resources.extend(data_collections)
    linked_resources = list({ str(v[0]['_id']):v for v in linked_resources }.values())
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
        elif resource_type == 'acquisition capability':
            return 7
        elif resource_type == 'acquisition':
            return 8
        elif resource_type == 'computation capability':
            return 9
        elif resource_type == 'computation':
            return 10
        elif resource_type == 'process':
            return 11
        elif resource_type == 'collection':
            return 12
        return 12
    def custom_compare(item1, item2):
        item1_weight = get_weight_of_resource_type(item1[1])
        item2_weight = get_weight_of_resource_type(item2[1])
        if item1_weight < item2_weight:
            return -1
        elif item1_weight > item2_weight:
            return 1
        else:
            return 0
    linked_resources.sort(key=cmp_to_key(custom_compare))

    return linked_resources

def _delete_current_version_and_revisions_of_resource_id(resource_id, resource_mongodb_model, resource_revision_mongodb_model):
    # Find the resource to delete, so it can be referenced later when deleting from
    # the revisions collection
    resource_to_delete = resource_mongodb_model.find_one({
        '_id': ObjectId(resource_id)
    })

    # Delete the current version of the resource
    resource_mongodb_model.delete_one({
        '_id': ObjectId(resource_id)
    })

    # Delete revisions stored as version control
    resource_revision_mongodb_model.delete_many({
        'identifier.PITHIA_Identifier.localID': resource_to_delete['identifier']['PITHIA_Identifier']['localID'],
        'identifier.PITHIA_Identifier.namespace': resource_to_delete['identifier']['PITHIA_Identifier']['namespace'],
    })



class DeleteResourceView(TemplateView):
    resource_id = ''
    resource_type = ''
    resource_mongodb_model = None
    resource_revision_mongodb_model = None
    redirect_url = ''
    template_name = 'delete/confirm_delete_resource.html'
    list_resources_of_type_view_page_title = 'Manage Resources'
    list_resources_of_type_view_name = 'resource_management:index'
    delete_resource_type_view_name = ''
    resource_to_delete = None
    other_resources_to_delete = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_type'] = self.resource_type
        if self.resource_type.lower() == 'collection':
            context['resource_type'] = 'data collection'
        context['title'] = f'Confirm Deletion of Data Registration'
        context['resource_management_index_page_title'] = _INDEX_PAGE_TITLE
        context['list_resources_of_type_view_page_title'] = self.list_resources_of_type_view_page_title
        context['list_resources_of_type_view_name'] = self.list_resources_of_type_view_name
        context['delete_resource_type_view_name'] = self.delete_resource_type_view_name
        context['resource_id'] = self.resource_id
        context['resource_to_delete'] = self.resource_to_delete
        context['other_resources_to_delete'] = self.other_resources_to_delete
        return context

    def get(self, request, *args, **kwargs):
        self.resource_to_delete = self.resource_mongodb_model.find_one({
            '_id': ObjectId(self.resource_id)
        })
        self.other_resources_to_delete = _get_resources_linked_through_resource_id(self.resource_id, self.resource_type, self.resource_mongodb_model)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Delete the resource and resources that are referencing the resource to be deleted. These should not
        # be able to exist without the resource being deleted.
        linked_resources = _get_resources_linked_through_resource_id(self.resource_id, self.resource_type, self.resource_mongodb_model)
        _delete_current_version_and_revisions_of_resource_id(self.resource_id, self.resource_mongodb_model, self.resource_revision_mongodb_model)
        for r in linked_resources:
            _delete_current_version_and_revisions_of_resource_id(r[0]['_id'], r[2], r[3])
        return HttpResponseRedirect(self.redirect_url)


class organisation(DeleteResourceView):
    resource_type = 'organisation'
    resource_mongodb_model = CurrentOrganisation
    resource_revision_mongodb_model = OrganisationRevision
    redirect_url = reverse_lazy('resource_management:organisations')
    list_resources_of_type_view_page_title = 'Manage Organisations'
    list_resources_of_type_view_name = 'resource_management:organisations'
    delete_resource_type_view_name = 'delete:organisation'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['organisation_id']
        return super().dispatch(request, *args, **kwargs)

class individual(DeleteResourceView):
    resource_type = 'individual'
    resource_mongodb_model = CurrentIndividual
    resource_revision_mongodb_model = IndividualRevision
    redirect_url = reverse_lazy('resource_management:individuals')
    list_resources_of_type_view_page_title = 'Manage Individuals'
    list_resources_of_type_view_name = 'resource_management:individuals'
    delete_resource_type_view_name = 'delete:individual'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['individual_id']
        return super().dispatch(request, *args, **kwargs)

class project(DeleteResourceView):
    resource_type = 'project'
    resource_mongodb_model = CurrentProject
    resource_revision_mongodb_model = ProjectRevision
    redirect_url = reverse_lazy('resource_management:projects')
    list_resources_of_type_view_page_title = 'Manage Projects'
    list_resources_of_type_view_name = 'resource_management:projects'
    delete_resource_type_view_name = 'delete:project'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['project_id']
        return super().dispatch(request, *args, **kwargs)

class platform(DeleteResourceView):
    resource_type = 'platform'
    resource_mongodb_model = CurrentPlatform
    resource_revision_mongodb_model = PlatformRevision
    redirect_url = reverse_lazy('resource_management:platforms')
    list_resources_of_type_view_page_title = 'Manage Platforms'
    list_resources_of_type_view_name = 'resource_management:platforms'
    delete_resource_type_view_name = 'delete:platform'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['platform_id']
        return super().dispatch(request, *args, **kwargs)

class instrument(DeleteResourceView):
    resource_type = 'instrument'
    resource_mongodb_model = CurrentInstrument
    resource_revision_mongodb_model = InstrumentRevision
    redirect_url = reverse_lazy('resource_management:instruments')
    list_resources_of_type_view_page_title = 'Manage Instruments'
    list_resources_of_type_view_name = 'resource_management:instruments'
    delete_resource_type_view_name = 'delete:instrument'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['instrument_id']
        return super().dispatch(request, *args, **kwargs)

class operation(DeleteResourceView):
    resource_type = 'operation'
    resource_mongodb_model = CurrentOperation
    resource_revision_mongodb_model = OperationRevision
    redirect_url = reverse_lazy('resource_management:operations')
    list_resources_of_type_view_page_title = 'Manage Operations'
    list_resources_of_type_view_name = 'resource_management:operations'
    delete_resource_type_view_name = 'delete:operation'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['operation_id']
        return super().dispatch(request, *args, **kwargs)

class acquisition_capability(DeleteResourceView):
    resource_type = 'acquisition capability'
    resource_mongodb_model = CurrentAcquisitionCapability
    resource_revision_mongodb_model = AcquisitionCapabilityRevision
    redirect_url = reverse_lazy('resource_management:acquisition_capabilities')
    list_resources_of_type_view_page_title = 'Manage Acquisition Capabilities'
    list_resources_of_type_view_name = 'resource_management:acquisition_capabilities'
    delete_resource_type_view_name = 'delete:acquisition_capability'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_capability_id']
        return super().dispatch(request, *args, **kwargs)

class acquisition(DeleteResourceView):
    resource_type = 'acquisition'
    resource_mongodb_model = CurrentAcquisition
    resource_revision_mongodb_model = AcquisitionRevision
    redirect_url = reverse_lazy('resource_management:acquisitions')
    list_resources_of_type_view_page_title = 'Manage Acquisitions'
    list_resources_of_type_view_name = 'resource_management:acquisitions'
    delete_resource_type_view_name = 'delete:acquisition'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_id']
        return super().dispatch(request, *args, **kwargs)

class computation_capability(DeleteResourceView):
    resource_type = 'computation capability'
    resource_mongodb_model = CurrentComputationCapability
    resource_revision_mongodb_model = ComputationCapabilityRevision
    redirect_url = reverse_lazy('resource_management:computation_capabilities')
    list_resources_of_type_view_page_title = 'Manage Computation Capabilities'
    list_resources_of_type_view_name = 'resource_management:computation_capabilities'
    delete_resource_type_view_name = 'delete:computation_capability'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_capability_id']
        return super().dispatch(request, *args, **kwargs)

class computation(DeleteResourceView):
    resource_type = 'computation'
    resource_mongodb_model = CurrentComputation
    resource_revision_mongodb_model = ComputationRevision
    redirect_url = reverse_lazy('resource_management:computations')
    list_resources_of_type_view_page_title = 'Manage Computations'
    list_resources_of_type_view_name = 'resource_management:computations'
    delete_resource_type_view_name = 'delete:computation'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_id']
        return super().dispatch(request, *args, **kwargs)

class process(DeleteResourceView):
    resource_type = 'process'
    resource_mongodb_model = CurrentProcess
    resource_revision_mongodb_model = ProcessRevision
    redirect_url = reverse_lazy('resource_management:processes')
    list_resources_of_type_view_page_title = 'Manage Processes'
    list_resources_of_type_view_name = 'resource_management:processes'
    delete_resource_type_view_name = 'delete:process'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['process_id']
        return super().dispatch(request, *args, **kwargs)

class data_collection(DeleteResourceView):
    resource_type = 'collection'
    resource_mongodb_model = CurrentDataCollection
    resource_revision_mongodb_model = DataCollectionRevision
    redirect_url = reverse_lazy('resource_management:data_collections')
    list_resources_of_type_view_page_title = 'Manage Data Collections'
    list_resources_of_type_view_name = 'resource_management:data_collections'
    delete_resource_type_view_name = 'delete:data_collection'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        return super().dispatch(request, *args, **kwargs)