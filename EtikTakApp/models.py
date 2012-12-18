from django.db import models
from django_google_maps import fields as map_fields

"""
Supermarket
"""

class Supermarket(models.Model):
    name = models.CharField(max_length=255)

class SupermarketLocation(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    supermarket = models.ForeignKey(Supermarket)



"""
Product
"""

class ProductCategory(models.Model):
    category = models.CharField(max_length=255)

class Product(models.Model):
    product_category = models.ForeignKey(ProductCategory)

class ProductLocation(models.Model):
    product = models.ForeignKey(Product)
    supermarket_location = models.ForeignKey(SupermarketLocation)



"""
User
"""

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)

class UserCredentials(models.Model):
    credentialsHash = models.CharField(max_length=255)

class PhoneNumber(models.Model):
    #phoneNumberHash = EncryptedCharField(max_length=255)
    phoneNumberHash = models.CharField(max_length=255)

