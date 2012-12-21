# encoding: utf-8
from EtikTakApp.util import util
from EtikTakApp.managers.usermanager import *

from datetime import datetime
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    created_timestamp = models.DateTimeField()

    @staticmethod
    def create_user(username, email):
        """
        Creates and saves a username with the specified username and email.
        """
        user = User(username = username, email = email, created_timestamp = datetime.now())
        user.save()
        return user

    def __unicode__(self):
        return u"%s | %s" % (self.username, self.email)

    class Meta:
        verbose_name = u"Bruger"
        verbose_name_plural = u"Brugere"
        app_label = "EtikTakApp"

class UserCredentials(models.Model):
    credentials_hash = models.CharField(max_length=255)
    created_timestamp = models.DateTimeField()

    @staticmethod
    def create_user_credentials(password):
        """
        Creates and saves a hash of the specified password.
        """
        credentials = UserCredentials(credentials_hash = util.sha256(password), created_timestamp = datetime.now())
        credentials.save()
        return credentials

    def __unicode__(self):
        return u"%s" % self.credentials_hash

    class Meta:
        verbose_name = u"Bruger kodeord"
        verbose_name_plural = u"Bruger kodeord"
        app_label = "EtikTakApp"

class MobileNumber(models.Model):
    mobile_number_hash = models.CharField(max_length=255) # EncryptedCharField(max_length=255)
    created_timestamp = models.DateTimeField()

    objects = MobileNumberManager()

    @staticmethod
    def create_mobile_number(mobile_number):
        """
        Creates and saves the hash of the specified mobile number.
        """
        m = MobileNumber(mobile_number_hash = util.sha256(mobile_number), created_timestamp = datetime.now())
        m.save()
        return m

    def __unicode__(self):
        return u"%s" % self.mobile_number_hash

    class Meta:
        verbose_name = u"Mobilnummer"
        verbose_name_plural = u"Mobilnumre"
        app_label = "EtikTakApp"

