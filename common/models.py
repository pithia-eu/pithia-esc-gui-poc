from django.db import models
from .managers import OrganisationManager

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

    @property
    def identifier(self):
        return self.json['identifier']

    @property
    def pithia_identifier(self):
        return self.identifier['PITHIA_Identifier']

    @property
    def namespace(self):
        return self.pithia_identifier['namespace']

    @property
    def localid(self):
        return self.pithia_identifier['localid']

    @property
    def _metadata_server_url_base(self):
        return 'https://metadata.pithia.eu/resources/2.2'

    @property
    def metadata_server_url(self):
        return f'{self._metadata_server_url_base}/{self.type_in_metadata_server_url}/{self.namespace}/{self.localid}'

class TechnicalMetadata(models.Model):
    API = 'api'
    MICADO = 'micado'
    DOWNLOAD = 'download'
    INTERACTION_METHOD_CHOICES = [
        (API, 'API'),
        (MICADO, 'MiCADO'),
        (DOWNLOAD, 'Download'),
    ]
    # data_collection_id = models.ForeignKey()
    interaction_method = models.CharField(
        choices=INTERACTION_METHOD_CHOICES,
        default=API,
        max_length=100
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

# Proxy models
class Organisation(ScientificMetadata):
    objects = OrganisationManager()

    class Meta:
        proxy = True

class Individual(ScientificMetadata):
    class Meta:
        proxy = True

class Project (ScientificMetadata):
    class Meta:
        proxy = True

class Platform(ScientificMetadata):
    class Meta:
        proxy = True

class Operation(ScientificMetadata):
    class Meta:
        proxy = True

class Instrument(ScientificMetadata):
    class Meta:
        proxy = True

class AcquisitionCapabilities(ScientificMetadata):
    class Meta:
        proxy = True

class Acquisition(ScientificMetadata):
    class Meta:
        proxy = True

class ComputationCapabilities(ScientificMetadata):
    class Meta:
        proxy = True

class Computation(ScientificMetadata):
    class Meta:
        proxy = True

class Process(ScientificMetadata):
    class Meta:
        proxy = True

class DataCollection(ScientificMetadata):
    class Meta:
        proxy = True

class Catalogue(ScientificMetadata):
    class Meta:
        proxy = True

class CatalogueEntry(ScientificMetadata):
    class Meta:
        proxy = True

class CatalogueDataSubset(ScientificMetadata):
    class Meta:
        proxy = True