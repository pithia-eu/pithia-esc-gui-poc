from django.urls import path

from . import views

test = [
    path('<resource_collection_name>/', views.list_resource_namespaces, name='list_resource_namespaces'),
]

app_name = 'resources'
urlpatterns = [
    path('', views.list_resource_namespaces, name='list_resource_namespaces'),
    path('<namespace>/', views.list_resources_in_namespace, name='list_resources_in_namespace'),
]