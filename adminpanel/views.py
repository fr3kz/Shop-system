from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from .forms import Loginform, AddProductForm, AddpromoCodeForm
from product.models import Product, Promo_code,Card
from users.models import User

# Create your views here.
class LoginView(View):
    def get(self, request):
        form = Loginform()
        return render(request, 'adminpanel/login.html', {'form': form})
    def post(self, request):
        form = Loginform(request.POST)
        if form.is_valid():
            user= form.login(request, form.data['email'], form.data['password'])
            if user is not None:
                login(request, user)
                return redirect('adminpanel')
            return render(request, 'adminpanel/login.html', {'form': form})
        else:
            return render(request, 'adminpanel/login.html', {'form': form})


class AdminPanelView(View):
    def get(self, request):
        orders_count = Card.objects.count()
        users_count = User.objects.count()
        total_revenue = sum(order.price for order in Card.objects.all())
        products_in_stock = sum(product.amount for product in Product.objects.all())


        product_form = AddProductForm()
        promo_code_form = AddpromoCodeForm()

        context = {
            'orders_count': orders_count,
            'users_count': users_count,
            'revenue': total_revenue,
            'products_in_stock': products_in_stock,
            'product_form': product_form,
            'promo_code_form': promo_code_form
        }
        return render(request, 'adminpanel/main.html', context=context)

    def post(self, request):
        product_form = AddProductForm(request.POST, request.FILES)
        promo_code_form = AddpromoCodeForm(request.POST)

        if product_form.is_valid():
            product_form.save()
            return redirect('adminpanel')

        if promo_code_form.is_valid():
            promo_code_form.save()
            return redirect('adminpanel')
        return render(request, 'adminpanel/main.html')


class AddProductView(View):
    def get(self, request):
        form = AddProductForm()
        return render(request, 'adminpanel/addproduct.html', {'form': form})
    def post(self, request):
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminpanel')
        else:
            return render(request, 'adminpanel/addproduct.html', {'form': form})


class AddPromoCodeView(View):
    def get(self, request):
        form = AddpromoCodeForm()
        return render(request, 'adminpanel/addpromocode.html', {'form': form})
    def post(self, request):

        form = AddpromoCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminpanel')
        else:
            return render(request, 'adminpanel/addpromocode.html', {'form': form})

