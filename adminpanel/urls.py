from django.urls import path
from .views import LoginView, AdminPanelView, AddProductView, AddPromoCodeView

urlpatterns = [
    path('login/', LoginView.as_view(), name='adminlogin'),
    path('',AdminPanelView.as_view(), name='adminpanel'),
    path('addproduct/', AddProductView.as_view(), name='addproduct'),
    path('addpromocode/', AddPromoCodeView.as_view(), name='addpromocode'),
]