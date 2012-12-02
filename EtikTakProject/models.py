from django.db import models
from django_google_maps import fields as map_fields

#from django_extensions.db.fields.encrypted import EncryptedCharField

class UserCredentials(models.Model):
    credentialsHash = models.CharField(max_length=255)

class PhoneNumber(models.Model):
    #phoneNumberHash = EncryptedCharField(max_length=255)
    phoneNumberHash = models.CharField(max_length=255)



class SuperMarket(models.Model):
    name = models.CharField(max_length=255)

class SuperMarketLocation(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    supermarket = models.ForeignKey(SuperMarket)
