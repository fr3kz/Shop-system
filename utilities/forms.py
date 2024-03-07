from django.forms import ModelForm
from .models import ConstValue, ConstFile


class ConstFileForm(ModelForm):
    class Meta:
        model = ConstFile
        fields = ['name', 'file']


class ConstValueForm(ModelForm):
    class Meta:
        model = ConstValue
        fields = ['name', 'value']
