from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core import serializers

from .models import Product, Card, Opinion
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
        if 'card' not in request.session:
            card = Card.objects.create(user=request.user)
            product = Product.objects.get(id=item_id)
            card.product.add(product)
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

        # Dodawanie produktu do koszyka




class Checkout(View):
    def get(self, request):
        # Sprawdzenie, czy klucz 'card' istnieje w sesji
        if 'card' in request.session:
            cardid = request.session['card']
            card = Card.objects.get(id=cardid)
            card_id = card.id  # Przykładowy atrybut, który jest serializowalny do JSON
            user_id = card.user.id  # Inny przykładowy atrybut
            # Tutaj możesz przekazać inne atrybuty, które chcesz wyświetlić w kontekście szablonu
            context = {
                'card_id': card_id,
                'user_id': user_id,
            }
            return render(request, 'product/checkout.html', context=context)
        else:
            # Jeśli klucz 'card' nie istnieje, utwórz nowy obiekt Card
            card = Card.objects.create(user=request.user)
            request.session['card'] = card.id
            context = {
                'card_id': None,  # Możesz przekazać wartość None lub dowolną inną, która oznacza brak karty w sesji
            }
            return render(request, 'product/checkout.html', context=context)

