import django
from django.db import models
from users.models import User
import datetime


class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to="images/")
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    amount = models.IntegerField(default=1)
    is_on = models.BooleanField(default=True, blank=True)
    stars = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    @staticmethod
    def set_off(self):
        self.is_on = False
        self.save()

    @staticmethod
    def set_on(self):
        self.is_on = True
        self.save()

class PerfumeOptions(models.Model):
    amount = models.IntegerField(default=1)  # in mililitres
    price = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='perfume_options', null=True, blank=True)
    title = models.CharField(max_length=50, default="")
    def __str__(self):
        return f"{self.amount} ml - {self.price} zł - {self.title}"

class Opinion(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, default="")
    description = models.TextField(default="")
    rated = models.IntegerField(default=0)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, default="")


class Discounts(models.Model):
    discount = models.IntegerField(default=0)


class CardItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default="", blank=True)
    quantity = models.IntegerField(default=1, blank=True)
    price = models.IntegerField(default=0, blank=True)
    card = models.ForeignKey(to='Card', on_delete=models.CASCADE, default="", blank=True)
    size = models.ManyToManyField(to=PerfumeOptions, default="", blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.product.title} - {self.quantity} szt. - {self.price} zł"

class Card(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default="", blank=True)
    quantity = models.IntegerField(default=1, blank=True)
    price = models.IntegerField(default=0)
    street = models.CharField(max_length=100, default="", blank=True)
    city = models.CharField(max_length=100, default="", blank=True)
    postal_code = models.CharField(max_length=6, default="", blank=True)
    phone_number = models.CharField(max_length=9, default="", blank=True)
    email = models.EmailField(default="", blank=True)
    first_name = models.CharField(max_length=50, default="", blank=True)
    last_name = models.CharField(max_length=50, default="", blank=True)
    promo_code = models.CharField(max_length=10, default="", blank=True)
    is_order = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_shipped = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Zamowienie nr {self.id} - {self.user.last_name} "

    def get_total_price(self, products):
        self.price = 0
        for product in products:
            self.price += product.price
        return self.price

    def make_order(self):
        self.is_order = True
        self.save()


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


class Category(models.Model):
    title = models.CharField(max_length=50, default="")
    products = models.ManyToManyField(to=Product, default="", blank=True)

    def __str__(self):
        return self.title


