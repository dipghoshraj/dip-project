from django.db import models
from django.contrib.auth.models import User
from .models import CustomUser

class Token(models.Model):
    token = models.CharField(max_length=100)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
