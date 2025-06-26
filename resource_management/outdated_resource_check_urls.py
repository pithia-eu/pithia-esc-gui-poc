from django.urls import path

from . import views

app_name = 'checks'
urlpatterns = [
    path('organisations-check/', views.OutdatedOrganisationsCheckTemplateView.as_view(), name='organisations_check'),
    path('individuals-check/', views.OutdatedIndividualsCheckTemplateView.as_view(), name='individuals_check'),
    path('projects-check/', views.OutdatedProjectsCheckTemplateView.as_view(), name='projects_check'),
    path('platforms-check/', views.OutdatedPlatformsCheckTemplateView.as_view(), name='platforms_check'),
    path('operations-check/', views.OutdatedOperationsCheckTemplateView.as_view(), name='operations_check'),
    path('instruments-check/', views.OutdatedInstrumentsCheckTemplateView.as_view(), name='instruments_check'),
    path('acquisition-capabilities-check/', views.OutdatedAcquisitionCapabilitiesCheckTemplateView.as_view(), name='acquisition_capability_sets_check'),
    path('acquisitions-check/', views.OutdatedAcquisitionsCheckTemplateView.as_view(), name='acquisitions_check'),
    path('computation-capabilities-check/', views.OutdatedComputationCapabilitiesCheckTemplateView.as_view(), name='computation_capability_sets_check'),
    path('computations-check/', views.OutdatedComputationsCheckTemplateView.as_view(), name='computations_check'),
    path('processes-check/', views.OutdatedProcessesCheckTemplateView.as_view(), name='processes_check'),
    path('data-collections-check/', views.OutdatedDataCollectionsCheckTemplateView.as_view(), name='data_collections_check'),
    path('static-dataset-entries-check/', views.OutdatedStaticDatasetEntriesCheckTemplateView.as_view(), name='static_dataset_entries_check'),
    path('data-subsets-check/', views.OutdatedDataSubsetsCheckTemplateView.as_view(), name='data_subsets_check'),
    path('workflows-check/', views.OutdatedWorkflowsCheckTemplateView.as_view(), name='workflows_check'),
]
