from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here
class User(AbstractUser):
    address = models.CharField(max_length=50,default="")
    phone_number = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    email = models.EmailField( unique=True)  # changes email to unique and blank to false
    REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS

