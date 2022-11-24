from django.urls import path

from . import views

app_name = 'utils'
urlpatterns = [
    path('utils/convert/urls', views.get_esc_url_templates_for_ontology_server_urls_and_resource_server_urls, name='convert_server_urls'),
]
