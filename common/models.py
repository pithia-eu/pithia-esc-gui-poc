from django.db import models

# Create your models here.
class ScientificMetadata(models.Model):
    registration_id = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=100)
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