from EtikTakApp.util.util import *
from django.db import models

class MobileNumberManager(models.Manager):
    def exists(self, mobileNumber):
        return self.filter(mobileNumberHash = sha256(mobileNumber)).exists()
