from django.urls import path

from . import views

urlpatterns = [
    path('<data_collection_id>/delete/', views.delete_data_collection, name='delete_data_collection'),
    path('<data_collection_id>/update/', views.update_data_collection, name='update_data_collection'),
]
