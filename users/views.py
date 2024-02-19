from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegisterForm,CreateUserForm
from .models import User


# Create your views here.
class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'users/loginpage.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.data.get('email')
            password = form.data.get('password')

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_page')  # Redirect to the main page or any other desired URL
        else:
            print("not valid")
            print(form.errors)
        return render(request, 'users/loginpage.html', {'form': form})

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/registerpage.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Pobierz dane z formularza
            username = form.cleaned_data['email']  # lub inny sposób uzyskania nazwy użytkownika
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = RegisterForm.save(commit=False)
            user.username = email.toLowerCase()
            user.save()
            login(request, user)

            return redirect('main_page')
        else:
            print(form.errors)

        return render(request, 'users/registerpage.html', {'form': form})