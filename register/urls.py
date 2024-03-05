from django.urls import path

from . import views

app_name = 'register'
urlpatterns = [
    path('organisation/', views.OrganisationRegisterFormView.as_view(), name='organisation'),
    path('individual/', views.IndividualRegisterFormView.as_view(), name='individual'),
    path('project/', views.ProjectRegisterFormView.as_view(), name='project'),
    path('platform/', views.PlatformRegisterFormView.as_view(), name='platform'),
    path('instrument/', views.InstrumentRegisterFormView.as_view(), name='instrument'),
    path('operation/', views.OperationRegisterFormView.as_view(), name='operation'),
    path('acquisition-capabilities/', views.AcquisitionCapabilitiesRegisterFormView.as_view(), name='acquisition_capability_set'),
    path('acquisition/', views.AcquisitionRegisterFormView.as_view(), name='acquisition'),
    path('computation-capabilities/', views.ComputationCapabilitiesRegisterFormView.as_view(), name='computation_capability_set'),
    path('computation/', views.ComputationRegisterFormView.as_view(), name='computation'),
    path('process/', views.ProcessRegisterFormView.as_view(), name='process'),
    path('data-collection/', views.DataCollectionRegisterFormView.as_view(), name='data_collection'),
    path('catalogue/', views.CatalogueRegisterFormView.as_view(), name='catalogue'),
    path('catalogue-entry/', views.CatalogueEntryRegisterFormView.as_view(), name='catalogue_entry'),
    path('catalogue-data-subset/', views.CatalogueDataSubsetRegisterFormView.as_view(), name='catalogue_data_subset'),
    path('workflow/', views.WorkflowRegisterFormView.as_view(), name='workflow'),
    path('organisation-wizard/', views.OrganisationRegisterWithoutFileFormView.as_view(), name='organisation_no_file'),
    path('individual-wizard/', views.IndividualRegisterWithoutFileFormView.as_view(), name='individual_no_file'),
]