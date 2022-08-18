from django.urls import include, path

app_name = 'resource_management'
urlpatterns = [
    path('manage/', include('resource_management.manage_urls')),
    path('organisations/', include('resource_management.organisation_urls')),
    path('individuals/', include('resource_management.individual_urls')),
    path('projects/', include('resource_management.project_urls')),
    path('platforms/', include('resource_management.platform_urls')),
    path('instruments/', include('resource_management.instrument_urls')),
    path('operations/', include('resource_management.operation_urls')),
    path('acquisitions/', include('resource_management.acquisition_urls')),
    path('computations/', include('resource_management.computation_urls')),
    path('processes/', include('resource_management.process_urls')),
    path('data-collections/', include('resource_management.data_collection_urls')),
]
