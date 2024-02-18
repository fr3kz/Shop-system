from django.forms import forms, ModelForm

from .models import Product, Opinion, Discounts
from users.models import User

class OpinionForm(forms.Form):
    class Meta:
        model = Opinion
        fields = ['description', 'rated']


class AccountForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'address', 'phone_number']

