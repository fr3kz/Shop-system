import django.utils.timezone
import stripe
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from sklep import settings
from .models import Product, Card, Opinion, Promo_code
from .forms import OpinionForm, AccountForm
from users.models import User


# Create your views here.
class MainView(View):
    products = Product.objects.all()
    fproducts = Product.objects.filter(is_featured=True)
    context = {
        'products': products,
        'fproducts': fproducts,
        'men_products': Product.objects.filter(category__title='Men'),
        'woman_products': Product.objects.filter(category__title='Women'),

    }

    def get(self, request):
        return render(request, 'product/main.html', context=self.context)


class ProductView(View):
    def get(self, request, product_id):  # product_id to zmienna z urls.py
        product = Product.objects.get(id=product_id)
        context = {
            'product': product,
            'opinions': product.opinion_set.all()
        }
        return render(request, 'product/product_detail.html', context=context)


class Review(View):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        form = OpinionForm(request.POST)

        if form.is_valid():
            opinion = Opinion.objects.create(description=form.data.get('description'), rated=form.data.get('rated'))
            opinion.product = product
            opinion.author = request.user
            opinion.save()
            return JsonResponse({'message': 'dodano opinie'})
        else:
            print(form.errors)
            return JsonResponse({'message': form.errors})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CardView(View):
    def get(self, request, item_id):
        return redirect('checkout')

    def post(self, request, item_id):
        # Sprawdzenie, czy klucz 'card' istnieje w sesji
        if 'card' in request.session:
            #Todo: sprawdzic czy dziala filter zamiast get
            card = Card.objects.filter(user=request.user)
            product = Product.objects.get(id=item_id)
            card.product.add(product)
            card.price += product.price
            card.save()
            request.session['card'] = card.id

            return redirect('checkout')
        else:
            card = Card.objects.create(user=request.user)
            product = Product.objects.get(id=item_id)
            card.product.add(product)
            card.price += product.price
            card.save()
            request.session['card'] = card.id

            return redirect('checkout')


# TODO: Edycja koszyka
class Checkout(View):
    def get(self, request):

        if 'card' in request.session:
            cardid = request.session['card']
            # Todo: sprawdzic co sie stanie jak w sesji bedzie zapisane id a nie bedzie w bazie
            card = Card.objects.get(id=cardid)
            total_price = card.price

            promo_code = Card.promo_code
            Promocode = None
            card_promocde = card.promo_code
            if card_promocde:
                Promocode = Promo_code.objects.get(code=card_promocde)

            context = {
                'card_id': cardid,
                'card_products': card.product.all(),
                'card_price': total_price,
                'card_promocode': card_promocde,
                'promocode': Promocode,
            }
            return render(request, 'product/checkout.html', context=context)
        else:
            return render(request, 'product/main.html')

    def post(self, request):
        promo_code = request.POST.get('promo_code')
        if promo_code:
            cardid = request.session['card']
            card = Card.objects.get(id=cardid)

            if card.promo_code:
                return HttpResponse('You have already used promo code', status=400)

            promo = Promo_code.objects.get(code=promo_code)

            if promo is not None:
                card.price *= (1 - (promo.discount / 100))
                card.promo_code = promo_code
                card.save()
                return redirect('checkout')
            else:
                return HttpResponse('Invalid promo code', status=400)


        else:
            return HttpResponse('Invalid promo code', status=400)


class UserOrders(View):
    def get(self, request):
        orders = Card.objects.filter(user=request.user)

        context = {
            'orders': orders
        }

        return render(request, 'product/user_orderview.html', context=context)


class UserAccount(View):
    def get(self, request):
        account = request.user
        form = AccountForm(instance=account)

        context = {
            'user': account,
            'form': form,
        }

        return render(request, 'product/user_profile.html', context=context)

    def post(self, request):
        account = request.user
        form = AccountForm(request.POST, instance=account)

        if form.is_valid():
            form.save()
            return redirect('my_account')
        else:
            print(form.errors)
            return redirect('my_account')


def Billing(request):
    card = Card.objects.get(id=request.session['card'])
    user = request.user
    card.first_name = request.POST.get('first_name')
    card.last_name = request.POST.get('last_name')
    card.email = request.POST.get('email')
    card.date = timezone.now()  # Użyj timezone.now() zamiast django.utils.timezone.now()
    card.phone_number = request.POST.get('phone_number')
    card.postal_code = request.POST.get('postal_code')
    card.city = request.POST.get('city')
    card.street = request.POST.get('street')
    card.user = user
    card.save()

    # Pobierz wszystkie produkty z karty
    products_on_card = card.product.all()

    line_items = []
    for product in products_on_card:
        line_items.append({
            'price_data': {
                'currency': 'pln',
                'product_data': {
                    'name': product.title,

                },
                'unit_amount': int(product.price * 100),
            },
            'quantity': 1,
        })

    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url="https://orca-app-tiz3h.ondigitalocean.app/success/",
        cancel_url="https://orca-app-tiz3h.ondigitalocean.app/cancel/",
    )

    # Zwróć ID sesji płatności jako odpowiedź
    curl = checkout_session.url
    return redirect(curl)


def live_search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(title__icontains=query)
    product_titles = list(products.values_list('title','id'))

    return JsonResponse({'results': product_titles})


def success(request):
    card = Card.objects.get(id=request.session['card'])
    card.make_order()

    del request.session['card']

    return redirect('afterpage')


def cancel(request):
    return redirect('checkout')

def AfterPage(request):
    return render(request, 'product/success.html')


#Todo: add implemetation to delete sessions card after x hours/days