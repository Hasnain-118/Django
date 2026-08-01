from pyexpat import model

from annotated_types import MaxLen
from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=35)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self) -> str:
        return self.name