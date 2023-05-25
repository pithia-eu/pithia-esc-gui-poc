from django.db import models

# Create your models here.
class ScientificMetadata(models.Model):
    ORGANISATION = 'organisation'
    INDIVIDUAL = 'individual'
    PROJECT = 'project'
    PLATFORM = 'platform'
    OPERATION = 'operation'
    INSTRUMENT = 'instrument'
    ACQUISITION_CAPABILITIES = 'acquisition_capabilities'
    ACQUISITION = 'acquisition'
    COMPUTATION_CAPABILITIES = 'computation_capabilities'
    COMPUTATION = 'computation'
    PROCESS = 'process'
    DATA_COLLECTION = 'data_collection'
    CATALOGUE = 'catalogue'
    CATALOGUE_ENTRY = 'catalogue_entry'
    CATALOGUE_DATA_SUBSET = 'catalogue_data_subset'
    RESOURCE_TYPE_CHOICES = [
        (ORGANISATION, 'Organisation'),
        (INDIVIDUAL, 'Individual'),
        (PROJECT, 'Project'),
        (PLATFORM, 'Platform'),
        (OPERATION, 'Operation'),
        (INSTRUMENT, 'Instrument'),
        (ACQUISITION_CAPABILITIES, 'Acquisition Capabilities'),
        (ACQUISITION, 'Acquisition'),
        (COMPUTATION_CAPABILITIES, 'Computation Capabilities'),
        (COMPUTATION, 'Computation'),
        (PROCESS, 'Process'),
        (DATA_COLLECTION, 'Data Collection'),
        (CATALOGUE, 'Catalogue'),
        (CATALOGUE_ENTRY, 'Catalogue Entry'),
        (CATALOGUE_DATA_SUBSET, 'Catalogue Data Subset'),
    ]
    registration_id = models.CharField(max_length=200)
    resource_type = models.CharField(
        max_length=100,
        choices=RESOURCE_TYPE_CHOICES
    )
    xml = models.TextField()
    json = models.JSONField()
    # institution_id = models.ForeignKey()
    # registrant_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TechnicalMetadata(models.Model):
    API = 'api'
    MICADO = 'micado'
    DOWNLOAD = 'download'
    INTERACTION_METHOD_CHOICES = [
        (API, 'API'),
        (MICADO, 'MiCADO'),
        (DOWNLOAD, 'Download'),
    ]
    data_collection_id = models.ForeignKey()
    interaction_method = models.CharField(
        choices=INTERACTION_METHOD_CHOICES,
        default=API
    )
    json = models.JSONField()
    # institution_id = models.ForeignKey()
    # registrant_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Institution(models.Model):
    institution_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)