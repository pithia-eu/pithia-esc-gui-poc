from django.urls import include, path

from . import views

app_name = 'browse'
urlpatterns = [
    path('browse/', views.index, name='index'),
    path('resources/', views.resources, name='resources'),
    path('schemas/', views.schemas, name='schemas'),
    path('ontology/', include('browse.ontology_urls')),
    path('organisations/', views.list_organisations.as_view(), name='list_organisations'),
    path('individuals/', views.list_individuals.as_view(), name='list_individuals'),
    path('projects/', views.list_projects.as_view(), name='list_projects'),
    path('platforms/', views.list_platforms.as_view(), name='list_platforms'),
    path('instruments/', views.list_instruments.as_view(), name='list_instruments'),
    path('operations/', views.list_operations.as_view(), name='list_operations'),
    path('acquisitions/', views.list_acquisitions.as_view(), name='list_acquisitions'),
    path('computations/', views.list_computations.as_view(), name='list_computations'),
    path('processes/', views.list_processes.as_view(), name='list_processes'),
    path('data-collections/', views.list_data_collections.as_view(), name='list_data_collections'),
    path('organisations/<organisation_id>/', views.organisation_detail, name='organisation_detail'),
    path('individuals/<individual_id>/', views.individual_detail, name='individual_detail'),
    path('projects/<project_id>/', views.project_detail, name='project_detail'),
    path('platforms/<platform_id>/', views.platform_detail, name='platform_detail'),
    path('instruments/<instrument_id>/', views.instrument_detail, name='instrument_detail'),
    path('operations/<operation_id>/', views.operation_detail, name='operation_detail'),
    path('acquisitions/<acquisition_id>/', views.acquisition_detail, name='acquisition_detail'),
    path('computations/<computation_id>/', views.computation_detail, name='computation_detail'),
    path('processes/<process_id>/', views.process_detail, name='process_detail'),
    path('data-collections/<data_collection_id>/', views.data_collection_detail, name='data_collection_detail'),
]
