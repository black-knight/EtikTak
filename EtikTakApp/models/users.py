# encoding: utf-8

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)

    def __unicode__(self):
        return u"%s | %s" % (self.username, self.email)

    class Meta:
        verbose_name = u"Bruger"
        verbose_name_plural = u"Brugere"
        app_label = "EtikTakApp"

class UserCredentials(models.Model):
    credentialsHash = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s" % (self.credentialsHash)

    class Meta:
        verbose_name = u"Bruger kodeord"
        verbose_name_plural = u"Bruger kodeord"
        app_label = "EtikTakApp"

class MobileNumber(models.Model):
    mobileNumberHash = models.CharField(max_length=255) # EncryptedCharField(max_length=255)

    def __unicode__(self):
        return u"%s" % (self.mobileNumberHash)

    class Meta:
        verbose_name = u"Mobilnummer"
        verbose_name_plural = u"Mobilnumre"
        app_label = "EtikTakApp"

