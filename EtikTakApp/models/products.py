# encoding: utf-8

from django.db import models
from EtikTakApp.models import supermarkets
from EtikTakApp.models import clients

class ProductCategory(models.Model):
    category = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s" % self.category

    class Meta:
        verbose_name = u"Produktkategori"
        verbose_name_plural = u"Produktkategorier"
        app_label = "EtikTakApp"

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_ean = models.CharField(max_length=100)
    product_category = models.ForeignKey(ProductCategory)

    def __unicode__(self):
        return u"%s | %s" % (self.product_name, self.product_ean)

    class Meta:
        verbose_name = u"Produkt"
        verbose_name_plural = u"Produkter"
        app_label = "EtikTakApp"

class ProductLocation(models.Model):
    product = models.ForeignKey(Product)
    supermarket_location = models.ForeignKey(supermarkets.SupermarketLocation)
    time_scanned = models.DateTimeField()
    client = models.ForeignKey(clients.ClientKey)

    def __unicode__(self):
        return u"%s" % self.supermarket_location

    class Meta:
        verbose_name = u"Produktlokation"
        verbose_name_plural = u"Produktlokationer"
        app_label = "EtikTakApp"

