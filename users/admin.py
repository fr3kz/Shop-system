from django.contrib import admin

from users.models import User
from users.forms import CreateUserForm


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    model = User
    add_form = CreateUserForm


admin.site.register(User, UserAdmin)
