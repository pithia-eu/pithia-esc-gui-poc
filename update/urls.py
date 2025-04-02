from django.urls import include, path

from . import views

app_name = 'update'
urlpatterns = [
    path('organisations/<resource_id>/update/', views.OrganisationUpdateFormView.as_view(), name='organisation'),
    path('individuals/<resource_id>/update/', views.IndividualUpdateFormView.as_view(), name='individual'),
    path('projects/<resource_id>/update/', views.ProjectUpdateFormView.as_view(), name='project'),
    path('platforms/<resource_id>/update/', views.PlatformUpdateFormView.as_view(), name='platform'),
    path('instruments/<resource_id>/update/', views.InstrumentUpdateFormView.as_view(), name='instrument'),
    path('operations/<resource_id>/update/', views.OperationUpdateFormView.as_view(), name='operation'),
    path('acquisition-capabilities/<resource_id>/update/', views.AcquisitionCapabilitiesUpdateFormView.as_view(), name='acquisition_capability_set'),
    path('acquisitions/<resource_id>/update/', views.AcquisitionUpdateFormView.as_view(), name='acquisition'),
    path('computation-capabilities/<resource_id>/update/', views.ComputationCapabilitiesUpdateFormView.as_view(), name='computation_capability_set'),
    path('computations/<resource_id>/update/', views.ComputationUpdateFormView.as_view(), name='computation'),
    path('processes/<resource_id>/update/', views.ProcessUpdateFormView.as_view(), name='process'),
    path('data-collections/<resource_id>/update/', views.DataCollectionUpdateFormView.as_view(), name='data_collection'),
    path('data-collections/<resource_id>/update/interaction-methods', views.data_collection_interaction_methods, name='data_collection_interaction_methods'),
    path('catalogues/<resource_id>/update', views.CatalogueUpdateFormView.as_view(), name='catalogue'),
    path('static-dataset-entries/<resource_id>/update', views.CatalogueEntryUpdateFormView.as_view(), name='static_dataset_entry'),
    path('data-subsets/<resource_id>/update', views.DataSubsetUpdateFormView.as_view(), name='data_subset'),
    path('workflows/<resource_id>/update', views.WorkflowUpdateFormView.as_view(), name='workflow'),
    path('workflows/<resource_id>/update/openapi-spec-url', views.workflow_openapi_specification_url, name='workflow_openapi_specification_url'),
    path('', include('update_with_support.urls')),
]
