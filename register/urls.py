from django.urls import path

from . import views

app_name = 'register'
urlpatterns = [
    path('', views.index, name='index'),
    path('organisation/', views.organisation, name='organisation'),
    path('individual/', views.individual, name='individual'),
    path('project/', views.project, name='project'),
    path('platform/', views.platform, name='platform'),
    path('instrument/', views.instrument, name='instrument'),
    path('operation/', views.operation, name='operation'),
    path('acquisition/', views.acquisition, name='acquisition'),
    path('computation/', views.computation, name='computation'),
    path('process/', views.process, name='process'),
    path('data-collection/', views.data_collection, name='data_collection'),
]