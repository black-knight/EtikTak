# encoding: utf-8
from django.db import models

from django_google_maps import fields as map_fields
from datetime import datetime

class Supermarket(models.Model):
    name = models.CharField(max_length=255)
    created_timestamp = models.DateTimeField()

    @staticmethod
    def create_supermarket(name):
        """
        Creates and saves a supermarket with the specified name.
        """
        supermarket = Supermarket(name = name, created_timestamp = datetime.now())
        supermarket.save()
        return supermarket

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name = u"Supermarked"
        verbose_name_plural = u"Supermarkeder"
        app_label = "EtikTakApp"

class SupermarketLocation(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    supermarket = models.ForeignKey(Supermarket)
    created_timestamp = models.DateTimeField()

    @staticmethod
    def create_supermarket_location(address, geolocation, supermarket):
        """
        Creates and saves a supermarket location with the specified address, geolocation and
        supermarket.
        """
        location = SupermarketLocation(address = address, geolocation = geolocation, supermarket = supermarket, created_timestamp = datetime.now())
        location.save()
        return location

    def __unicode__(self):
        return u"%s | %s" % (self.address, self.geolocation)

    class Meta:
        verbose_name = u"Supermarkedslokation"
        verbose_name_plural = u"Supermarkedslokationer"
        app_label = "EtikTakApp"

