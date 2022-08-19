from django.urls import include, path

from . import views

app_name = 'update'
urlpatterns = [
    path('organisations/<organisation_id>/update/', views.organisation, name='organisation'),
    path('individuals/<individual_id>/update/', views.individual, name='individual'),
    path('projects/<project_id>/update/', views.project, name='project'),
    path('platforms/<platform_id>/update/', views.platform, name='platform'),
    path('instruments/<instrument_id>/update/', views.instrument, name='instrument'),
    path('operations/<operation_id>/update/', views.operation, name='operation'),
    path('acquisitions/<acquisition_id>/update/', views.acquisition, name='acquisition'),
    path('computations/<computation_id>/update/', views.computation, name='computation'),
    path('processes/<process_id>/update/', views.process, name='process'),
    path('data-collections/<data_collection_id>/update/', views.data_collection, name='data_collection'),
]
