from django.urls import include, path

from . import views

app_name = 'update'
urlpatterns = [
    path('organisations/<organisation_id>/update/', views.organisation.as_view(), name='organisation'),
    path('individuals/<individual_id>/update/', views.individual.as_view(), name='individual'),
    path('projects/<project_id>/update/', views.project.as_view(), name='project'),
    path('platforms/<platform_id>/update/', views.platform.as_view(), name='platform'),
    path('instruments/<instrument_id>/update/', views.instrument.as_view(), name='instrument'),
    path('operations/<operation_id>/update/', views.operation.as_view(), name='operation'),
    path('acquisition-capabilities/<acquisition_capability_id>/update/', views.acquisition_capability.as_view(), name='acquisition_capability'),
    path('acquisitions/<acquisition_id>/update/', views.acquisition.as_view(), name='acquisition'),
    path('computation-capabilities/<computation_capability_id>/update/', views.computation_capability.as_view(), name='computation_capability'),
    path('computations/<computation_id>/update/', views.computation.as_view(), name='computation'),
    path('processes/<process_id>/update/', views.process.as_view(), name='process'),
    path('data-collections/<data_collection_id>/update/', views.data_collection.as_view(), name='data_collection'),
    path('data-collections/<data_collection_id>/update/interaction-methods', views.data_collection_interaction_methods, name='data_collection_interaction_methods'),
    path('catalogues/<catalogue_id>/update', views.catalogue.as_view(), name='catalogue'),
    path('catalogues/<catalogue_entry_id>/update', views.catalogue_entry.as_view(), name='catalogue_entry'),
    path('catalogues/<catalogue_data_subset_id>/update', views.catalogue_data_subset.as_view(), name='catalogue_data_subset'),
]
