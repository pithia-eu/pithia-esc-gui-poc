from django.urls import include, path

from . import views

app_name = 'browse'
urlpatterns = [
    path('', views.list_resource_namespaces, name='list_resource_namespaces'),
    path('<namespace>/', views.list_resources_in_namespace, name='list_resources_in_namespace'),
    path('<namespace>/<local_id>/', views.detail, name='detail'),
]