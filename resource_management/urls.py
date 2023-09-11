from django.urls import include, path

from . import views

app_name = 'resource_management'
urlpatterns = [
    path('', views.index, name='index'),
    path('guide', views.resource_registration_user_guide, name='guide'),
    path('data-collection-related-metadata/', views.data_collection_related_metadata_index, name='data_collection_related_metadata_index'),
    path('catalogue-related-metadata/', views.catalogue_related_metadata_index, name='catalogue_related_metadata_index'),
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
    path('catalogues/', views.CatalogueManagementListView.as_view(), name='catalogues'),
    path('catalogue-entries/', views.CatalogueEntryManagementListView.as_view(), name='catalogue_entries'),
    path('catalogue-data-subsets/', views.CatalogueDataSubsetManagementListView.as_view(), name='catalogue_data_subsets'),
]
