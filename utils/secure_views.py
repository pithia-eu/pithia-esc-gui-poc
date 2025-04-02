from django.utils.decorators import method_decorator

from . import view_mixins
from .views import ResourceXmlDownloadView

from common.decorators import login_session_institution_required, institution_ownership_required


@method_decorator(login_session_institution_required, name='dispatch')
@method_decorator(institution_ownership_required, name='dispatch')
class ResourceXmlDownloadFromManagementView(
        view_mixins.ResourceXmlDownloadFromManagementViewMixin,
        ResourceXmlDownloadView):
    pass


class OrganisationXmlDownloadFromManagementView(
        view_mixins.OrganisationXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class IndividualXmlDownloadFromManagementView(
        view_mixins.IndividualXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class ProjectXmlDownloadFromManagementView(
        view_mixins.ProjectXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class PlatformXmlDownloadFromManagementView(
        view_mixins.PlatformXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class OperationXmlDownloadFromManagementView(
        view_mixins.OperationXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class InstrumentXmlDownloadFromManagementView(
        view_mixins.InstrumentXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class AcquisitionCapabilitiesXmlDownloadFromManagementView(
        view_mixins.AcquisitionCapabilitiesXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class AcquisitionXmlDownloadFromManagementView(
        view_mixins.AcquisitionXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class ComputationCapabilitiesXmlDownloadFromManagementView(
        view_mixins.ComputationCapabilitiesXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class ComputationXmlDownloadFromManagementView(
        view_mixins.ComputationXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class ProcessXmlDownloadFromManagementView(
        view_mixins.ProcessXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class DataCollectionXmlDownloadFromManagementView(
        view_mixins.DataCollectionXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class CatalogueXmlDownloadFromManagementView(
        view_mixins.CatalogueXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class StaticDatasetEntryXmlDownloadFromManagementView(
        view_mixins.StaticDatasetEntryXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class DataSubsetXmlDownloadFromManagementView(
        view_mixins.DataSubsetXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    pass


class WorkflowXmlDownloadFromManagementView(
        view_mixins.WorkflowXmlDownloadViewMixin,
        ResourceXmlDownloadFromManagementView):
    template_name = 'utils/from_management/resource_as_xml_from_management_2.html'