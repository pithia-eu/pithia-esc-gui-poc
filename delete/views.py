from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from bson.objectid import ObjectId
from common.mongodb_models import AcquisitionRevision, ComputationRevision, CurrentAcquisition, CurrentComputation, CurrentDataCollection, CurrentIndividual, CurrentInstrument, CurrentOperation, CurrentOrganisation, CurrentPlatform, CurrentProcess, CurrentProject, DataCollectionRevision, IndividualRevision, InstrumentRevision, OperationRevision, OrganisationRevision, PlatformRevision, ProcessRevision, ProjectRevision
from django.views.generic import View

# Create your views here.
def _create_resource_url(namespace, resource_type, localid):
    if not localid.startswith(f'{resource_type.capitalize()}_'):
        localid = f'{resource_type.capitalize()}_{localid}'
    return f'https://resources.pithia.eu/2.2/{namespace}/{resource_type}/{localid}'

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
    elif resource_mongodb_model == CurrentPlatform:
        # Referenced by: Acquisition
        # Acquisition references it via the platform prop.
        acquisitions = CurrentAcquisition.find({
            'platform.@xlink:href': resource_url
        })
    elif resource_mongodb_model == CurrentInstrument:
        # Referenced by: Acquisition (from instrument prop
        # and instrumentModePair.instrument prop)
        acquisitions = CurrentAcquisition.find({
            'instrument.@xlink:href': resource_url
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
    elif resource_mongodb_model == CurrentAcquisition:
        # Acquisition is referenced by Process via
        # the acquisitionComponent prop.
        processes = CurrentProcess.find({
            'acquisitionComponent.@xlink.href': resource_url
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
        individuals[i] = (individuals[i], 'individual', CurrentIndividual)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(individuals[i][0]['_id']), 'individual', individuals[i][2]))
    projects = list(projects)
    for i in range(len(projects)):
        projects[i] = (projects[i], 'project', CurrentProject)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(projects[i][0]['_id']), 'project', projects[i][2]))
    platforms = list(platforms)
    for i in range(len(platforms)):
        platforms[i] = (platforms[i], 'platform', CurrentPlatform)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(platforms[i][2][0]['_id']), 'platform', platforms[i][2]))
    instruments = list(instruments)
    for i in range(len(instruments)):
        instruments[i] = (instruments[i], 'instrument', CurrentInstrument)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(instruments[i][2][0]['_id']), 'instrument', instruments[i][2]))
    acquisitions = list(acquisitions)
    for i in range(len(acquisitions)):
        acquisitions[i] = (acquisitions[i], 'acquisition', CurrentAcquisition)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(acquisitions[i][2][0]['_id']), 'acquisition', acquisitions[i][2]))
    computations = list(computations)
    for i in range(len(computations)):
        computations[i] = (computations[i], 'computation', CurrentComputation)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(computations[i][2][0]['_id']), 'computation', computations[i][2]))
    processes = list(processes)
    for i in range(len(processes)):
        processes[i] = (processes[i], 'process', CurrentProcess)
        linked_resources.extend(_get_resources_linked_through_resource_id(str(processes[i][2][0]['_id']), 'process', processes[i][2]))
    data_collections = list(data_collections)
    for i in range(len(data_collections)):
        data_collections[i] = (data_collections[i], 'collection', CurrentDataCollection)
    linked_resources.extend(individuals)
    linked_resources.extend(projects)
    linked_resources.extend(platforms)
    linked_resources.extend(instruments)
    linked_resources.extend(acquisitions)
    linked_resources.extend(computations)
    linked_resources.extend(processes)
    linked_resources.extend(data_collections)

    return linked_resources

