from django.urls import path

from . import views

urlpatterns = [
    path('organisation-wizard/', views.OrganisationRegisterWithEditorFormView.as_view(), name='organisation_with_editor'),
    path('individual-wizard/', views.IndividualRegisterWithEditorFormView.as_view(), name='individual_with_editor'),
    path('project-wizard/', views.ProjectRegisterWithEditorFormView.as_view(), name='project_with_editor'),
    path('platform-wizard/', views.PlatformRegisterWithoutFormView.as_view(), name='platform_with_editor'),
    path('operation-wizard/', views.OperationRegisterWithoutFormView.as_view(), name='operation_with_editor'),
    path('instrument-wizard/', views.InstrumentRegisterWithoutFormView.as_view(), name='instrument_with_editor'),
    path('acquisition-capabilities-wizard/', views.AcquisitionCapabilitiesRegisterWithoutFormView.as_view(), name='acquisition_capability_set_with_editor'),
    path('acquisition-wizard/', views.AcquisitionRegisterWithoutFormView.as_view(), name='acquisition_with_editor'),
    path('computation-capabilities-wizard/', views.ComputationCapabilitiesRegisterWithoutFormView.as_view(), name='computation_capability_set_with_editor'),
    path('workflow-wizard/', views.WorkflowRegisterWithoutFormView.as_view(), name='workflow_with_editor'),
]