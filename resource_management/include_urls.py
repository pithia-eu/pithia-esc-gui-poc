from django.urls import include, path

from . import views

app_name = 'resource_management'
urlpatterns = [
    path('', views.list_resources_of_type, name='list_resources_of_type'),
    path('<resource_id>/', views.index, name='detail'),
]