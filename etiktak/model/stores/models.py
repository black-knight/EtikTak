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

from etiktak.util import util as util


class Store(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_store(name):
        """
        Creates and saves a store with the specified name.
        """
        store = Store(name=name)
        store.save()
        return store

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name = u"Forretning"
        verbose_name_plural = u"Forretning"


class StoreInstanceManager(models.Manager):
    def get_stores(self, latitude, longitude, radius, max_nodes=10000000):
        stores = self.filter(latitude__gt=latitude - radius,
                             latitude__lt=latitude + radius,
                             longitude__gt=longitude - radius,
                             longitude__lt=longitude + radius)[0:max_nodes]
        return self.filter_stores_by_radius(latitude, longitude, radius, stores)

    def filter_stores_by_radius(self, latitude, longitude, radius, stores):
        if stores is None or len(stores) == 0:
            return []
        radius_stores = []
        for s in stores:
            if self.squared_distance_in_meters(latitude, longitude, s) <= radius*radius:
                radius_stores.append(s)
        return radius_stores

    def squared_distance_in_meters(self, latitude, longitude, store):
        latitude_delta_meters = util.latitude_to_meters(latitude) -\
                                util.latitude_to_meters(store.latitude)
        longitude_delta_meters = util.longitude_to_meters(longitude, latitude) -\
                                 util.longitude_to_meters(store.longitude, store.latitude)
        return latitude_delta_meters*latitude_delta_meters + longitude_delta_meters*longitude_delta_meters


class StoreInstance(models.Model):
    address = map_fields.AddressField(max_length=200)
    location = map_fields.GeoLocationField(max_length=100)
    latitude = models.FloatField(db_index=True)
    longitude = models.FloatField(db_index=True)
    store = models.ForeignKey(Store)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    objects = StoreInstanceManager()

    @staticmethod
    def create_store_instance(address, latitude, longitude, store):
        """
        Creates and saves a specific instance of a store with the specified address and geolocation.
        """
        location = StoreInstance(address=address,
                                 # location=latitude + ", " + longitude,
                                 latitude=latitude, longitude=longitude,
                                 store=store)
        location.save()
        return location

    def __unicode__(self):
        return u"%s | %s | %s | %s" % (self.address, self.latitude, self.longitude, self.store)

    class Meta:
        verbose_name = u"Forretningsinstans"
        verbose_name_plural = u"Forretningsinstanser"

