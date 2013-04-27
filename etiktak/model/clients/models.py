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

import uuid

from etiktak.util import security
from etiktak.model import choices

from django.db import models

class ClientManager(models.Manager):
    def get_by_password(self, mobile_number, password):
        clients = self.filter(mobile_number_hash_password_hash_hashed=security.Client.mobileNumberHashPasswordHashHashed(mobile_number, password))
        assert clients is not None and len(clients) == 1, "No unique client found for mobile number: %s" % mobile_number
        return clients[0]

    def get_by_uid(self, uid):
        clients = self.filter(uid=uid)
        assert clients is not None and len(clients) == 1, "No unique client found for uid: %s" % uid
        return clients[0]

    def verify(self, mobile_number, password):
        client = self.get_by_password(mobile_number, password)
        client.verified = True
        client.save()

class Client(models.Model):
    uid = models.CharField(max_length=255, unique=True) # EncryptedCharField(max_length=255)
    mobile_number_hash_password_hash_hashed = models.CharField(max_length=255, unique=True) # EncryptedCharField(max_length=255)
    verified = models.BooleanField(default=False)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    objects = ClientManager()

    @staticmethod
    def create_client_key(mobile_number, password):
        """
        Creates and saves a client key with autogenerated UID and with a hash of
        the sum of the specified mobile number hashed concatenated with the specified
        password hashed.
        """
        client_key = Client(
            uid=str(uuid.uuid4()),
            mobile_number_hash_password_hash_hashed=security.Client.mobileNumberHashPasswordHashHashed(mobile_number, password))
        client_key.save()
        return client_key

    def __unicode__(self):
        return u"%s | %s" % (self.uid, self.mobile_number_hash_password_hash_hashed)

    class Meta:
        verbose_name = u"Klientnøgle"
        verbose_name_plural = u"Klientnøgler"



# SMS verification entity keeps track of client verification. It consists of two parts; 1) the
# actual SMS verification, which the user has to verify by receiving a SMS, and 2) a "hidden"
# client challenge sent from the server to the client. Since the SMS verification challenge
# is inheritedly weak a client challenge is used to strengthen security, thus forcing an
# attacker to guess also a client challenge.

class SMS_STATUSES(choices.Choice):
    PENDING = (u'PENDING', u'Pending (being sent)')
    SENT = (u'SENT', u'Delivered')
    FAILED = (u'FAILED', u'Failed')
    VERIFIED = (u'VERIFIED', u'Verified')

    @staticmethod
    def CPSMS_status_to_enum(CPSMS_status):
        status_map = {"1": SMS_STATUSES.SENT,
                      "2": SMS_STATUSES.FAILED,
                      "4": SMS_STATUSES.PENDING,
                      "8": SMS_STATUSES.FAILED}
        assert CPSMS_status in status_map, "Invalid SMS status: %s" % CPSMS_status
        return status_map.get(CPSMS_status)

class SmsVerificationManager(models.Manager):
    def get(self, mobile_number):
        verifications = self.filter(mobile_number_hash=security.hash(mobile_number))
        assert verifications is not None and len(verifications) == 1, "No unique challenge found for mobile number: %s" % mobile_number
        return verifications[0]

    def verify_user(self, mobile_number, password, sms_challenge, client_challenge):
        verification = self.get(mobile_number)
        assert verification.status == SMS_STATUSES.SENT, "Provided challenge for mobile number %s in invalid state: %s" % (mobile_number, verification.status)
        assert verification.sms_challenge_hash == security.hash(sms_challenge), "Provided SMS challenge for mobile number %s doesn't match" % mobile_number
        assert verification.client_challenge == client_challenge, "Provided client challenge for mobile number %s doesn't match" % mobile_number
        verification.status = SMS_STATUSES.VERIFIED
        verification.save()
        Client.objects.verify(mobile_number, password)

    def update_sms_status(self, mobile_number, sms_handle, status):
        verification = self.get(mobile_number)
        assert verification.sms_handle == sms_handle, "Provided SMS handle (%s) for mobile number %s doesn't match actual handle: %s" % (sms_handle, mobile_number, verification.sms_handle)
        assert verification.status == SMS_STATUSES.PENDING, "Cannot update SMS verification with status %s due to wrong state: %s" % (status, verification.status)
        verification.status = status
        verification.save()

class SmsVerification(models.Model):
    mobile_number_hash = models.CharField(max_length=255, unique=True) # EncryptedCharField(max_length=255)
    sms_handle = models.CharField(max_length=255) # EncryptedCharField(max_length=255)
    sms_challenge_hash = models.CharField(max_length=255) # EncryptedCharField(max_length=255)
    client_challenge = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=SMS_STATUSES)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    objects = SmsVerificationManager()

    @staticmethod
    def create_challenge(mobile_number):
        """
        Creates and saves a SMS verification with autogenerated SMS challenge and client (UUID) challenge
        """
        SmsVerification.assert_challenge_not_already_exists(mobile_number)
        sms_verification = SmsVerification(
            sms_challenge_hash = security.hash(security.SMS.generate_sms_challenge()),
            client_challenge = str(uuid.uuid4()),
            status=SMS_STATUSES.PENDING,
            mobile_number_hash = security.hash(mobile_number),
            sms_handle = security.SMS.generate_sms_handle())
        sms_verification.save()
        return sms_verification

    @staticmethod
    def assert_challenge_not_already_exists(mobile_number):
        verifications = SmsVerification.objects.filter(mobile_number_hash=security.hash(mobile_number))
        assert verifications is None or len(verifications) == 0, "Challenge already exists for mobile number %s" % mobile_number

    def __unicode__(self):
        return u"%s | %s" % (self.sms_challenge_hash, self.mobile_number_hash)

    class Meta:
        verbose_name = u"SMS verifikation"
        verbose_name_plural = u"SMS verifikationer"



# Used to keep track of which mobile numbers are in use. Since client entity knows nothing about
# mobile number (without password) we need this entity. However, there is no direct relation between
# a client and its mobile number.

class MobileNumberManager(models.Manager):
    def exists(self, mobile_number):
        return self.filter(mobile_number_hash = security.hash(mobile_number)).exists()

class MobileNumber(models.Model):
    mobile_number_hash = models.CharField(max_length=255, unique=True) # EncryptedCharField(max_length=255)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    objects = MobileNumberManager()

    @staticmethod
    def create_mobile_number(mobile_number):
        """
        Creates and saves the hash of the specified mobile number.
        """
        assert not MobileNumber.objects.exists(mobile_number), "Mobile number %s already exists" % mobile_number
        m = MobileNumber(mobile_number_hash = security.hash(mobile_number))
        m.save()
        return m

    def __unicode__(self):
        return u"%s" % self.mobile_number_hash

    class Meta:
        verbose_name = u"Mobilnummer"
        verbose_name_plural = u"Mobilnumre"
