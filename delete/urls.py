from django.urls import include, path

from . import views

app_name = 'delete'
urlpatterns = [
    path('organisations/<resource_id>/delete/', views.OrganisationDeleteView.as_view(), name='organisation'),
    path('individuals/<resource_id>/delete/', views.IndividualDeleteView.as_view(), name='individual'),
    path('projects/<resource_id>/delete/', views.ProjectDeleteView.as_view(), name='project'),
    path('platforms/<resource_id>/delete/', views.PlatformDeleteView.as_view(), name='platform'),
    path('instruments/<resource_id>/delete/', views.InstrumentDeleteView.as_view(), name='instrument'),
    path('operations/<resource_id>/delete/', views.OperationDeleteView.as_view(), name='operation'),
    path('acquisition-capabilities/<resource_id>/delete/', views.AcquisitionCapabilitiesDeleteView.as_view(), name='acquisition_capability_set'),
    path('acquisitions/<resource_id>/delete/', views.AcquisitionDeleteView.as_view(), name='acquisition'),
    path('computation-capabilities/<resource_id>/delete/', views.ComputationCapabilitiesDeleteView.as_view(), name='computation_capability_set'),
    path('computations/<resource_id>/delete/', views.ComputationDeleteView.as_view(), name='computation'),
    path('processes/<resource_id>/delete/', views.ProcessDeleteView.as_view(), name='process'),
    path('data-collections/<resource_id>/delete/', views.DataCollectionDeleteView.as_view(), name='data_collection'),
    path('static-datasets/<resource_id>/delete/', views.StaticDatasetDeleteView.as_view(), name='catalogue'),
    path('static-dataset-entries/<resource_id>/delete/', views.StaticDatasetEntryDeleteView.as_view(), name='static_dataset_entry'),
    path('data-subsets/<resource_id>/delete/', views.DataSubsetDeleteView.as_view(), name='data_subset'),
    path('workflows/<resource_id>/delete/', views.WorkflowDeleteView.as_view(), name='workflow'),
]
