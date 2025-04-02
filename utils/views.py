from django.shortcuts import get_object_or_404
from django.http import (
    FileResponse,
    Http404,
)
from django.views.generic import TemplateView
from lxml import etree

from . import view_mixins

from common.models import ScientificMetadata


# Create your views here.


class ResourceXmlDownloadView(TemplateView):
    resource_id = ''
    resource_name = ''
    resource_localid = ''
    template_name = 'utils/resource_as_xml.html'
    xml = ''
    resource_management_list_page_breadcrumb_text = ''
    resource_management_list_page_breadcrumb_url_name = ''

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['resource_id']
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.resource = get_object_or_404(self.model, pk=self.resource_id)
        _xml = self.resource.xml
        try:
            _xml = _xml.encode('utf-8')
        except AttributeError:
            pass
        self.xml =  etree.tostring(etree.fromstring(_xml.strip()), pretty_print=True, doctype='<?xml version="1.0" encoding="UTF-8"?>').decode()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.resource.name} | XML'
        context['resource_name'] = self.resource.name
        context['resource_localid'] = self.resource.localid
        context['xml'] = self.xml
        return context


class OrganisationXmlDownloadFromBrowsingView(
        view_mixins.OrganisationXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    pass


class IndividualXmlDownloadFromBrowsingView(
        view_mixins.IndividualXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    pass


class ProjectXmlDownloadFromBrowsingView(
        view_mixins.ProjectXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    pass


class PlatformXmlDownloadFromBrowsingView(
        view_mixins.PlatformXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    pass


class OperationXmlDownloadFromBrowsingView(
        view_mixins.OperationXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    pass


class InstrumentXmlDownloadFromBrowsingView(
        view_mixins.InstrumentXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    pass


class AcquisitionCapabilitiesXmlDownloadFromBrowsingView(
        view_mixins.AcquisitionCapabilitiesXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    pass


class AcquisitionXmlDownloadFromBrowsingView(
        view_mixins.AcquisitionXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    pass


class ComputationCapabilitiesXmlDownloadFromBrowsingView(
        view_mixins.ComputationCapabilitiesXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    pass


class ComputationXmlDownloadFromBrowsingView(
        view_mixins.ComputationXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    pass


class ProcessXmlDownloadFromBrowsingView(
        view_mixins.ProcessXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    pass


class DataCollectionXmlDownloadFromBrowsingView(
        view_mixins.DataCollectionXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    pass


class StaticDatasetXmlDownloadFromBrowsingView(
        view_mixins.StaticDatasetXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    template_name = 'utils/from_browsing/resource_as_xml_from_browsing_2.html'


class StaticDatasetEntryXmlDownloadFromBrowsingView(
        view_mixins.StaticDatasetEntryXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    template_name = 'utils/from_browsing/resource_as_xml_from_browsing_2.html'


class DataSubsetXmlDownloadFromBrowsingView(
        view_mixins.DataSubsetXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    template_name = 'utils/from_browsing/resource_as_xml_from_browsing_2.html'


class WorkflowXmlDownloadFromBrowsingView(
        view_mixins.WorkflowXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    template_name = 'utils/from_browsing/resource_as_xml_from_browsing_2.html'


def metadata_xml_file_direct_download(request, resource_type, resource_namespace, resource_id):
    scientific_metadata_model_subclasses = list(ScientificMetadata.__subclasses__())
    model = next(
        (
            m
            for m in scientific_metadata_model_subclasses
            if m.type_in_metadata_server_url == resource_type
        ), None)
    if not model:
        raise Http404(f'"{resource_type}" is not a valid metadata type.')
    try:
        resource = model.objects.get_by_namespace_and_localid(resource_namespace, resource_id)
    except ScientificMetadata.DoesNotExist:
        raise Http404(f'Metadata with a namespace of "{resource_namespace}" and a local ID of "{resource_id}" was not found.')
    response = FileResponse(
        resource.xml,
        content_type='application/xml'
    )
    response['Content-Disposition'] = f'filename="{resource_id}.xml"'
    return response