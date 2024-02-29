from django.contrib.auth.forms import UserCreationForm

from .models import User
from django.forms import forms, ModelForm


class LoginForm(forms.Form):
    class Meta:
        model = User
        fields = ['email', 'password']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_username(self):
        username = self.cleaned_data.get('email')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'
