from django.urls import path

from . import views

urlpatterns = [
    path('organisation-wizard/', views.OrganisationRegisterWithEditorFormView.as_view(), name='organisation_with_editor'),
    path('individual-wizard/', views.IndividualRegisterWithEditorFormView.as_view(), name='individual_with_editor'),
    path('project-wizard/', views.ProjectRegisterWithEditorFormView.as_view(), name='project_with_editor'),
    path('platform-wizard/', views.PlatformRegisterWithEditorFormView.as_view(), name='platform_with_editor'),
    path('operation-wizard/', views.OperationRegisterWithEditorFormView.as_view(), name='operation_with_editor'),
    path('instrument-wizard/', views.InstrumentRegisterWithEditorFormView.as_view(), name='instrument_with_editor'),
    path('acquisition-capabilities-wizard/', views.AcquisitionCapabilitiesRegisterWithEditorFormView.as_view(), name='acquisition_capability_set_with_editor'),
    path('acquisition-wizard/', views.AcquisitionRegisterWithEditorFormView.as_view(), name='acquisition_with_editor'),
    path('computation-capabilities-wizard/', views.ComputationCapabilitiesRegisterWithEditorFormView.as_view(), name='computation_capability_set_with_editor'),
    path('computation-wizard/', views.ComputationRegisterWithEditorFormView.as_view(), name='computation_with_editor'),
    path('process-wizard/', views.ProcessRegisterWithEditorFormView.as_view(), name='process_with_editor'),
    path('data-collection-wizard/', views.DataCollectionRegisterWithEditorFormView.as_view(), name='data_collection_with_editor'),
    path('catalogue-wizard/', views.CatalogueRegisterWithEditorFormView.as_view(), name='catalogue_with_editor'),
    path('workflow-wizard/', views.WorkflowRegisterWithEditorFormView.as_view(), name='workflow_with_editor'),
]