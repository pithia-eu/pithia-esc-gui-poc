from django.db import models

# Create your models here.
class PithiaResourceIdentifier(models.Model):
    localID = models.CharField(max_length=200)
    namespace = models.CharField(max_length=200)
    version = models.IntegerField()
    creationDate = models.DateTimeField()
    lastModificationDate = models.DateTimeField()

class ResourceIdentifier(models.Model):
    pithiaIdentifier = models.ForeignKey(PithiaResourceIdentifier, on_delete=models.CASCADE)

class Resource(models.Model):
    name = models.CharField(max_length=200)
    upload_date = models.DateTimeField('date uploaded')
    def __str__(self):
        return self.name