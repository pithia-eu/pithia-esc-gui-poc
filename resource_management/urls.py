from django.urls import include, path

from . import views

app_name = 'resource_management'
urlpatterns = [
    path('resources/', views.index, name='index'),
    path('organisations/', views.organisations.as_view(), name='organisations'),
    path('individuals/', views.individuals.as_view(), name='individuals'),
    path('projects/', views.projects.as_view(), name='projects'),
    path('platforms/', views.platforms.as_view(), name='platforms'),
    path('instruments/', views.instruments.as_view(), name='instruments'),
    path('operations/', views.operations.as_view(), name='operations'),
    path('acquisitions/', views.acquisitions.as_view(), name='acquisitions'),
    path('computations/', views.computations.as_view(), name='computations'),
    path('processes/', views.processes.as_view(), name='processes'),
    path('data-collections/', views.data_collections.as_view(), name='data_collections'),
]
