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
    path('acquisition-capability/', views.AcquisitionCapabilitiesRegisterFormView.as_view(), name='acquisition_capability_set'),
    path('acquisition/', views.AcquisitionRegisterFormView.as_view(), name='acquisition'),
    path('computation-capability/', views.ComputationCapabilitiesRegisterFormView.as_view(), name='computation_capability_set'),
    path('computation/', views.ComputationRegisterFormView.as_view(), name='computation'),
    path('process/', views.ProcessRegisterFormView.as_view(), name='process'),
    path('data-collection/', views.DataCollectionRegisterFormView.as_view(), name='data_collection'),
    path('catalogue/', views.catalogue.as_view(), name='catalogue'),
    path('catalogue-entry/', views.catalogue_entry.as_view(), name='catalogue_entry'),
    path('catalogue-data-subset/', views.catalogue_data_subset.as_view(), name='catalogue_data_subset'),
]