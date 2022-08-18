from django.urls import path

from . import views


urlpatterns = [
    path('resources/', views.index, name='index'),
    path('organisations/', views.list_acquisitions, name='list_organisations'),
    path('individuals/', views.list_individuals, name='list_individuals'),
    path('projects/', views.list_projects, name='list_projects'),
    path('platforms/', views.list_platforms, name='list_platforms'),
    path('instruments/', views.list_instruments, name='list_instruments'),
    path('operations/', views.list_operations, name='list_operations'),
    path('acquisitions/', views.list_acquisitions, name='list_acquisitions'),
    path('computations/', views.list_computations, name='list_computations'),
    path('processes/', views.list_processes, name='list_processes'),
    path('data-collections/', views.list_data_collections, name='list_data_collections'),
]
