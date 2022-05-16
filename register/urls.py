from django.urls import path

from . import views

app_name = 'register'
urlpatterns = [
    path('', views.index, name='index'),
    path('<metadata_upload_type>/', views.metadata_upload, name='metadata_upload'),
    path('<metadata_upload_type>/validation/schema', views.validate_xml_file_by_type, name='xml_schema_validation'),
]