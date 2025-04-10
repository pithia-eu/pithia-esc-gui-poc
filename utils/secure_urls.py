from django.urls import path

from . import secure_views

app_name = 'utils_secure'
urlpatterns = [
    path('organisations/<resource_id>/xml/', secure_views.OrganisationXmlDownloadFromManagementView.as_view(), name='view_organisation_as_xml_with_editing'),
    path('individuals/<resource_id>/xml/', secure_views.IndividualXmlDownloadFromManagementView.as_view(), name='view_individual_as_xml_with_editing'),
    path('projects/<resource_id>/xml/', secure_views.ProjectXmlDownloadFromManagementView.as_view(), name='view_project_as_xml_with_editing'),
    path('platforms/<resource_id>/xml/', secure_views.PlatformXmlDownloadFromManagementView.as_view(), name='view_platform_as_xml_with_editing'),
    path('operations/<resource_id>/xml/', secure_views.OperationXmlDownloadFromManagementView.as_view(), name='view_operation_as_xml_with_editing'),
    path('instruments/<resource_id>/xml/', secure_views.InstrumentXmlDownloadFromManagementView.as_view(), name='view_instrument_as_xml_with_editing'),
    path('acquisition-capabilities/<resource_id>/xml/', secure_views.AcquisitionCapabilitiesXmlDownloadFromManagementView.as_view(), name='view_acquisition_capability_set_as_xml_with_editing'),
    path('acquisitions/<resource_id>/xml/', secure_views.AcquisitionXmlDownloadFromManagementView.as_view(), name='view_acquisition_as_xml_with_editing'),
    path('computation-capabilities/<resource_id>/xml/', secure_views.ComputationCapabilitiesXmlDownloadFromManagementView.as_view(), name='view_computation_capability_set_as_xml_with_editing'),
    path('computations/<resource_id>/xml/', secure_views.ComputationXmlDownloadFromManagementView.as_view(), name='view_computation_as_xml_with_editing'),
    path('process/<resource_id>/xml/', secure_views.ProcessXmlDownloadFromManagementView.as_view(), name='view_process_as_xml_with_editing'),
    path('data-collections/<resource_id>/xml/', secure_views.DataCollectionXmlDownloadFromManagementView.as_view(), name='view_data_collection_as_xml_with_editing'),
    path('static-dataset-entries/<resource_id>/xml/', secure_views.StaticDatasetEntryXmlDownloadFromManagementView.as_view(), name='view_static_dataset_entry_as_xml_with_editing'),
    path('data-subsets/<resource_id>/xml/', secure_views.DataSubsetXmlDownloadFromManagementView.as_view(), name='view_data_subset_as_xml_with_editing'),
    path('workflows/<resource_id>/xml/', secure_views.WorkflowXmlDownloadFromManagementView.as_view(), name='view_workflow_as_xml_with_editing'),
]
