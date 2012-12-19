from django.db import models

class Client(models.Model):
    uid = models.CharField(max_length=255)

    class Meta:
        app_label = "EtikTakApp"

class ClientKey(models.Model):
    uid = models.CharField(max_length=255) # EncryptedCharField(max_length=255)
    phoneNumberHashPasswordHashHashed = models.CharField(max_length=255) # EncryptedCharField(max_length=255)
    challengeHash = models.CharField(max_length=255) # EncryptedCharField(max_length=255)

    class Meta:
        app_label = "EtikTakApp"

