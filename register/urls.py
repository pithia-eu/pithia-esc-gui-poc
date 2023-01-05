from django.urls import path

from . import views

app_name = 'register'
urlpatterns = [
    path('organisation/', views.organisation.as_view(), name='organisation'),
    path('individual/', views.individual.as_view(), name='individual'),
    path('project/', views.project.as_view(), name='project'),
    path('platform/', views.platform.as_view(), name='platform'),
    path('instrument/', views.instrument.as_view(), name='instrument'),
    path('operation/', views.operation.as_view(), name='operation'),
    path('acquisition-capability/', views.acquisition_capability.as_view(), name='acquisition_capability'),
    path('acquisition/', views.acquisition.as_view(), name='acquisition'),
    path('computation-capability/', views.computation_capability.as_view(), name='computation_capability'),
    path('computation/', views.computation.as_view(), name='computation'),
    path('process/', views.process.as_view(), name='process'),
    path('data-collection/', views.data_collection.as_view(), name='data_collection'),
    path('catalogue/', views.catalogue.as_view(), name='catalogue'),
    path('catalogue-entry/', views.catalogue_entry.as_view(), name='catalogue_entry'),
    path('catalogue-data-subset/', views.catalogue_data_subset.as_view(), name='catalogue_data_subset'),
]