from django.urls import include, path

from . import views

app_name = 'resource_management'
urlpatterns = [
    path('', views.list_resources_of_type, name='list_resources_of_type'),
    path('update/<resource_id>/', views.update, name='update'),
    path('delete/<resource_id>/', views.delete, name='delete'),
]