class DeleteResourceView(View):
    resource_id = ''
    resource_type = ''
    resource_mongodb_model = None
    resource_revision_mongodb_model = None
    redirect_url = ''

    def post(self, request, *args, **kwargs):
        # Find the resource to delete, so it can be referenced later when deleting from
        # the revisions collection
        # resource_to_delete = self.resource_mongodb_model.find_one({
        #     '_id': ObjectId(self.resource_id)
        # })

        # # Delete the current version of the resource
        # self.resource_revision_mongodb_model.delete_one({
        #     '_id': ObjectId(self.resource_id)
        # })

        # # Delete revisions stored as version control
        # self.resource_revision_mongodb_model.delete_many({
        #     'identifier.pithia:Identifier.localID': resource_to_delete['identifier']['pithia:Identifier']['localID'],
        #     'identifier.pithia:Identifier.namespace': resource_to_delete['identifier']['pithia:Identifier']['namespace'],
        # })

        # Delete resources that are referencing the resource to be deleted. These should not
        # be able to exist without the resource being deleted.
        linked_resources = _get_resources_linked_through_resource_id(self.resource_id, self.resource_type, self.resource_mongodb_model)
        for r in linked_resources:
            r_pithia_identifier = r[0]['identifier']['pithia:Identifier']
            print(_create_resource_url(r_pithia_identifier['namespace'], r[1], r_pithia_identifier['localID']))

        return HttpResponseRedirect(self.redirect_url)


class organisation(DeleteResourceView):
    resource_type = 'organisation'
    resource_mongodb_model = CurrentOrganisation
    resource_revision_mongodb_model = OrganisationRevision
    redirect_url = reverse_lazy('resource_management:organisations')

    def post(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['organisation_id']
        return super().post(request, *args, **kwargs)

class individual(DeleteResourceView):
    resource_type = 'individual'
    resource_mongodb_model = CurrentIndividual
    resource_revision_mongodb_model = IndividualRevision
    redirect_url = reverse_lazy('resource_management:individuals')

    def post(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['individual_id']
        return super().post(request, *args, **kwargs)

class project(DeleteResourceView):
    resource_type = 'project'
    resource_mongodb_model = CurrentProject
    resource_revision_mongodb_model = ProjectRevision
    redirect_url = reverse_lazy('resource_management:projects')

    def post(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['project_id']
        return super().post(request, *args, **kwargs)

class platform(DeleteResourceView):
    resource_type = 'platform'
    resource_mongodb_model = CurrentPlatform
    resource_revision_mongodb_model = PlatformRevision
    redirect_url = reverse_lazy('resource_management:platforms')

    def post(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['platform_id']
        return super().post(request, *args, **kwargs)

class instrument(DeleteResourceView):
    resource_type = 'instrument'
    resource_mongodb_model = CurrentInstrument
    resource_revision_mongodb_model = InstrumentRevision
    redirect_url = reverse_lazy('resource_management:instruments')

    def post(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['instrument_id']
        return super().post(request, *args, **kwargs)

class operation(DeleteResourceView):
    resource_type = 'operation'
    resource_mongodb_model = CurrentOperation
    resource_revision_mongodb_model = OperationRevision
    redirect_url = reverse_lazy('resource_management:operations')

    def post(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['operation_id']
        return super().post(request, *args, **kwargs)

class acquisition(DeleteResourceView):
    resource_type = 'acquisition'
    resource_mongodb_model = CurrentAcquisition
    resource_revision_mongodb_model = AcquisitionRevision
    redirect_url = reverse_lazy('resource_management:acquisitions')

    def post(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_id']
        return super().post(request, *args, **kwargs)

class computation(DeleteResourceView):
    resource_type = 'computation'
    resource_mongodb_model = CurrentComputation
    resource_revision_mongodb_model = ComputationRevision
    redirect_url = reverse_lazy('resource_management:computations')

    def post(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_id']
        return super().post(request, *args, **kwargs)

class process(DeleteResourceView):
    resource_type = 'process'
    resource_mongodb_model = CurrentProcess
    resource_revision_mongodb_model = ProcessRevision
    redirect_url = reverse_lazy('resource_management:processes')

    def post(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['process_id']
        return super().post(request, *args, **kwargs)

class data_collection(DeleteResourceView):
    resource_type = 'collection'
    resource_mongodb_model = CurrentDataCollection
    resource_revision_mongodb_model = DataCollectionRevision
    redirect_url = reverse_lazy('resource_management:data_collections')

    def post(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        return super().post(request, *args, **kwargs)