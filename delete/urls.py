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
    path('catalogues/<resource_id>/delete/', views.CatalogueDeleteView.as_view(), name='catalogue'),
    path('catalogue-entries/<resource_id>/delete/', views.CatalogueEntryDeleteView.as_view(), name='catalogue_entry'),
    path('catalogue-data-subsets/<resource_id>/delete/', views.CatalogueDataSubsetDeleteView.as_view(), name='catalogue_data_subset'),
    path('workflows/<resource_id>/delete/', views.WorkflowDeleteView.as_view(), name='workflow'),
]
