from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

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

    def get(self, request):
        card = request.session['card']
        context = {
            'card': card
        }

        return render(request, 'product/card.html', context=context)

    def post(self, item_id, request):
        if 'card' not in request.session:
            card = Card.objects.create(user=request.user)
            request.session['card'] = card
        else:
            card = request.session['card']
            product = Product.objects.get(id=item_id)
            card.product.add(product).save()

        return JsonResponse({'message': 'dodano'})
