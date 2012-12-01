from django.db import models
from field import CoordinatesField

#from django_extensions.db.fields.encrypted import EncryptedCharField

class UserCredentials(models.Model):
    credentialsHash = models.CharField(max_length=255)

class PhoneNumber(models.Model):
    #phoneNumberHash = EncryptedCharField(max_length=255)
    phoneNumberHash = models.CharField(max_length=255)



class SuperMarket(models.Model):
    name = models.CharField(max_length=255)

class SuperMarketLocation(models.Model):
    supermarket = models.ForeignKey(SuperMarket)
    location = CoordinatesField()

