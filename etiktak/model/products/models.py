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

from django.db import models
from django_google_maps import fields as map_fields

from etiktak.model.clients import models as clients
from etiktak.util import util, choices


class BARCODE_TYPES(choices.Choice):
    EAN13=(u'EAN13', u'EAN13')
    UPC=(u'UPC', u'UPC')

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
    barcode = models.CharField(max_length=100, unique=True)
    barcode_type = models.CharField(max_length=64, choices=BARCODE_TYPES)
    category = models.ForeignKey(ProductCategory)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_product(name, barcode, barcode_type, category):
        """
        Creates and saves a product with the specified name,
        barcode and category.
        """
        product = Product(name=name, barcode=barcode, barcode_type=barcode_type, category=category)
        product.save()
        return product

    def __unicode__(self):
        return u"%s | %s | %s" % (self.name, self.barcode_type, self.barcode)

    class Meta:
        verbose_name = u"Produkt"
        verbose_name_plural = u"Produkter"



CLUSTER_ALG_STATUS = util.enum(NOT_VISITED=0, VISITED=1, NOISE=2)

class ProductScanClusterStatus(models.Model):
    clustering = models.BooleanField(default=False)

class ProductScanCluster(models.Model):
    product = models.ForeignKey(Product)
    cluster_number = models.IntegerField()
    cluster_alg_status = models.IntegerField()

    @staticmethod
    def create_product_scan_cluster(product):
        """
        Creates and saves a product scan location cluster with initial cluster set to
        unknown.
        """
        scan = ProductScanCluster(product=product, cluster_alg_status=CLUSTER_ALG_STATUS.NOT_VISITED, cluster_number=-1)
        scan.save()
        return scan

    def __unicode__(self):
        return u"%s | %s" % (self.cluster_number, self.cluster_status)

    class Meta:
        verbose_name = u"Produktscanning"
        verbose_name_plural = u"Produktscanninger"



class ProductScan(models.Model):
    product = models.ForeignKey(Product)
    scanned_location = map_fields.GeoLocationField(max_length=100)
    scan_longitude = models.FloatField()
    scan_latitude = models.FloatField()
    client = models.ForeignKey(clients.Client)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_product_scan(product, client, scan_latitude, scan_longitude):
        """
        Creates and saves a product scan location for the specified product, scanned
        location and client and with created timestamp (=scanned timestamp) set to now.
        If client is not verified an exception is raised.
        """
        assert client.verified, "Client attempted to contribute though not verified"
        scan = ProductScan(product=product, client=client, scanned_location=scan_latitude + ", " + scan_longitude,
                           scan_latitude=scan_latitude, scan_longitude=scan_longitude)
        scan.save()
        ProductScanCluster.create_product_scan_cluster(product=product)
        return scan

    def __unicode__(self):
        return u"%s | %s" % (self.supermarket_location, self.scanned_location)

    class Meta:
        verbose_name = u"Produktscanning"
        verbose_name_plural = u"Produktscanninger"
