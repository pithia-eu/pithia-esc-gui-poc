from django.urls import path

from . import views

app_name = 'validation'
urlpatterns = [
    path('organisation/', views.OrganisationXmlMetadataFileValidationFormView.as_view(), name='organisation'),
    path('individual/', views.IndividualXmlMetadataFileValidationFormView.as_view(), name='individual'),
    path('project/', views.ProjectXmlMetadataFileValidationFormView.as_view(), name='project'),
    path('platform/', views.PlatformXmlMetadataFileValidationFormView.as_view(), name='platform'),
    path('instrument/', views.InstrumentXmlMetadataFileValidationFormView.as_view(), name='instrument'),
    path('operation/', views.OperationXmlMetadataFileValidationFormView.as_view(), name='operation'),
    path('acquisition-capabilities/', views.AcquisitionCapabilitiesXmlMetadataFileValidationFormView.as_view(), name='acquisition_capability_set'),
    path('acquisition/', views.AcquisitionXmlMetadataFileValidationFormView.as_view(), name='acquisition'),
    path('computation-capabilities/', views.ComputationCapabilitiesXmlMetadataFileValidationFormView.as_view(), name='computation_capability_set'),
    path('computation/', views.ComputationXmlMetadataFileValidationFormView.as_view(), name='computation'),
    path('process/', views.ProcessXmlMetadataFileValidationFormView.as_view(), name='process'),
    path('data-collection/', views.DataCollectionXmlMetadataFileValidationFormView.as_view(), name='data_collection'),
    path('catalogue/', views.CatalogueXmlMetadataFileValidationFormView.as_view(), name='catalogue'),
    path('catalogue-entry/', views.CatalogueEntryXmlMetadataFileValidationFormView.as_view(), name='catalogue_entry'),
    path('catalogue-data-subset/', views.CatalogueDataSubsetXmlMetadataFileValidationFormView.as_view(), name='catalogue_data_subset'),
    path('api-specification-url/', views.api_specification_url, name='api_specification_url'),
]