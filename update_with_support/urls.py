from django.urls import path

from . import views

urlpatterns = [
    path('organisations/<resource_id>/update-with-wizard/', views.OrganisationUpdateWithEditorFormView.as_view(), name='organisation_with_editor'),
    path('individuals/<resource_id>/update-with-wizard/', views.IndividualUpdateWithEditorFormView.as_view(), name='individual_with_editor'),
    path('projects/<resource_id>/update-with-wizard/', views.ProjectUpdateWithEditorFormView.as_view(), name='project_with_editor'),
    path('platforms/<resource_id>/update-with-wizard/', views.PlatformUpdateWithEditorFormView.as_view(), name='platform_with_editor'),
    path('operations/<resource_id>/update-with-wizard/', views.OperationUpdateWithEditorFormView.as_view(), name='operation_with_editor'),
    path('instruments/<resource_id>/update-with-wizard/', views.InstrumentUpdateWithEditorFormView.as_view(), name='instrument_with_editor'),
    path('acquisition-capabilities/<resource_id>/update-with-wizard/', views.AcquisitionCapabilitiesUpdateWithEditorFormView.as_view(), name='acquisition_capabilities_with_editor'),
]