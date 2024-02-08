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
        return render(request, 'users/loginpage.html', {'form': form})
    def post(self, request):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return
        form.clean_username()
        user = User.objects.create_user(username=form.data.get('username'),
                                        password=form.data.get('password'),
                                        first_name=form.data.get('first_name'),
                                        last_name=form.data.get('last_name'),
                                        address=form.data.get('address'),
                                        phone_number=form.data.get('phone_number'))

        user = authenticate(username=user.username, password=user.password)
        if user is not None:
            login(request, user)
            return render(request, 'product/main.html')
        else:
            return render(request, 'users/loginpage.html', {'form': form})
