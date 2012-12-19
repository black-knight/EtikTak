from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)

    class Meta:
        app_label = "EtikTakApp"

class UserCredentials(models.Model):
    credentialsHash = models.CharField(max_length=255)

    class Meta:
        app_label = "EtikTakApp"

class PhoneNumber(models.Model):
    phoneNumberHash = models.CharField(max_length=255) # EncryptedCharField(max_length=255)

    class Meta:
        app_label = "EtikTakApp"

