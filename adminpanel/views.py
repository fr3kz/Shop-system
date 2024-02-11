from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from .forms import Loginform, AddProductForm, AddpromoCodeForm
from product.models import Product, Promo_code, Card,Opinion
from users.models import User



class LoginView(View):
    def get(self, request):
        form = Loginform()
        return render(request, 'adminpanel/login.html', {'form': form})

    def post(self, request):
        form = Loginform(request.POST)
        if form.is_valid():
            user = form.login(request, form.data['email'], form.data['password'])
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
        product_form = AddProductForm()
        context = {
            'product_form': product_form,
        }
        return render(request, 'adminpanel/addproduct.html', context=context)

    def post(self, request):
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminpanel')
        else:
            return render(request, 'adminpanel/addproduct.html', {'form': form})


class AddPromoCodeView(View):
    def get(self, request):
        promo_code_form = AddpromoCodeForm()
        context = {
            'promo_code_form': promo_code_form
        }

        return render(request, 'adminpanel/addpromocode.html', context=context)

    def post(self, request):

        form = AddpromoCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminpanel')
        else:
            return render(request, 'adminpanel/addpromocode.html', {'form': form})


class OrdersView(View):
    def get(self, request):
        orders = Card.objects.all()
        context = {
            'orders': orders
        }
        return render(request, 'adminpanel/orders.html', context=context)


class StockView(View):
    def get(self, request):
        products = Product.objects.all()
        featured_products = Product.objects.filter(is_featured=True)

        context = {
            'products': products,
            'featured_products': featured_products,
        }
        return render(request, 'adminpanel/stock.html', context=context)



def set_off_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.set_off(self=product)
    return redirect('stock')

class OpinionsView(View):
    def get(self, request):
        opinions = Opinion.objects.all()
        context = {
            'opinions': opinions
        }
        return render(request, 'adminpanel/opinions.html', context=context)


class ProductEditView(View):
        def get(self,request, product_id):
            product = Product.objects.get(id=product_id)
            form = AddProductForm(instance=product)
            context = {
                'form': form
            }
            return render(request, 'adminpanel/editproduct.html', context=context)