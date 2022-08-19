from django.urls import include, path

from . import views

app_name = 'delete'
urlpatterns = [
    path('organisations/<organisation_id>/delete/', views.organisation, name='organisation'),
    path('individuals/<individual_id>/delete/', views.individual, name='individual'),
    path('projects/<project_id>/delete/', views.project, name='project'),
    path('platforms/<platform_id>/delete/', views.platform, name='platform'),
    path('instruments/<instrument_id>/delete/', views.instrument, name='instrument'),
    path('operations/<operation_id>/delete/', views.operation, name='operation'),
    path('acquisitions/<acquisition_id>/delete/', views.acquisition, name='acquisition'),
    path('computations/<computation_id>/delete/', views.computation, name='computation'),
    path('processes/<process_id>/delete/', views.process, name='process'),
    path('data-collections/<data_collection_id>/delete/', views.data_collection, name='data_collection'),
]
