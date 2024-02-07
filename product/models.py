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
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, default="")
    discount = models.IntegerField(default=0)
 #   valid_date = models.DateField()

  #  def check_date(self):

   #     if self.valid_date > datetime.date.now():
    #        return False
   #     else:
     #       return True


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

    def __str__(self):
        return f"Zamowienie nr {self.id} - {self.user.last_name} "


    def get_total_price(self):
        # check for discount
        for product in self.product:
            if Discounts.objects.get(product=product).check_date():
                self.price += (product.price - (Discounts.objects.get(product=product).discount))
            else:
                self.price += product.price
        return self.price
