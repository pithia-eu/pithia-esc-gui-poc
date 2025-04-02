from django.urls import path

from . import views

from datahub_management.views import (
    get_data_subset_online_resource_file,
    get_workflow_details_file,
)

app_name = 'browse'
urlpatterns = [
    path('browse-metadata/', views.index, name='index'),
    path('data-collection-related-metadata/', views.data_collection_related_resource_types, name='data_collection_related_resource_types'),
    path('catalogues/', views.catalogue_tree, name='catalogue_tree'),
    path('organisations/', views.OrganisationListView.as_view(), name='list_organisations'),
    path('individuals/', views.IndividualListView.as_view(), name='list_individuals'),
    path('projects/', views.ProjectListView.as_view(), name='list_projects'),
    path('platforms/', views.PlatformListView.as_view(), name='list_platforms'),
    path('instruments/', views.InstrumentListView.as_view(), name='list_instruments'),
    path('operations/', views.OperationListView.as_view(), name='list_operations'),
    path('acquisition-capabilities/', views.AcquisitionCapabilitiesListView.as_view(), name='list_acquisition_capability_sets'),
    path('acquisitions/', views.AcquisitionListView.as_view(), name='list_acquisitions'),
    path('computation-capabilities/', views.ComputationCapabilitiesListView.as_view(), name='list_computation_capability_sets'),
    path('computations/', views.ComputationListView.as_view(), name='list_computations'),
    path('processes/', views.ProcessListView.as_view(), name='list_processes'),
    path('data-collections/', views.DataCollectionListView.as_view(), name='list_data_collections'),
    path('workflows/', views.WorkflowListView.as_view(), name='list_workflows'),
    path('organisations/<organisation_id>/', views.OrganisationDetailView.as_view(), name='organisation_detail'),
    path('individuals/<individual_id>/', views.IndividualDetailView.as_view(), name='individual_detail'),
    path('projects/<project_id>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('platforms/<platform_id>/', views.PlatformDetailView.as_view(), name='platform_detail'),
    path('instruments/<instrument_id>/', views.InstrumentDetailView.as_view(), name='instrument_detail'),
    path('operations/<operation_id>/', views.OperationDetailView.as_view(), name='operation_detail'),
    path('acquisition-capabilities/<acquisition_capability_set_id>/', views.AcquisitionCapabilitiesDetailView.as_view(), name='acquisition_capability_set_detail'),
    path('acquisitions/<acquisition_id>/', views.AcquisitionDetailView.as_view(), name='acquisition_detail'),
    path('computation-capabilities/<computation_capability_set_id>/', views.ComputationCapabilitiesDetailView.as_view(), name='computation_capability_set_detail'),
    path('computations/<computation_id>/', views.ComputationDetailView.as_view(), name='computation_detail'),
    path('processes/<process_id>/', views.ProcessDetailView.as_view(), name='process_detail'),
    path('data-collections/<data_collection_id>/', views.DataCollectionDetailView.as_view(), name='data_collection_detail'),
    path('catalogues/<catalogue_id>/', views.StaticDatasetDetailView.as_view(), name='catalogue_detail'),
    path('static-dataset-entries/<static_dataset_entry_id>/', views.StaticDatasetEntryDetailView.as_view(), name='static_dataset_entry_detail'),
    path('data-subsets/<data_subset_id>/', views.DataSubsetDetailView.as_view(), name='data_subset_detail'),
    path('data-subsets/<data_subset_id>/online-resources/<online_resource_name>/', get_data_subset_online_resource_file, name='data_subset_online_resource_file'),
    path('workflows/<workflow_id>/', views.WorkflowDetailView.as_view(), name='workflow_detail'),
    path('workflows/<workflow_id>/details/', get_workflow_details_file, name='workflow_details_file'),
    path('utils/convert/urls/', views.get_esc_url_templates_for_ontology_server_urls_and_resource_server_urls, name='convert_server_urls'),
    path('utils/map/ontology-urls-to-properties/', views.map_ontology_server_urls_to_corresponding_properties, name='ontology_node_properties_mapping_url'),
]
