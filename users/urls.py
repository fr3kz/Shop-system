from django.urls import path
from .views import LoginView, RegisterView,user_logout
urlpatterns = [
    path('login/',LoginView.as_view(), name='login'),
    path('register/',RegisterView.as_view(), name='register'),
    path('logout/',user_logout, name='logout'),
]


