from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here
class User(AbstractUser):
    address = models.CharField(max_length=50,default="")
    city = models.CharField(max_length=50,default="")
    postal_code = models.IntegerField(default=0)
    phone_number = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    email = models.EmailField( unique=True)
    REQUIRED_FIELDS = []

