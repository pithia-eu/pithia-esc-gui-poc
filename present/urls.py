from django.urls import path

from . import views

app_name = 'present'
urlpatterns = [
    path('', views.index, name='index'),
    path('api/<data_collection_id>/', views.interact_with_data_collection_through_api, name='interact_with_data_collection_through_api'),
]