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

import hashlib, random, os, base64, math
import keyring, keyring.backend, getpass
from util import cachedClassMethod


def hash(s):
    return hashlib.sha256(s).hexdigest()


def secure_random():
    return random.SystemRandom()


class Client:
    @staticmethod
    def mobileNumberHashPasswordHashHashed(mobile_number, password):
        return hash(hash(mobile_number) + hash(password))


class SMS:
    SMS_HANDLE_BYTES = 16
    SMS_CHALLENGE_DIGITS = 5

    @classmethod
    def generate_sms_challenge(cls):
        MIN_VALUE = math.pow(10, cls.SMS_CHALLENGE_DIGITS - 1)
        MAX_VALUE = (MIN_VALUE * 10) - 1
        return str(secure_random().randint(MIN_VALUE, MAX_VALUE))

    @classmethod
    def generate_sms_handle(cls):
        return base64.b64encode(os.urandom(cls.SMS_HANDLE_BYTES))


class EtikTakKeyring:
    KEYRING_PASSWORD_FILENAME = "keyring.pass"
    KEYRING_USERNAME = "etiktak"

    keyring_password = None
    password_cache = {}

    @classmethod
    def instantiate(cls):
        keyring.set_keyring(keyring.backend.CryptedFileKeyring())
        if cls.keyring_password is not None:
            return
        cls.load_keyring_password()
        if cls.keyring_password is None:
            cls.prompt_keyring_password()

    @classmethod
    @cachedClassMethod(dictionary=password_cache)
    def get_password(cls, service_name):
        return keyring.get_password(service_name, cls.KEYRING_USERNAME)

    @classmethod
    def load_keyring_password(cls):
        try:
            with open(cls.KEYRING_PASSWORD_FILENAME) as f:
                cls.keyring_password = f.readline()
        except:
            pass

    @classmethod
    def prompt_keyring_password(cls):
        cls.keyring_password = getpass.getpass("Enter keyring password: ")

    @classmethod
    def cached(cls, f):
        def check_cache(key):
            if key in cls.password_cache:
                return cls.password_cache[key]
            cls.password_cache[key] = f(key)
            return cls.password_cache[key]
        return check_cache
