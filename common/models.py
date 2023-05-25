from django.db import models

# Create your models here.
class ScientificMetadata(models.Model):
    registration_id = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=100)
    date_added = models.DateTimeField()
    date_modified = models.DateTimeField()
    # institution_id = models.ForeignKey()
    uploader_id = models.CharField(max_length=100)
    xml = models.TextField()
    json = models.JSONField()

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
    institution_id = models.ForeignKey()
    date_added = models.DateTimeField()
    date_modified = models.DateTimeField()
    json = models.JSONField()

class Institution(models.Model):
    institution_name = models.CharField(max_length=200)
    date_added = models.DateTimeField()
    date_modified = models.DateTimeField()