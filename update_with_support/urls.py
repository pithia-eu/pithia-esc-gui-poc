from django.urls import path

from . import views

urlpatterns = [
    path('organisations/<resource_id>/update-with-wizard/', views.OrganisationUpdateWithEditorFormView.as_view(), name='organisation_with_editor'),
    path('individuals/<resource_id>/update-with-wizard/', views.IndividualUpdateWithEditorFormView.as_view(), name='individual_with_editor'),
    path('projects/<resource_id>/update-with-wizard/', views.ProjectUpdateWithEditorFormView.as_view(), name='project_with_editor'),
    path('platforms/<resource_id>/update-with-wizard/', views.PlatformUpdateWithEditorFormView.as_view(), name='platform_with_editor'),
    path('operations/<resource_id>/update-with-wizard/', views.OperationUpdateWithEditorFormView.as_view(), name='operation_with_editor'),
    path('instruments/<resource_id>/update-with-wizard/', views.InstrumentUpdateWithEditorFormView.as_view(), name='instrument_with_editor'),
    path('acquisition-capabilities/<resource_id>/update-with-wizard/', views.AcquisitionCapabilitiesUpdateWithEditorFormView.as_view(), name='acquisition_capability_set_with_editor'),
    path('acquisitions/<resource_id>/update-with-wizard/', views.AcquisitionUpdateWithEditorFormView.as_view(), name='acquisition_with_editor'),
    path('computation-capabilities/<resource_id>/update-with-wizard/', views.ComputationCapabilitiesUpdateWithEditorFormView.as_view(), name='computation_capability_set_with_editor'),
    path('computation/<resource_id>/update-with-wizard/', views.ComputationUpdateWithEditorFormView.as_view(), name='computation_with_editor'),
    path('process/<resource_id>/update-with-wizard/', views.ProcessUpdateWithEditorFormView.as_view(), name='process_with_editor'),
    path('data-collection/<resource_id>/update-with-wizard/', views.DataCollectionUpdateWithEditorFormView.as_view(), name='data_collection_with_editor'),
    path('catalogue/<resource_id>/update-with-wizard/', views.CatalogueUpdateWithEditorFormView.as_view(), name='catalogue_with_editor'),
    path('catalogue-entry/<resource_id>/update-with-wizard/', views.CatalogueEntryUpdateWithEditorFormView.as_view(), name='static_dataset_entry_with_editor'),
    path('data-subset/<resource_id>/update-with-wizard/', views.CatalogueDataSubsetUpdateWithEditorFormView.as_view(), name='data_subset_with_editor'),
    path('workflow/<resource_id>/update-with-wizard/', views.WorkflowUpdateWithEditorFormView.as_view(), name='workflow_with_editor'),
]