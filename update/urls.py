from django.urls import include, path

from . import views

app_name = 'update'
urlpatterns = [
    path('organisations/<organisation_id>/update/', views.OrganisationUpdateFormView.as_view(), name='organisation'),
    path('individuals/<individual_id>/update/', views.IndividualUpdateFormView.as_view(), name='individual'),
    path('projects/<project_id>/update/', views.ProjectUpdateFormView.as_view(), name='project'),
    path('platforms/<platform_id>/update/', views.PlatformUpdateFormView.as_view(), name='platform'),
    path('instruments/<instrument_id>/update/', views.InstrumentUpdateFormView.as_view(), name='instrument'),
    path('operations/<operation_id>/update/', views.OperationUpdateFormView.as_view(), name='operation'),
    path('acquisition-capabilities/<acquisition_capability_set_id>/update/', views.AcquisitionCapabilitiesUpdateFormView.as_view(), name='acquisition_capability_set'),
    path('acquisitions/<acquisition_id>/update/', views.AcquisitionUpdateFormView.as_view(), name='acquisition'),
    path('computation-capabilities/<computation_capability_set_id>/update/', views.ComputationCapabilitiesUpdateFormView.as_view(), name='computation_capability_set'),
    path('computations/<computation_id>/update/', views.ComputationUpdateFormView.as_view(), name='computation'),
    path('processes/<process_id>/update/', views.ProcessUpdateFormView.as_view(), name='process'),
    path('data-collections/<data_collection_id>/update/', views.DataCollectionUpdateFormView.as_view(), name='data_collection'),
    path('data-collections/<data_collection_id>/update/interaction-methods', views.data_collection_interaction_methods, name='data_collection_interaction_methods'),
]
