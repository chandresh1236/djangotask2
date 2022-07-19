from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True,primary_key=True)
    username = models.CharField(max_length=100, blank=False, null=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_connected = models.BooleanField(default=False)

    def __str__(self):
        return self.email