from django.urls import path

from . import views

app_name = 'present'
urlpatterns = [
    path('api/<data_collection_id>/', views.interact_with_data_collection_through_api, name='interact_with_data_collection_through_api'),
]