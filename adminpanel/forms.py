from typing import Any

from django.contrib.auth import authenticate
from django.forms import forms, ModelForm
from users.models import User
from product.models import Product, Promo_code


class Loginform(forms.Form):
    class Meta:
        model = User
        fields = ["email", "password"]

    def check_credentials(self, email, password) -> Any | None:
        user = authenticate(email=email, password=password)
        if user is not None:
            return user
        else:
            return None


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class AddpromoCodeForm(ModelForm):
    class Meta:
        model = Promo_code
        fields = "__all__"
