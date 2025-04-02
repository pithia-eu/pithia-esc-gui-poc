from django.urls import include, path

from . import views

app_name = 'resource_management'
urlpatterns = [
    path('', views.index, name='index'),
    path('data-collection-related-metadata/', views.data_collection_related_metadata_index, name='data_collection_related_metadata_index'),
    path('static-dataset-related-metadata/', views.static_dataset_related_metadata_index, name='static_dataset_related_metadata_index'),
    path('organisations/', views.OrganisationManagementListView.as_view(), name='organisations'),
    path('individuals/', views.IndividualManagementListView.as_view(), name='individuals'),
    path('projects/', views.ProjectManagementListView.as_view(), name='projects'),
    path('platforms/', views.PlatformManagementListView.as_view(), name='platforms'),
    path('instruments/', views.InstrumentManagementListView.as_view(), name='instruments'),
    path('operations/', views.OperationManagementListView.as_view(), name='operations'),
    path('acquisition-capabilities/', views.AcquisitionCapabilitiesManagementListView.as_view(), name='acquisition_capability_sets'),
    path('acquisitions/', views.AcquisitionManagementListView.as_view(), name='acquisitions'),
    path('computation-capabilities/', views.ComputationCapabilitiesManagementListView.as_view(), name='computation_capability_sets'),
    path('computations/', views.ComputationManagementListView.as_view(), name='computations'),
    path('processes/', views.ProcessManagementListView.as_view(), name='processes'),
    path('data-collections/', views.DataCollectionManagementListView.as_view(), name='data_collections'),
    path('static-datasets/', views.StaticDatasetManagementListView.as_view(), name='static_datasets'),
    path('static-dataset-entries/', views.StaticDatasetEntryManagementListView.as_view(), name='static_dataset_entries'),
    path('data-subsets/', views.DataSubsetManagementListView.as_view(), name='data_subsets'),
    path('workflows/', views.WorkflowManagementListView.as_view(), name='workflows'),
]
