from django.urls import include, path

from . import views

app_name = 'delete'
urlpatterns = [
    path('organisations/<organisation_id>/delete/', views.OrganisationDeleteView.as_view(), name='organisation'),
    path('individuals/<individual_id>/delete/', views.IndividualDeleteView.as_view(), name='individual'),
    path('projects/<project_id>/delete/', views.ProjectDeleteView.as_view(), name='project'),
    path('platforms/<platform_id>/delete/', views.PlatformDeleteView.as_view(), name='platform'),
    path('instruments/<instrument_id>/delete/', views.InstrumentDeleteView.as_view(), name='instrument'),
    path('operations/<operation_id>/delete/', views.OperationDeleteView.as_view(), name='operation'),
    path('acquisition-capabilities/<acquisition_capability_set_id>/delete/', views.AcquisitionCapabilitiesDeleteView.as_view(), name='acquisition_capability_set'),
    path('acquisitions/<acquisition_id>/delete/', views.AcquisitionDeleteView.as_view(), name='acquisition'),
    path('computation-capabilities/<computation_capability_set_id>/delete/', views.ComputationCapabilitiesDeleteView.as_view(), name='computation_capability_set'),
    path('computations/<computation_id>/delete/', views.ComputationDeleteView.as_view(), name='computation'),
    path('processes/<process_id>/delete/', views.ProcessDeleteView.as_view(), name='process'),
    path('data-collections/<data_collection_id>/delete/', views.DataCollectionDeleteView.as_view(), name='data_collection'),
    path('catalogues/<catalogue_id>/delete/', views.CatalogueDeleteView.as_view(), name='catalogue'),
    path('catalogue_entries/<catalogue_entry_id>/delete/', views.CatalogueEntryDeleteView.as_view(), name='catalogue_entry'),
    path('catalogue_data_subsets/<catalogue_data_subset_id>/delete/', views.CatalogueDataSubsetDeleteView.as_view(), name='catalogue_data_subset'),
]
