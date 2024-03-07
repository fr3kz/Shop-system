from django.contrib import admin
from .models import ConstValue, ConstFile
# Register your models here.
admin.site.register(ConstFile)
admin.site.register(ConstValue)