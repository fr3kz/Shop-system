from django.urls import path
from .views import MainView, ProductView, CardView, Checkout,Billing,success,cancel
urlpatterns = [
        path('',MainView.as_view(), name='main_page'),
        path('product/<int:product_id>/',ProductView.as_view(), name='product_detail'),
        path('add_to_card/<int:item_id>/',CardView.as_view(), name='add_to_card'),
        path('checkout/', Checkout.as_view(), name='checkout'),
        path('billing/',Billing,name="billing"),
        path('success/',success,name='success'),
        path('cancel/',cancel,name='cancel'),

]