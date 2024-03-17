from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from .forms import Loginform, AddProductForm, AddpromoCodeForm, PerfumeOptionsForm, DiscoversetForm
from product.models import Product, Promo_code, Card, Opinion, CardItem, PerfumeOptions, Category
from users.models import User
from utilities.models import ConstValue, ConstFile
from utilities.forms import ConstFileForm, ConstValueForm


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

        # show not shipped orders
        not_shipped_orders = Card.objects.filter(is_shipped=False, is_order=True)

        context = {
            'orders_count': orders_count,
            'users_count': users_count,
            'revenue': total_revenue,
            'products_in_stock': products_in_stock,
            'product_form': product_form,
            'promo_code_form': promo_code_form,
            'not_shipped_orders': not_shipped_orders,
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
        perfumeoption_form = PerfumeOptionsForm()
        context = {
            'form': product_form,
            'perfume_form': perfumeoption_form
        }
        return render(request, 'adminpanel/addproduct.html', context=context)

    def post(self, request):
        form = AddProductForm(request.POST, request.FILES)
        perfume_form = PerfumeOptionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminpanel')
        elif perfume_form.is_valid():
            perfume_form.save()
            return redirect('adminpanel')
        else:
            return render(request, 'adminpanel/addproduct.html', {'form': form})


class AddPromoCodeView(View):
    def get(self, request):
        promo_code_form = AddpromoCodeForm()
        context = {
            'form': promo_code_form
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
        orders = Card.objects.filter(is_order=True, is_delivered=False).all()
        context = {
            'orders': orders
        }
        return render(request, 'adminpanel/orders.html', context=context)


class StockView(View):
    def get(self, request):
        products = Product.objects.filter(is_perfume=True)
        featured_products = Product.objects.filter(is_featured=True, is_perfume=True)

        context = {
            'products': products,
            'featured_products': featured_products,
        }
        return render(request, 'adminpanel/stock.html', context=context)


class OpinionsView(View):
    def get(self, request):
        opinions = Opinion.objects.all()
        context = {
            'opinions': opinions
        }
        return render(request, 'adminpanel/opinions.html', context=context)


class ProductEditView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        products = Product.objects.filter().all()
        perfume_options = PerfumeOptions.objects.filter(product=product).all()
        form = AddProductForm(instance=product)
        perfume_form = PerfumeOptionsForm()

        categories = Category.objects.all()

        context = {
            'form': form,
            'product': product,
            'products': products,
            'perfume_form': perfume_form,
            'perfume_options': perfume_options,
            'categories': categories,
        }
        return render(request, 'adminpanel/editproduct.html', context=context)

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        form = AddProductForm(request.POST, request.FILES, instance=product)
        perfume_form = PerfumeOptionsForm(request.POST)

        if form.is_valid():
            pr = form.save(commit=False)
            pr.make_perfume(pr)
            pr.save()
            return redirect('stock')
        elif perfume_form.is_valid():
            perfume_form.save()
            return redirect('stock')
        else:
            return render(request, 'adminpanel/editproduct.html', {'form': form})


def set_off_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.set_off(self=product)
    return redirect('stock')


def set_on_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.set_on(self=product)
    return redirect('stock')


def mark_order_as_shipped(request, order_id):
    order = Card.objects.get(id=order_id)
    order.is_shipped = True
    order.save()
    return redirect('orders')


def mark_order_as_delivered(request, order_id):
    order = Card.objects.get(id=order_id)
    order.is_delivered = True
    order.save()
    return redirect('orders')


def delete_opinion(request, opinion_id):
    opinon = Opinion.objects.get(id=opinion_id)
    opinon.delete()
    return redirect('opinions')


class CardDetailsView(View):
    def get(self, request, card_id):
        card = Card.objects.get(id=card_id)
        card_items = CardItem.objects.filter(card=card).all()
        context = {
            'card': card,
            'card_items': card_items,
        }
        return render(request, 'adminpanel/orderdetail.html', context=context)


def add_perfume_options(request, product_id):
    product = Product.objects.get(id=product_id)
    form = PerfumeOptionsForm(request.POST)

    if form.is_valid():
        perfoption = form.save()
        perfoption.product = product
        perfoption.title = product.title
        perfoption.save()
        return redirect('stock')


class Utilities(View):
    def get(self, request):
        # 3 zdjecia z strony glownej
        img1 = ConstFile.objects.get(name="photo1")
        img2 = ConstFile.objects.get(name="photo2")
        img3 = ConstFile.objects.get(name="photo3")

        img1form = ConstFileForm(instance=img1)
        img2form = ConstFileForm(instance=img2)
        img3form = ConstFileForm(instance=img3)

        # ustawienia wysylki
        shiping_price = ConstValue.objects.get(name="shipping")
        shiping_free = ConstValue.objects.get(name="free_shipping")

        shiping_free_form = ConstValueForm(instance=shiping_free)
        shiping_price_form = ConstValueForm(instance=shiping_price)

        # zarzadzenia kuponami
        coupons = Promo_code.objects.all()

        context = {
            'img1': img1,
            'img2': img2,
            'img3': img3,
            'img1form': img1form,
            'img2form': img2form,
            'img3form': img3form,
            'shipping_price': shiping_price,
            'shipping_free': shiping_free,
            'shiping_free_form': shiping_free_form,
            'shiping_price_form': shiping_price_form,
            'coupons': coupons,
        }

        return render(request, "adminpanel/utilities.html", context=context)


def edit_photo(request, name):
    photo = ConstFile.objects.get(name=name)
    form = ConstFileForm(request.POST, request.FILES, instance=photo)
    print(request.POST)
    print(request.FILES)

    if form.is_valid():
        form.save()
        return redirect('utilities')
    else:
        return redirect('utilities')


def edit_shipping_price(request):
    item = ConstValue.objects.get(name="shipping")
    form = ConstValueForm(request.POST, instance=item)
    if form.is_valid():
        form.save()
        return redirect('utilities')
    else:
        return render(request, 'adminpanel/utilities.html', {'form': form})


def edit_shipping_free(request):
    item = ConstValue.objects.get(name="free_shipping")
    form = ConstValueForm(request.POST, instance=item)
    if form.is_valid():
        form.save()
        return redirect('utilities')
    else:
        return render(request, 'adminpanel/utilities.html', {'form': form})


def delete_coupon(request, coupon_id):
    item = Promo_code.objects.get(id=coupon_id)
    item.delete()
    return redirect('utilities')


class DiscoversetMainPage(View):
    def get(self, request):
        discover_sets = Product.objects.filter(is_discoverset=True, is_on=True)
        form = DiscoversetForm()

        context = {
            'discover_sets': discover_sets,
            'form': form,

        }

        return render(request, "adminpanel/discoversets.html", context=context)

    def post(self, request):
        form = DiscoversetForm(request.POST, request.FILES)

        if form.is_valid():

            product = form.save(commit=False)
            product.make_discoverset(product)
            product.save()

            category = Category.objects.get(title="Discoverset")
            category.products.add(product)
            category.save()

            return redirect('discover_sets')
        else:
            print(form.errors)
            return redirect('adminpanel')


class EditDiscoverSet(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product_options = PerfumeOptions.objects.filter(product__id=product_id)

        product_options_form = PerfumeOptionsForm()
        form = DiscoversetForm(instance=product)

        context = {
            'product': product,
            'perfume_form': product_options_form,
            'product_options': product_options,
            'form': form,
        }

        return render(request, 'adminpanel/editdiscoverset.html', context=context)

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)

        form = DiscoversetForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            product1 = form.save(commit=False)
            product1.make_discoverset(product1)
            product1.save()

            return redirect('editdiscover_set', product_id)
        else:
            context = {
                'errors': form.errors
            }
            return render(request, 'adminpanel/editdiscoverset.html', context=context)


def add_discoverset_options(request, product_id):
    product = Product.objects.get(id=product_id)
    form = PerfumeOptionsForm(request.POST)

    if form.is_valid():
        perfoption = form.save()
        perfoption.product = product
        perfoption.title = product.title
        perfoption.save()
        return redirect('discover_sets')


def add_perfume_to_category(request, product_id,category_id):
    product = Product.objects.get(id=product_id)
    category = Category.objects.get(id=category_id)
    category.products.add(product)
    category.save()
    return redirect('edit_product',product_id)


def remove_perfume_from_category(request, product_id,category_id):
    product = Product.objects.get(id=product_id)
    category = Category.objects.get(id=category_id)
    category.products.remove(product)
    category.save()
    return redirect('edit_product',product_id)

