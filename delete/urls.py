from django.urls import include, path

from . import views

app_name = 'delete'
urlpatterns = [
    path('organisations/<organisation_id>/delete/', views.organisation.as_view(), name='organisation'),
    path('individuals/<individual_id>/delete/', views.individual.as_view(), name='individual'),
    path('projects/<project_id>/delete/', views.project.as_view(), name='project'),
    path('platforms/<platform_id>/delete/', views.platform.as_view(), name='platform'),
    path('instruments/<instrument_id>/delete/', views.instrument.as_view(), name='instrument'),
    path('operations/<operation_id>/delete/', views.operation.as_view(), name='operation'),
    path('acquisitions/<acquisition_id>/delete/', views.acquisition.as_view(), name='acquisition'),
    path('computations/<computation_id>/delete/', views.computation.as_view(), name='computation'),
    path('processes/<process_id>/delete/', views.process.as_view(), name='process'),
    path('data-collections/<data_collection_id>/delete/', views.data_collection.as_view(), name='data_collection'),
]
