from django.urls import path

from . import views

app_name = 'utils'
urlpatterns = [
    path('organisations/<resource_id>/xml/', views.OrganisationXmlDownloadView.as_view(), name='view_organisation_as_xml'),
    path('individuals/<resource_id>/xml/', views.IndividualXmlDownloadView.as_view(), name='view_individual_as_xml'),
    path('projects/<resource_id>/xml/', views.ProjectXmlDownloadView.as_view(), name='view_project_as_xml'),
    path('platforms/<resource_id>/xml/', views.PlatformXmlDownloadView.as_view(), name='view_platform_as_xml'),
    path('operations/<resource_id>/xml/', views.OperationXmlDownloadView.as_view(), name='view_operation_as_xml'),
    path('instruments/<resource_id>/xml/', views.InstrumentXmlDownloadView.as_view(), name='view_instrument_as_xml'),
    path('acquisition-capabilities/<resource_id>/xml/', views.AcquisitionCapabilitiesXmlDownloadView.as_view(), name='view_acquisition_capability_set_as_xml'),
    path('acquisitions/<resource_id>/xml/', views.AcquisitionXmlDownloadView.as_view(), name='view_acquisition_as_xml'),
    path('computation-capabilities/<resource_id>/xml/', views.ComputationCapabilitiesXmlDownloadView.as_view(), name='view_computation_capability_set_as_xml'),
    path('computations/<resource_id>/xml/', views.ComputationXmlDownloadView.as_view(), name='view_computation_as_xml'),
    path('process/<resource_id>/xml/', views.ProcessXmlDownloadView.as_view(), name='view_process_as_xml'),
    path('data-collections/<resource_id>/xml/', views.DataCollectionXmlDownloadView.as_view(), name='view_data_collection_as_xml'),
    path('catalogues/<resource_id>/xml/', views.CatalogueXmlDownloadView.as_view(), name='view_catalogue_as_xml'),
    path('catalogue-entries/<resource_id>/xml/', views.CatalogueEntryXmlDownloadView.as_view(), name='view_catalogue_entry_as_xml'),
    path('catalogue-data-subsets/<resource_id>/xml/', views.CatalogueDataSubsetXmlDownloadView.as_view(), name='view_catalogue_data_subset_as_xml'),
    path('workflows/<resource_id>/xml/', views.WorkflowXmlDownloadView.as_view(), name='view_workflow_as_xml'),
]
