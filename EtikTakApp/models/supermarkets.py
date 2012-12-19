# encoding: utf-8

from django.db import models
from django_google_maps import fields as map_fields

class Supermarket(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name = u"Supermarked"
        verbose_name_plural = u"Supermarkeder"
        app_label = "EtikTakApp"

class SupermarketLocation(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    supermarket = models.ForeignKey(Supermarket)

    def __unicode__(self):
        return u"%s | %s" % (self.address, self.geolocation)

    class Meta:
        verbose_name = u"Supermarkedslokation"
        verbose_name_plural = u"Supermarkedslokationer"
        app_label = "EtikTakApp"

