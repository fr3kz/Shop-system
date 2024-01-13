from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here
class User(AbstractUser):
    address = models.CharField(max_length=50,default="")
    phone_number = models.IntegerField(default=0)
