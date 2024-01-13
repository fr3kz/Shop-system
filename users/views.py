from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views import View
from .forms import LoginForm, RegisterForm
from .models import User


# Create your views here.
class LoginView(View):

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'form': form})


class RegisterView(View):
    def post(self, request):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return
        form.clean_username()
        user = User.objects.create_user(username=form.cleaned_data.get('username'),
                                        password=form.cleaned_data.get('password'),
                                        first_name=form.cleaned_data.get('first_name'),
                                        last_name=form.cleaned_data.get('last_name'),
                                        address=form.cleaned_data.get('address'),
                                        phone_number=form.cleaned_data.get('phone_number'))

        user = authenticate(username=user.username, password=user.password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'form': form})
