from django.urls import path

from . import views

app_name = 'resources'
urlpatterns = [
    path('', views.index, name='index'),
    path('<resource_collection_name>/', views.list_resource_namespaces, name='list_resource_namespaces'),
    path('<resource_collection_name>/<namespace>/', views.list_resources_in_namespace, name='list_resources_in_namespace'),
    path('<resource_collection_name>/<namespace>/<local_id>/', views.detail, name='detail'),
]
