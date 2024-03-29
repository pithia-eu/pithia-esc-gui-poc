from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from lxml import etree

from common import models
from resource_management.views import (
    _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE,
    _create_manage_resource_page_title,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    _INDEX_PAGE_TITLE,
)

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
        context['title'] = f'{self.resource.name} XML'
        context['resource_name'] = self.resource.name
        context['resource_localid'] = self.resource.localid
        context['xml'] = self.xml
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:data_collection_related_metadata_index'
        context['resource_management_list_page_breadcrumb_text'] = _create_manage_resource_page_title(self.model.type_plural_readable.title())
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        return context

class OrganisationXmlDownloadView(ResourceXmlDownloadView):
    model = models.Organisation

    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'

class IndividualXmlDownloadView(ResourceXmlDownloadView):
    model = models.Individual
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'

class ProjectXmlDownloadView(ResourceXmlDownloadView):
    model = models.Project
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'

class PlatformXmlDownloadView(ResourceXmlDownloadView):
    model = models.Platform
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'

class OperationXmlDownloadView(ResourceXmlDownloadView):
    model = models.Operation
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'

class InstrumentXmlDownloadView(ResourceXmlDownloadView):
    model = models.Instrument
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'

class AcquisitionCapabilitiesXmlDownloadView(ResourceXmlDownloadView):
    model = models.AcquisitionCapabilities
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'

class AcquisitionXmlDownloadView(ResourceXmlDownloadView):
    model = models.Acquisition
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'

class ComputationCapabilitiesXmlDownloadView(ResourceXmlDownloadView):
    model = models.ComputationCapabilities
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'

class ComputationXmlDownloadView(ResourceXmlDownloadView):
    model = models.Computation
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'

class ProcessXmlDownloadView(ResourceXmlDownloadView):
    model = models.Process
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'

class DataCollectionXmlDownloadView(ResourceXmlDownloadView):
    model = models.DataCollection
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'

class CatalogueXmlDownloadView(ResourceXmlDownloadView):
    model = models.Catalogue
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogues'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context

class CatalogueEntryXmlDownloadView(ResourceXmlDownloadView):
    model = models.CatalogueEntry
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_entries'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context

class CatalogueDataSubsetXmlDownloadView(ResourceXmlDownloadView):
    model = models.CatalogueDataSubset
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_data_subsets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context

class WorkflowXmlDownloadView(ResourceXmlDownloadView):
    model = models.Workflow
    
    resource_management_list_page_breadcrumb_url_name = 'resource_management:workflows'
