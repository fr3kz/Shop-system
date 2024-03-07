from django.db import models


# Create your models here.
class ConstValue(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=80,default="")

    def __str__(self):
        return self.name


class ConstFile(models.Model):
    name = models.CharField(max_length=50)
    file = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name


