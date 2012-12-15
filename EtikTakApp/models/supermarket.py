from django.db import models
from django_google_maps import fields as map_fields

class SuperMarket(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = "EtikTakApp"

class SuperMarketLocation(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    supermarket = models.ForeignKey(SuperMarket)

    class Meta:
        app_label = "EtikTakApp"
