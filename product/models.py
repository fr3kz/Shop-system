from django.db import models
from users.models import User


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to="images/")
    description = models.TextField()


class Opinion(models.Model):
    author = models.OneToOneField(to=User, on_delete=models.CASCADE, default="")
    description = models.TextField()
    rated = models.IntegerField()
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, default="")
