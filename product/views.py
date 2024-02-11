from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core import serializers

from .models import Product, Card, Opinion, Promo_code
from .forms import OpinionForm


# Create your views here.
class MainView(View):
    products = Product.objects.all()
    fproducts = Product.objects.filter(is_featured=True)
    context = {
        'products': products,
        'fproducts': fproducts,

    }

    def get(self, request):
        return render(request, 'product/main.html', context=self.context)


class ProductView(View):
    def get(self, request, product_id):  # product_id zostaje jako argument URL
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


class CardView(View):

    def get(self, request, item_id):
        return redirect('checkout')

    def post(self, request, item_id):
        # Sprawdzenie, czy klucz 'card' istnieje w sesji
        if 'card'  in request.session:
            card = Card.objects.create(user=request.user)
            product = Product.objects.get(id=item_id)
            card.product.add(product)
            card.price += product.price
            card.save()
            request.session['card'] = card.id

            return redirect('checkout')
        else:
            cardid = request.session['card']
            product = Product.objects.get(id=item_id)
            card = Card.objects.get(id=cardid)
            card.product.add(product)
            card.save()
            request.session['card'] = card.id

            return redirect('checkout')


class Checkout(View):
    def get(self, request):

        if 'card' in request.session:
            cardid = request.session['card']
            #TODO: sprawdzenie czy to gowno dziala
            card = Card.objects.get_or_create(id=cardid)
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
