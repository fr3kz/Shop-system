from django.urls import path
from .views import (MainView, ProductView, CardView, Checkout,Billing,success,cancel,live_search,UserOrders,UserAccount,AfterPage,
update_card                    )
urlpatterns = [
        path('',MainView.as_view(), name='main_page'),
        path('product/<int:product_id>/',ProductView.as_view(), name='product_detail'),
        path('add_to_card/<int:item_id>/',CardView.as_view(), name='add_to_card'),
        path('checkout/', Checkout.as_view(), name='checkout'),
        path('billing/',Billing,name="billing"),
        path('success/',success,name='success'),
        path('cancel/',cancel,name='cancel'),
        path('live-search/',live_search,name='live-search'),
        path('my_orders/',UserOrders.as_view(),name='my_orders'),
        path('my_account/', UserAccount.as_view(), name='my_account'),
        path('afterpage/',AfterPage ,name='afterpage'),
        path('update_card/<int:item_id>/',update_card,name='update_card')
]