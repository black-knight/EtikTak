from EtikTakApp.util import util

from django.db import models

class MobileNumberManager(models.Manager):
    def exists(self, mobile_number):
        return self.filter(mobile_number_hash = util.sha256(mobile_number)).exists()
