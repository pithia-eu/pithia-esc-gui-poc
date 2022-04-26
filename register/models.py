from tkinter import CASCADE
from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=200)

class PithiaIdentifier(models.Model):
    localID = models.CharField(max_length=200)
    namespace = models.CharField(max_length=200)
    version = models.IntegerField()
    creationDate = models.DateTimeField()
    lastModificationDate = models.DateTimeField()

class ResourceIdentifier(models.Model):
    pithiaIdentifier = models.ForeignKey(PithiaIdentifier, on_delete=models.CASCADE)

class Resource(models.Model):
    identifier = models.ForeignKey(ResourceIdentifier, on_delete=models.CASCADE)
    upload_date = models.DateTimeField('date uploaded')
    uploader = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name
    
class Process(Resource):
    description = models.TextField()
    acquisitionComponent = models.ForeignKey()

class ObservationCollection(Resource):
    name = models.CharField(max_length=200)
    description = models.TextField()
    project = models.CharField(max_length=200)

class Parameter(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    observationCollection = models.ForeignKey(ObservationCollection, on_delete=models.CASCADE)

class RelatedParty(models.Model):
    role = models.CharField(max_length=200)
    party = models.ForeignKey('Organisation', on_delete=models.CASCADE)
    observationCollection = models.ForeignKey(ObservationCollection, on_delete=models.CASCADE)

class InstrumentModePair(models.Model):
    instrument = models.IntegerField()
    mode = models.IntegerField()

class Acquisition(Resource):
    description = models.CharField(max_length=200)
    instrument = models.IntegerField()
    instrumentModePair = models.ForeignKey(InstrumentModePair, null=True, on_delete=models.SET_NULL)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    platform = models.IntegerField()

class AcquisitionCapability(models.Model):
    name = models.CharField(max_length=200)
    observedProperty = models.CharField(max_length=200)
    dimensionalityInstance = models.CharField(max_length=200)
    units = models.CharField(max_length=200)
    computation = models.ForeignKey(Acquisition, on_delete=models.CASCADE)

class Computation(Resource):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    version = models.IntegerField()
    process = models.ForeignKey(Process, on_delete=models.CASCADE)

class ComputationType(models.Model):
    value = models.CharField(max_length=200)
    computation = models.ForeignKey(Computation, on_delete=models.CASCADE)

class ComputationCapability(models.Model):
    name = models.CharField(max_length=200)
    observedProperty = models.CharField(max_length=200)
    dimensionalityInstance = models.CharField(max_length=200)
    units = models.CharField(max_length=200)
    computation = models.ForeignKey(Computation, on_delete=models.CASCADE)