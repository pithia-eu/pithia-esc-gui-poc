from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from lxml import etree

from . import view_mixins

from common import models

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
    model = models.Organisation
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'


class IndividualXmlDownloadFromBrowsingView(
        view_mixins.IndividualXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    model = models.Individual
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'


class ProjectXmlDownloadFromBrowsingView(
        view_mixins.ProjectXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    model = models.Project
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'


class PlatformXmlDownloadFromBrowsingView(
        view_mixins.PlatformXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    model = models.Platform
    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'


class OperationXmlDownloadFromBrowsingView(
        view_mixins.OperationXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    model = models.Operation
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'


class InstrumentXmlDownloadFromBrowsingView(
        view_mixins.InstrumentXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    model = models.Instrument
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'


class AcquisitionCapabilitiesXmlDownloadFromBrowsingView(
        view_mixins.AcquisitionCapabilitiesXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    model = models.AcquisitionCapabilities
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'


class AcquisitionXmlDownloadFromBrowsingView(
        view_mixins.AcquisitionXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    model = models.Acquisition
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'


class ComputationCapabilitiesXmlDownloadFromBrowsingView(
        view_mixins.ComputationCapabilitiesXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    model = models.ComputationCapabilities
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'


class ComputationXmlDownloadFromBrowsingView(
        view_mixins.ComputationXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    model = models.Computation
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'


class ProcessXmlDownloadFromBrowsingView(
        view_mixins.ProcessXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    model = models.Process
    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'


class DataCollectionXmlDownloadFromBrowsingView(
        view_mixins.DataCollectionXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    model = models.DataCollection
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'


class CatalogueXmlDownloadFromBrowsingView(
        view_mixins.CatalogueXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    template_name = 'utils/from_browsing/resource_as_xml_from_browsing_2.html'
    model = models.Catalogue
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogues'


class CatalogueEntryXmlDownloadFromBrowsingView(
        view_mixins.CatalogueEntryXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    template_name = 'utils/from_browsing/resource_as_xml_from_browsing_2.html'
    model = models.CatalogueEntry
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_entries'


class CatalogueDataSubsetXmlDownloadFromBrowsingView(
        view_mixins.CatalogueDataSubsetXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    template_name = 'utils/from_browsing/resource_as_xml_from_browsing_2.html'
    model = models.CatalogueDataSubset
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_data_subsets'


class WorkflowXmlDownloadFromBrowsingView(
        view_mixins.WorkflowXmlDownloadViewMixin,
        view_mixins.ResourceXmlDownloadFromBrowsingViewMixin,
        ResourceXmlDownloadView):
    template_name = 'utils/from_browsing/resource_as_xml_from_browsing_2.html'
    model = models.Workflow
    resource_management_list_page_breadcrumb_url_name = 'resource_management:workflows'
