from django.db import models
from django.contrib.auth.models import AbstractUser


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
    place_id = models.TextField(blank=True, unique=True)
    price_level = models.SmallIntegerField(choices=PRICE_LEVEL_CHOICES, default=5)
    rating = models.FloatField(null=True, blank=True)
    vicinity = models.TextField(blank=True, null=True)
    formatted_address = models.TextField(blank=True, null=True)
    permanently_closed = models.BooleanField(blank=True, null=True)
    types = models.ManyToManyField(Types, blank=True)

    @staticmethod
    def places_by_residence(residence):
        places = []
        for place in Places.objects.filter(currentresidence__current_residence=residence):
            places.append(place.name)
        return places  # Пока возвращает только имена, так удобней


class CurrentResidence(models.Model):
    current_residence = models.TextField(unique=True)
    last_synchronized = models.DateTimeField(auto_now=True)
    places = models.ManyToManyField(Places, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    @staticmethod
    def create_residence(location, username):
        residence = CurrentResidence(current_residence=location, user=username)
        residence.save()
        return residence

    @staticmethod
    def residences_by_user(username):
        residences = []
        for residence in CurrentResidence.objects.filter(user__username=username):
            residences.append(residence.current_residence)
        return residences
