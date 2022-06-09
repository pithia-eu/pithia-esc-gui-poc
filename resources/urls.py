from django.urls import include, path

from . import views

app_name = 'resources'
urlpatterns = [
    path('', views.index, name='index'),
    path('organisations/', include('resources.namespace_urls', namespace='organisations'), ),
    path('individuals/', include('resources.namespace_urls', namespace='individuals'), ),
    path('projects/', include('resources.namespace_urls', namespace='projects'), ),
    path('platforms/', include('resources.namespace_urls', namespace='platforms'), ),
    path('instruments/', include('resources.namespace_urls', namespace='instruments'), ),
    path('operations/', include('resources.namespace_urls', namespace='operations'), ),
    path('acquisitions/', include('resources.namespace_urls', namespace='acquisitions'), ),
    path('computations/', include('resources.namespace_urls', namespace='computations'), ),
    path('processes/', include('resources.namespace_urls', namespace='processes'), ),
    path('data-collections/', include('resources.namespace_urls', namespace='data-collections'), ),
]
