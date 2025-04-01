from django.urls import path

from . import views

app_name = 'utils'
urlpatterns = [
    path('organisations/<resource_id>/xml/', views.OrganisationXmlDownloadFromBrowsingView.as_view(), name='view_organisation_as_xml'),
    path('individuals/<resource_id>/xml/', views.IndividualXmlDownloadFromBrowsingView.as_view(), name='view_individual_as_xml'),
    path('projects/<resource_id>/xml/', views.ProjectXmlDownloadFromBrowsingView.as_view(), name='view_project_as_xml'),
    path('platforms/<resource_id>/xml/', views.PlatformXmlDownloadFromBrowsingView.as_view(), name='view_platform_as_xml'),
    path('operations/<resource_id>/xml/', views.OperationXmlDownloadFromBrowsingView.as_view(), name='view_operation_as_xml'),
    path('instruments/<resource_id>/xml/', views.InstrumentXmlDownloadFromBrowsingView.as_view(), name='view_instrument_as_xml'),
    path('acquisition-capabilities/<resource_id>/xml/', views.AcquisitionCapabilitiesXmlDownloadFromBrowsingView.as_view(), name='view_acquisition_capability_set_as_xml'),
    path('acquisitions/<resource_id>/xml/', views.AcquisitionXmlDownloadFromBrowsingView.as_view(), name='view_acquisition_as_xml'),
    path('computation-capabilities/<resource_id>/xml/', views.ComputationCapabilitiesXmlDownloadFromBrowsingView.as_view(), name='view_computation_capability_set_as_xml'),
    path('computations/<resource_id>/xml/', views.ComputationXmlDownloadFromBrowsingView.as_view(), name='view_computation_as_xml'),
    path('process/<resource_id>/xml/', views.ProcessXmlDownloadFromBrowsingView.as_view(), name='view_process_as_xml'),
    path('data-collections/<resource_id>/xml/', views.DataCollectionXmlDownloadFromBrowsingView.as_view(), name='view_data_collection_as_xml'),
    path('catalogues/<resource_id>/xml/', views.CatalogueXmlDownloadFromBrowsingView.as_view(), name='view_catalogue_as_xml'),
    path('catalogue-entries/<resource_id>/xml/', views.CatalogueEntryXmlDownloadFromBrowsingView.as_view(), name='view_catalogue_entry_as_xml'),
    path('catalogue-data-subsets/<resource_id>/xml/', views.CatalogueDataSubsetXmlDownloadFromBrowsingView.as_view(), name='view_data_subset_as_xml'),
    path('workflows/<resource_id>/xml/', views.WorkflowXmlDownloadFromBrowsingView.as_view(), name='view_workflow_as_xml'),
    path('resources/2.2/<resource_type>/<resource_namespace>/<resource_id>/', views.metadata_xml_file_direct_download, name='xml_file_download')
]
