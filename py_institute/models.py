from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class MyUsers(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    area_zip_code = models.CharField(max_length=255, blank=True, null=False)
    password = models.CharField(max_length=255, blank=True, null=True)
    last_logged_in = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.username.username


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    message = models.CharField(max_length=500, blank=True, null=True)
    terms = models.BooleanField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.email


class IP(models.Model):
    ip = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.ip


class UserDeviceInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    device_type = models.CharField(max_length=255, blank=True, null=False)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    ip_ref = models.ForeignKey(IP, on_delete=models.CASCADE, blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    lat_long = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    last_used = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.ip_ref)