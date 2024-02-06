from django.forms import forms

from .models import Product, Opinion, Discounts

class OpinionForm(forms.Form):
    class Meta:
        model = Opinion
        fields = ['description', 'rated']



