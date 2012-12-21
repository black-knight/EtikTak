# encoding: utf-8

import uuid
from EtikTakApp.util.util import *
from EtikTakApp.models.users import MobileNumber
from django.db import models

class Client(models.Model):
    uid = models.CharField(max_length=255)

    def create_client(self):
        client = Client(uid = uuid.uuid4())
        client.save()
        return client

    def __unicode__(self):
        return u"%s" % (self.uid)

    class Meta:
        verbose_name = u"Klient"
        verbose_name_plural = u"Klienter"
        app_label = "EtikTakApp"

class ClientKey(models.Model):
    uid = models.CharField(max_length=255) # EncryptedCharField(max_length=255)
    mobileNumberHashPasswordHashHashed = models.CharField(max_length=255) # EncryptedCharField(max_length=255)
    challengeHash = models.CharField(max_length=255) # EncryptedCharField(max_length=255)

    @staticmethod
    def create_client_key(mobileNumber, password):
        if MobileNumber.objects.exists(mobileNumber):
            raise ValueError("Mobile number %s already exists" % mobileNumber)
        clientkey = ClientKey(
            uid = uuid.uuid4(),
            mobileNumberHashPasswordHashHashed = sha256(sha256(mobileNumber) + sha256(password)))
        clientkey.save()
        return clientkey

    def __unicode__(self):
        return u"%s | %s | %s" % (self.uid, self.mobileNumberHashPasswordHashHashed, self.challengeHash)

    class Meta:
        verbose_name = u"Klientnøgle"
        verbose_name_plural = u"Klientnøgler"
        app_label = "EtikTakApp"

