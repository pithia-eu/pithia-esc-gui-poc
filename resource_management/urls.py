from django.urls import include, path

from . import views

app_name = 'resource_management'
urlpatterns = [
    path('', views.index, name='index'),
    path('data-collection-related-registrations/', views.data_collection_related_registrations_index, name='data_collection_related_registrations_index'),
    path('catalogue-related-registrations/', views.catalogue_related_registrations_index, name='catalogue_related_registrations_index'),
    path('organisations/', views.organisations.as_view(), name='organisations'),
    path('individuals/', views.individuals.as_view(), name='individuals'),
    path('projects/', views.projects.as_view(), name='projects'),
    path('platforms/', views.platforms.as_view(), name='platforms'),
    path('instruments/', views.instruments.as_view(), name='instruments'),
    path('operations/', views.operations.as_view(), name='operations'),
    path('acquisition-capabilities/', views.acquisition_capabilities.as_view(), name='acquisition_capabilities'),
    path('acquisitions/', views.acquisitions.as_view(), name='acquisitions'),
    path('computation-capabilities/', views.computation_capabilities.as_view(), name='computation_capabilities'),
    path('computations/', views.computations.as_view(), name='computations'),
    path('processes/', views.processes.as_view(), name='processes'),
    path('data-collections/', views.data_collections.as_view(), name='data_collections'),
    path('catalogues/', views.catalogues.as_view(), name='catalogues'),
    path('catalogue-entries/', views.catalogue_entries.as_view(), name='catalogue_entries'),
    path('catalogue-data-subsets/', views.catalogue_data_subsets.as_view(), name='catalogue_data_subsets'),
]
