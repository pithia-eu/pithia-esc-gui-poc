from django.db import models

# Create your models here.
class Resource(models.Model):
    name = models.CharField(max_length=200)
    upload_date = models.DateTimeField('date uploaded')
    def __str__(self):
        return self.name