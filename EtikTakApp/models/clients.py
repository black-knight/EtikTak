# encoding: utf-8

import hashlib
from django.db import models

class Client(models.Model):
    uid = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s" % (self.uid)

    class Meta:
        verbose_name = u"Klient"
        verbose_name_plural = u"Klienter"
        app_label = "EtikTakApp"

class ClientKey(models.Model):
    uid = models.CharField(max_length=255) # EncryptedCharField(max_length=255)
    phoneNumberHashPasswordHashHashed = models.CharField(max_length=255) # EncryptedCharField(max_length=255)
    challengeHash = models.CharField(max_length=255) # EncryptedCharField(max_length=255)

    def __unicode__(self):
        return u"%s | %s | %s" % (self.uid, self.phoneNumberHashPasswordHashHashed, self.challengeHash)

    class Meta:
        verbose_name = u"Klientnøgle"
        verbose_name_plural = u"Klientnøgler"
        app_label = "EtikTakApp"

