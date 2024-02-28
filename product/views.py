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
from .models import Product, Card, Opinion, Promo_code, CardItem, PerfumeOptions
from .forms import OpinionForm, AccountForm
from users.models import User


# Create your views here.
class MainView(View):
    products = Product.objects.all()
    fproducts = Product.objects.filter(is_featured=True)
    context = {
        'products': products,
        'fproducts': fproducts,
        'men_products': Product.objects.filter(category__title='Men', is_on=True),
        'woman_products': Product.objects.filter(category__title='Women', is_on=True),

    }

    def get(self, request):
        return render(request, 'product/main.html', context=self.context)


class ProductView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        perfume_options = product.perfume_options.all()
        context = {
            'product': product,
            'opinions': product.opinion_set.all(),
            'product_options': perfume_options,
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
    def post(self, request, item_id):
        if 'card' in request.session:
            card = Card.objects.filter(user=request.user, is_order=False).first()
            product = Product.objects.get(id=item_id)

            # Uzyskaj wybraną opcję z żądania POST
            option_id = request.POST.get('option')
            option = PerfumeOptions.objects.get(id=option_id)


            ##Todo:sprawdzenie czy obiekt jest juz w koszyku
            product_item = CardItem.objects.create(card=card, product=product)
            product_item.size.add(option)  # Dodaj opcję do pola ManyToManyField

            card.price += option.price
            card.save()

            product_item.price = option.price

            product_item.save()
            request.session['card'] = card.id

            return redirect('checkout')
        else:
            card = Card.objects.create(user=request.user)
            product = Product.objects.get(id=item_id)

            # Uzyskaj wybraną opcję z żądania POST
            option_id = request.POST.get('option')
            option = PerfumeOptions.objects.get(id=option_id)

            product_item = CardItem.objects.create(card=card, product=product)
            product_item.size.add(option)  # Dodaj opcję do pola ManyToManyField

            card.price += option.price
            card.save()
            request.session['card'] = card.id
            product_item.price = option.price
            product_item.save()
            return redirect('checkout')


class Checkout(View):
    def get(self, request):

        if 'card' in request.session:
            cardid = request.session['card']
            card = Card.objects.get(id=cardid)
            total_price = card.price

            promo_code = Card.promo_code
            Promocode = None
            card_promocde = card.promo_code
            if card_promocde:
                Promocode = Promo_code.objects.get(code=card_promocde)


            product_items = CardItem.objects.filter(card=card).all()
            context = {
                'card_id': cardid,
                'card_products': product_items,
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


from django.shortcuts import redirect
from django.utils import timezone
from .models import CardItem

from django.db.models import Sum

def Billing(request):
    card = Card.objects.get(id=request.session['card'])
    user = request.user
    card.first_name = request.POST.get('first_name')
    card.last_name = request.POST.get('last_name')
    card.email = request.POST.get('email')
    card.date = timezone.now()
    card.phone_number = request.POST.get('phone_number')
    card.postal_code = request.POST.get('postal_code')
    card.city = request.POST.get('city')
    card.street = request.POST.get('street')
    card.user = user
    card.save()

    line_items = []

    # Pobierz wszystkie elementy koszyka
    cart_items = CardItem.objects.filter(card=card)

    # Zlicz ilość każdego produktu w koszyku
    product_quantities = cart_items.values('product__id','product__carditem__price').annotate(total_quantity=Sum('quantity'))

    for product_quantity in product_quantities:
        product_id = product_quantity['product__id']
        carditem = CardItem.objects.get(product__id=product_id, card=card, price=product_quantity['product__carditem__price'])
        total_quantity = product_quantity['total_quantity']

        # Pobierz produkt
        product = Product.objects.get(id=product_id)

        # Dodaj pozycję do listy zakupów
        line_items.append({
            'price_data': {
                'currency': 'pln',
                'product_data': {
                    'name': product.title,
                },
                'unit_amount': int(carditem.price * 100),
            },
            'quantity': total_quantity,
        })

    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card","blik","p24",],
        line_items=line_items,
        mode="payment",
        success_url="https://orca-app-tiz3h.ondigitalocean.app/success/",
        cancel_url="https://orca-app-tiz3h.ondigitalocean.app/cancel/",
    )

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

    card_items = CardItem.objects.filter(card=card).all()

    for card_item in card_items:
        product = Product.objects.get(id=card_item.product.id)
        product.amount -= card_item.quantity
        product.save()

    card_items = CardItem.objects.filter(card=card).all()
    context = {
        'card': card,
        'card_items': card_items,
    }
    del request.session['card']

    #return redirect('afterpage')
    return render(request, 'product/success.html',context=context)



def cancel(request):
    return redirect('checkout')

def AfterPage(request):
    return render(request, 'product/success.html')


def update_card(request, item_id):
    if request.method == 'POST':
        card = Card.objects.get(id=request.session['card'])

        product = Product.objects.get(id=item_id)

        card_item = CardItem.objects.get(card=card, product=product)

        new_quantity = int(request.POST.get(f'quantity_{item_id}', 1))

        card_item.quantity = new_quantity
        card_item.save()

        update_card_price(card)

        return redirect('checkout')
    else:
        return HttpResponse('Method not allowed', status=405)


def update_card_price(card):
    card_items = CardItem.objects.filter(card=card)

    total_price = card_items.get().price * card_items.get().quantity
    card.price = total_price
    card.save()



    #Todo: jak ktos bedzie probowasl dodac 2x to same perfumy to tylko zwiekszyc ilosc
    #Todo: ogarnac zeby moglby byc te same perfumy ale z rozna wielkoscia