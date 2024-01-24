from django.urls import path

from . import views

app_name = 'present'
urlpatterns = [
    path('data-collections/<data_collection_id>/api/', views.interact_with_data_collection_through_api, name='interact_with_data_collection_through_api'),
    path('workflows/<workflow_id>/api/', views.interact_with_workflow_through_api, name='interact_with_workflow_through_api'),
]