from django.urls import include, path

from . import views

app_name = 'browse'
urlpatterns = [
    path('browse/', views.index, name='index'),
    path('organisations/', include('browse.namespace_urls', namespace='organisations')),
    path('individuals/', include('browse.namespace_urls', namespace='individuals')),
    path('projects/', include('browse.namespace_urls', namespace='projects')),
    path('platforms/', include('browse.namespace_urls', namespace='platforms')),
    path('instruments/', include('browse.namespace_urls', namespace='instruments')),
    path('operations/', include('browse.namespace_urls', namespace='operations')),
    path('acquisitions/', include('browse.namespace_urls', namespace='acquisitions')),
    path('computations/', include('browse.namespace_urls', namespace='computations')),
    path('processes/', include('browse.namespace_urls', namespace='processes')),
    path('data-collections/', include('browse.namespace_urls', namespace='data-collections')),
]
