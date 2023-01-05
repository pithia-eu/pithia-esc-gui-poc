from django.urls import include, path

from . import views

app_name = 'browse'
urlpatterns = [
    # path('browse/', views.index, name='index'),
    path('resources/', views.resources, name='resources'),
    path('ontology/', include('browse.ontology_urls')),
    path('organisations/', views.OrganisationListView.as_view(), name='list_organisations'),
    path('individuals/', views.IndividualListView.as_view(), name='list_individuals'),
    path('projects/', views.ProjectListView.as_view(), name='list_projects'),
    path('platforms/', views.PlatformListView.as_view(), name='list_platforms'),
    path('instruments/', views.InstrumentListView.as_view(), name='list_instruments'),
    path('operations/', views.OperationListView.as_view(), name='list_operations'),
    path('acquisition-capabilities/', views.AcquisitionCapabilitiesListView.as_view(), name='list_acquisition_capability_sets'),
    path('acquisitions/', views.AcquisitionListView.as_view(), name='list_acquisitions'),
    path('computation-capabilities/', views.ComputationCapabilitiesListView.as_view(), name='list_computation_capability_sets'),
    path('computations/', views.ComputationListView.as_view(), name='list_computations'),
    path('processes/', views.ProcessListView.as_view(), name='list_processes'),
    path('data-collections/', views.DataCollectionListView.as_view(), name='list_data_collections'),
    path('organisations/<organisation_id>/', views.OrganisationDetailView.as_view(), name='organisation_detail'),
    path('individuals/<individual_id>/', views.IndividualDetailView.as_view(), name='individual_detail'),
    path('projects/<project_id>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('platforms/<platform_id>/', views.PlatformDetailView.as_view(), name='platform_detail'),
    path('instruments/<instrument_id>/', views.InstrumentDetailView.as_view(), name='instrument_detail'),
    path('operations/<operation_id>/', views.OperationDetailView.as_view(), name='operation_detail'),
    path('acquisition-capabilities/<acquisition_capability_set_id>/', views.AcquisitionCapabilitiesDetailView.as_view(), name='acquisition_capability_set_detail'),
    path('acquisitions/<acquisition_id>/', views.AcquisitionDetailView.as_view(), name='acquisition_detail'),
    path('computation-capabilities/<computation_capability_set_id>/', views.ComputationCapabilitiesDetailView.as_view(), name='computation_capability_set_detail'),
    path('computations/<computation_id>/', views.ComputationDetailView.as_view(), name='computation_detail'),
    path('processes/<process_id>/', views.ProcessDetailView.as_view(), name='process_detail'),
    path('data-collections/<data_collection_id>/', views.DataCollectionDetailView.as_view(), name='data_collection_detail'),
]
