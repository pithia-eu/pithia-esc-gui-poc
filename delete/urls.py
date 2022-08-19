from django.urls import include, path

from . import views

app_name = 'delete'
urlpatterns = [=
    path('organisations/<organisation_id>/delete/', views),
    path('individuals/<individual_id>/delete/', include('resource_management.individual_urls')),
    path('projects/<project_id>/delete/', include('resource_management.project_urls')),
    path('platforms/<platform_id>/delete/', include('resource_management.platform_urls')),
    path('instruments/<instrument_id>/delete/', include('resource_management.instrument_urls')),
    path('operations/<operation_id>/delete/', include('resource_management.operation_urls')),
    path('acquisitions/<acquisition_id>/delete/', include('resource_management.acquisition_urls')),
    path('computations/<computation_id>/delete/', include('resource_management.computation_urls')),
    path('processes/<process_id>/delete/', include('resource_management.process_urls')),
    path('data-collections/<data_collection_id>/delete/', include('resource_management.data_collection_urls')),
]
