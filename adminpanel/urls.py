from django.urls import path
from .views import (LoginView, AdminPanelView, AddProductView, AddPromoCodeView, OrdersView,StockView,OpinionsView
,set_off_product,ProductEditView)

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

]