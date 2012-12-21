# encoding: utf-8

from EtikTakApp.models import supermarkets
from EtikTakApp.models import clients

from datetime import datetime
from django.db import models

class ProductCategory(models.Model):
    category = models.CharField(max_length=255)
    created_timestamp = models.DateTimeField()

    @staticmethod
    def create_product_category(category):
        """
        Creates and saves a product category with the specified
        category text.
        """
        product_category = ProductCategory(category = category, created_timestamp = datetime.now())
        product_category.save()
        return product_category

    def __unicode__(self):
        return u"%s" % self.category

    class Meta:
        verbose_name = u"Produktkategori"
        verbose_name_plural = u"Produktkategorier"
        app_label = "EtikTakApp"

class Product(models.Model):
    name = models.CharField(max_length=255)
    ean = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory)
    created_timestamp = models.DateTimeField()

    @staticmethod
    def create_product(name, ean, category):
        """
        Creates and saves a product with the specified name,
        ean and category.
        """
        product = Product(name = name, ean = ean, category = category, created_timestamp = datetime.now())
        product.save()
        return product

    def __unicode__(self):
        return u"%s | %s" % (self.product_name, self.product_ean)

    class Meta:
        verbose_name = u"Produkt"
        verbose_name_plural = u"Produkter"
        app_label = "EtikTakApp"

class ProductLocation(models.Model):
    product = models.ForeignKey(Product)
    supermarket_location = models.ForeignKey(supermarkets.SupermarketLocation)
    client = models.ForeignKey(clients.ClientKey)
    created_timestamp = models.DateTimeField()

    @staticmethod
    def create_product_location(product, supermarket_location, client):
        """
        Creates and saves a product location for the specified product, supermarket
        location and client and with created timestamp (=scanned timestamp) set to now.
        """
        location = ProductLocation(product = product, supermarket_location = supermarket_location, client = client, created_timestamp = datetime.now())
        location.save()
        return location

    def __unicode__(self):
        return u"%s" % self.supermarket_location

    class Meta:
        verbose_name = u"Produktlokation"
        verbose_name_plural = u"Produktlokationer"
        app_label = "EtikTakApp"

