import django
from django.db import models
from users.models import User
import datetime


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to="images/")
    description = models.TextField()
    is_featured = models.BooleanField(default=False)  # Dodane pole


class Opinion(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, default="")
    description = models.TextField(default="")
    rated = models.IntegerField(default=0)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, default="")


class Discounts(models.Model):
    discount = models.IntegerField(default=0)


class Card(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default="")
    product = models.ManyToManyField(to=Product, default="")
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    street = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    postal_code = models.CharField(max_length=6, default="")
    phone_number = models.CharField(max_length=9, default="")
    email = models.EmailField(default="")
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    promo_code = models.CharField(max_length=10, default="")

    def __str__(self):
        return f"Zamowienie nr {self.id} - {self.user.last_name} "

    def get_total_price(self, products):
        self.price = 0
        # check for discount
        for product in products:
            self.price += product.price

        return self.price


class Promo_code(models.Model):
    code = models.CharField(max_length=10, default="")
    discount = models.IntegerField(default=0)
    title = models.CharField(max_length=50, default="")
    max_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.code} - {self.discount}%"

    def check_using_limit(self):
        if self.max_count > 0:
            self.max_count -= 1
            self.save()
            return True
        else:
            return False
