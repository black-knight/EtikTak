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

from etiktak.util import util

from datetime import datetime
from django.db import models

class MobileNumberManager(models.Manager):
    def exists(self, mobile_number):
        return self.filter(mobile_number_hash = util.sha256(mobile_number)).exists()

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
