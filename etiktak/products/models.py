# encoding: utf-8

# Copyright (c) 2012, Daniel Andersen (dani_ande@yahoo.dk)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from etiktak.supermarkets import models as supermarkets
from etiktak.clients import models as clients

from django_google_maps import fields as map_fields
from django.db import models

class ProductCategory(models.Model):
    category = models.CharField(max_length=255, unique=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_product_category(category):
        """
        Creates and saves a product category with the specified
        category text.
        """
        product_category = ProductCategory(category = category)
        product_category.save()
        return product_category

    def __unicode__(self):
        return u"%s" % self.category

    class Meta:
        verbose_name = u"Produktkategori"
        verbose_name_plural = u"Produktkategorier"

class Product(models.Model):
    name = models.CharField(max_length=255)
    ean = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(ProductCategory)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_product(name, ean, category):
        """
        Creates and saves a product with the specified name,
        ean and category.
        """
        product = Product(name = name, ean = ean, category = category)
        product.save()
        return product

    def __unicode__(self):
        return u"%s | %s" % (self.product_name, self.product_ean)

    class Meta:
        verbose_name = u"Produkt"
        verbose_name_plural = u"Produkter"

class ProductLocation(models.Model):
    product = models.ForeignKey(Product)
    supermarket_location = models.ForeignKey(supermarkets.SupermarketLocation, default=None)
    scanned_location = map_fields.GeoLocationField(max_length=100)
    client = models.ForeignKey(clients.Client)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_product_location(product, scanned_location, client):
        """
        Creates and saves a product location for the specified product, scanned
        location and client and with created timestamp (=scanned timestamp) set to now.
        """
        location = ProductLocation(product = product, scanned_location = scanned_location, client = client)
        location.save()
        return location

    def __unicode__(self):
        return u"%s | %s" % (self.supermarket_location, self.scanned_location)

    class Meta:
        verbose_name = u"Produktlokation"
        verbose_name_plural = u"Produktlokationer"
