from django.urls import include, path

from . import views

app_name = 'browse'
urlpatterns = [
    path('', views.list_resources_of_type, name='list_resources_of_type'),
    path('<resource_id>/', views.detail, name='detail'),
]