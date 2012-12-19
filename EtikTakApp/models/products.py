from django.db import models
from EtikTakApp.models import supermarkets
from EtikTakApp.models import clients

class ProductCategory(models.Model):
    category = models.CharField(max_length=255)

    class Meta:
        app_label = "EtikTakApp"

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_ean = models.CharField(max_length=100)
    product_category = models.ForeignKey(ProductCategory)

    class Meta:
        app_label = "EtikTakApp"

class ProductLocation(models.Model):
    product = models.ForeignKey(Product)
    supermarket_location = models.ForeignKey(supermarkets.SupermarketLocation)
    time_scanned = models.DateTimeField()
    client = models.ForeignKey(clients.ClientKey)

    class Meta:
        app_label = "EtikTakApp"

