import uuid
import hashlib
from EtikTakApp.models.clients import *
from EtikTakApp.models.users import MobileNumber

def sha256(s):
    return hashlib.sha256(s).hexdigest()

def create_client():
    client = Client(uid = uuid.uuid4())
    client.save()
    return client

def create_client_key(mobileNumber, password):
    if mobile_number_exists(mobileNumber):
        raise ValueError("Mobile number %s exists already" % (mobileNumber))
    clientkey = ClientKey(
            uid = uuid.uuid4(),
            mobileNumberHashPasswordHashHashed = sha256(sha256(mobileNumber) + sha256(password)))
    clientkey.save()
    return clientkey

def mobile_number_exists(mobileNumber):
    return MobileNumber.objects.all().filter(mobileNumberHash = sha256(mobileNumber)).exists()

