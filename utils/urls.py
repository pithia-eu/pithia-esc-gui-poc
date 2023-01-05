from django.urls import path

from . import views

app_name = 'utils'
urlpatterns = [
    path('utils/convert/urls', views.get_esc_url_templates_for_ontology_server_urls_and_resource_server_urls, name='convert_server_urls'),
    path('organisations/<organisation_id>/xml', views.OrganisationXmlDownloadView.as_view(), name='view_organisation_as_xml'),
    path('individuals/<individual_id>/xml', views.IndividualXmlDownloadView.as_view(), name='view_individual_as_xml'),
    path('projects/<project_id>/xml', views.ProjectXmlDownloadView.as_view(), name='view_project_as_xml'),
    path('platforms/<platform_id>/xml', views.PlatformXmlDownloadView.as_view(), name='view_platform_as_xml'),
    path('operations/<operation_id>/xml', views.OperationXmlDownloadView.as_view(), name='view_operation_as_xml'),
    path('instruments/<instrument_id>/xml', views.InstrumentXmlDownloadView.as_view(), name='view_instrument_as_xml'),
    path('acquisition-capabilities/<acquisition_capability_set_id>/xml', views.AcquisitionCapabilitiesXmlDownloadView.as_view(), name='view_acquisition_capability_set_as_xml'),
    path('acquisitions/<acquisition_id>/xml', views.AcquisitionXmlDownloadView.as_view(), name='view_acquisition_as_xml'),
    path('computation-capabilities/<computation_capability_set_id>/xml', views.ComputationCapabilitiesXmlDownloadView.as_view(), name='view_computation_capability_set_as_xml'),
    path('computations/<computation_id>/xml', views.ComputationXmlDownloadView.as_view(), name='view_computation_as_xml'),
    path('processs/<process_id>/xml', views.ProcessXmlDownloadView.as_view(), name='view_process_as_xml'),
    path('data-collections/<data_collection_id>/xml', views.DataCollectionXmlDownloadView.as_view(), name='view_data_collection_as_xml'),
    path('catalogues/<catalogue_id>/xml', views.view_catalogue_as_xml.as_view(), name='view_catalogue_as_xml'),
    path('catalogues/<catalogue_entry_id>/xml', views.view_catalogue_entry_as_xml.as_view(), name='view_catalogue_entry_as_xml'),
    path('catalogues/<catalogue_data_subset_id>/xml', views.view_catalogue_data_subset_as_xml.as_view(), name='view_catalogue_data_subset_as_xml'),
]
