from django.urls import path
from .views import (LoginView, AdminPanelView, AddProductView, AddPromoCodeView, OrdersView,StockView,OpinionsView
,set_off_product,ProductEditView,mark_order_as_shipped,mark_order_as_delivered,delete_opinion)

urlpatterns = [
    path('login/', LoginView.as_view(), name='adminlogin'),
    path('',AdminPanelView.as_view(), name='adminpanel'),
    path('addproduct/', AddProductView.as_view(), name='addproduct'),
    path('addpromocode/', AddPromoCodeView.as_view(), name='addpromocode'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('stock/', StockView.as_view(), name='stock'),
    path('opinions/', OpinionsView.as_view(), name='opinions'),
    path('setoff_product/<int:product_id>/', set_off_product, name='setoff_product'),
    path('edit_product/<int:product_id>/', ProductEditView.as_view(), name='edit_product'),
    path('mark_order_as_shipped/<int:order_id>/', mark_order_as_shipped, name='mark_order_as_shipped'),
    path('mark_order_as_delivered/<int:order_id>/', mark_order_as_delivered, name='mark_order_as_delivered'),
    path('delete_opinion/<int:opinion_id>/', delete_opinion, name='delete_opinion'),

]