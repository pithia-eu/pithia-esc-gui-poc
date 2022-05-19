from django.urls import path

from . import views

app_name = 'register'
urlpatterns = [
    path('', views.index, name='index'),
    path('<resource_type>/', views.resource_metadata_upload, name='resource_metadata_upload'),
    path('<resource_type>/validation/schema', views.validate_xml_file_by_resource_type, name='xml_schema_validation'),
]