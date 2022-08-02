from django.urls import include, path

from . import views

app_name = 'resource_management'
urlpatterns = [
    path('', views.index, name='index'),
    path('organisations/', include('resource_management.include_urls', namespace='organisations')),
    path('individuals/', include('resource_management.include_urls', namespace='individuals')),
    path('projects/', include('resource_management.include_urls', namespace='projects')),
    path('platforms/', include('resource_management.include_urls', namespace='platforms')),
    path('instruments/', include('resource_management.include_urls', namespace='instruments')),
    path('operations/', include('resource_management.include_urls', namespace='operations')),
    path('acquisitions/', include('resource_management.include_urls', namespace='acquisitions')),
    path('computations/', include('resource_management.include_urls', namespace='computations')),
    path('processes/', include('resource_management.include_urls', namespace='processes')),
    path('data-collections/', include('resource_management.include_urls', namespace='data-collections')),
]
