from django.urls import include, path

from . import views

app_name = 'browse'
urlpatterns = [
    # path('browse/', views.index, name='index'),
    path('resources/', views.resources, name='resources'),
    path('ontology/', include('browse.ontology_urls')),
    path('organisations/', views.list_organisations.as_view(), name='list_organisations'),
    path('individuals/', views.list_individuals.as_view(), name='list_individuals'),
    path('projects/', views.list_projects.as_view(), name='list_projects'),
    path('platforms/', views.list_platforms.as_view(), name='list_platforms'),
    path('instruments/', views.list_instruments.as_view(), name='list_instruments'),
    path('operations/', views.list_operations.as_view(), name='list_operations'),
    path('acquisition-capabilities/', views.list_acquisition_capabilities.as_view(), name='list_acquisition_capabilities'),
    path('acquisitions/', views.list_acquisitions.as_view(), name='list_acquisitions'),
    path('computation-capabilities/', views.list_computation_capabilities.as_view(), name='list_computation_capabilities'),
    path('computations/', views.list_computations.as_view(), name='list_computations'),
    path('processes/', views.list_processes.as_view(), name='list_processes'),
    path('data-collections/', views.list_data_collections.as_view(), name='list_data_collections'),
    path('catalogues/', views.list_catalogues.as_view(), name='list_catalogues'),
    path('organisations/<organisation_id>/', views.organisation_detail.as_view(), name='organisation_detail'),
    path('individuals/<individual_id>/', views.individual_detail.as_view(), name='individual_detail'),
    path('projects/<project_id>/', views.project_detail.as_view(), name='project_detail'),
    path('platforms/<platform_id>/', views.platform_detail.as_view(), name='platform_detail'),
    path('instruments/<instrument_id>/', views.instrument_detail.as_view(), name='instrument_detail'),
    path('operations/<operation_id>/', views.operation_detail.as_view(), name='operation_detail'),
    path('acquisition-capabilities/<acquisition_capability_id>/', views.acquisition_capability_detail.as_view(), name='acquisition_capability_detail'),
    path('acquisitions/<acquisition_id>/', views.acquisition_detail.as_view(), name='acquisition_detail'),
    path('computation-capabilities/<computation_capability_id>/', views.computation_capability_detail.as_view(), name='computation_capability_detail'),
    path('computations/<computation_id>/', views.computation_detail.as_view(), name='computation_detail'),
    path('processes/<process_id>/', views.process_detail.as_view(), name='process_detail'),
    path('data-collections/<data_collection_id>/', views.data_collection_detail.as_view(), name='data_collection_detail'),
    path('catalogues/<catalogue_id>/', views.catalogue_detail.as_view(), name='catalogue_detail'),
]
