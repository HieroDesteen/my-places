from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as m


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.email


class Types(models.Model):
    type = models.TextField(unique=True)


class Places(models.Model):
    PRICE_LEVEL_CHOICES = (
        (0, 'Free'),
        (1, 'Inexpensive'),
        (2, 'Moderate'),
        (3, 'Expensive'),
        (4, 'Very Expensive'),
        (5, 'Unknown price')
    )
    name = models.TextField()
    place_id = models.TextField(unique=True)
    price_level = models.SmallIntegerField(choices=PRICE_LEVEL_CHOICES, default=5)
    rating = models.FloatField(null=True, blank=True)
    vicinity = models.TextField(blank=True, null=True)
    formatted_address = models.TextField(blank=True, null=True)
    permanently_closed = models.BooleanField(blank=True, null=True)
    types = models.ManyToManyField(Types, blank=True)
