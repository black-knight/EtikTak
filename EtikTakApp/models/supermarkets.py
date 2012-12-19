from django.db import models
from django_google_maps import fields as map_fields

class Supermarket(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = "EtikTakApp"

class SupermarketLocation(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    supermarket = models.ForeignKey(Supermarket)

    class Meta:
        app_label = "EtikTakApp"

