from django.urls import path

from . import views

app_name = 'utils'
urlpatterns = [
    path('utils/convert/urls', views.get_esc_url_templates_for_ontology_server_urls_and_resource_server_urls, name='convert_server_urls'),
    path('organisations/<organisation_id>/xml', views.view_organisation_as_xml.as_view(), name='view_organisation_as_xml'),
    path('individuals/<individual_id>/xml', views.view_individual_as_xml.as_view(), name='view_individual_as_xml'),
    path('projects/<project_id>/xml', views.view_project_as_xml.as_view(), name='view_project_as_xml'),
    path('platforms/<platform_id>/xml', views.view_platform_as_xml.as_view(), name='view_platform_as_xml'),
    path('operations/<operation_id>/xml', views.view_operation_as_xml.as_view(), name='view_operation_as_xml'),
    path('instruments/<instrument_id>/xml', views.view_instrument_as_xml.as_view(), name='view_instrument_as_xml'),
    path('acquisition-capabilities/<acquisition_capability_id>/xml', views.view_acquisition_capability_as_xml.as_view(), name='view_acquisition_capability_as_xml'),
    path('acquisitions/<acquisition_id>/xml', views.view_acquisition_as_xml.as_view(), name='view_acquisition_as_xml'),
    path('computations/<computation_id>/xml', views.view_computation_as_xml.as_view(), name='view_computation_as_xml'),
    path('computation-capabilities/<computation_capability_id>/xml', views.view_computation_capability_as_xml.as_view(), name='view_computation_capability_as_xml'),
    path('processs/<process_id>/xml', views.view_process_as_xml.as_view(), name='view_process_as_xml'),
    path('data-collections/<data_collection_id>/xml', views.view_data_collection_as_xml.as_view(), name='view_data_collection_as_xml'),
]
