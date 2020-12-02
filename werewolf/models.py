from django.db import models

# Create your models here.

class Setting(models.Model):
    name = models.CharField(max_length=25)
    type = models.CharField(max_length=15)
    value = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.name
