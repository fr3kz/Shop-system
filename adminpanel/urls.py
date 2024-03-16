from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (AdminPanelView, AddProductView, AddPromoCodeView, OrdersView, StockView, OpinionsView,
                    set_off_product, ProductEditView, mark_order_as_shipped, mark_order_as_delivered, delete_opinion,
                    CardDetailsView,add_perfume_options,set_on_product,Utilities,edit_shipping_price,edit_shipping_free,edit_photo,delete_coupon,DiscoversetMainPage,
                    EditDiscoverSet,add_discoverset_options)


def staff_member_required(user):
    return user.is_authenticated and user.is_staff

urlpatterns = [
    path('login/', LoginView.as_view(), name='adminlogin'),
    path('', user_passes_test(staff_member_required, login_url='/login/')(AdminPanelView.as_view()), name='adminpanel'),
    path('addproduct/', user_passes_test(staff_member_required, login_url='/login/')(AddProductView.as_view()), name='addproduct'),
    path('addpromocode/', user_passes_test(staff_member_required, login_url='/login/')(AddPromoCodeView.as_view()), name='addpromocode'),
    path('orders/', user_passes_test(staff_member_required, login_url='/login/')(OrdersView.as_view()), name='orders'),
    path('stock/', user_passes_test(staff_member_required, login_url='/login/')(StockView.as_view()), name='stock'),
    path('opinions/', user_passes_test(staff_member_required, login_url='/login/')(OpinionsView.as_view()), name='opinions'),
    path('setoff_product/<int:product_id>/', user_passes_test(staff_member_required, login_url='/login/')(set_off_product), name='setoff_product'),
    path('seton_product/<int:product_id>/', user_passes_test(staff_member_required, login_url='/login/')(set_on_product), name='seton_product'),
    path('edit_product/<int:product_id>/', user_passes_test(staff_member_required, login_url='/login/')(ProductEditView.as_view()), name='edit_product'),
    path('mark_order_as_shipped/<int:order_id>/', user_passes_test(staff_member_required, login_url='/login/')(mark_order_as_shipped), name='mark_order_as_shipped'),
    path('mark_order_as_delivered/<int:order_id>/', user_passes_test(staff_member_required, login_url='/login/')(mark_order_as_delivered), name='mark_order_as_delivered'),
    path('delete_opinion/<int:opinion_id>/', user_passes_test(staff_member_required, login_url='/login/')(delete_opinion), name='delete_opinion'),
    path('order_detail/<int:card_id>/', user_passes_test(staff_member_required, login_url='/login/')(CardDetailsView.as_view()), name='order_detail'),
    path('addperfumeoptions/<int:product_id>/', user_passes_test(staff_member_required, login_url='/login/')(add_perfume_options), name='addperfumeoptions'),
    path('utilities/', user_passes_test(staff_member_required, login_url='/login/')(Utilities.as_view()), name='utilities'),
    path('edit_shipping_price/', user_passes_test(staff_member_required, login_url='/login/')(edit_shipping_price), name='edit_shipping_price'),
    path('edit_shipping_free/', user_passes_test(staff_member_required, login_url='/login/')(edit_shipping_free), name='edit_shipping_free'),
    path('edit_photo/<str:name>/', user_passes_test(staff_member_required, login_url='/login/')(edit_photo), name='edit_photo'),
    path('delete_coupon/<int:coupon_id>/', user_passes_test(staff_member_required, login_url='/login/')(delete_coupon), name='delete_coupon'),
    path('discover_sets/',user_passes_test(staff_member_required,login_url='/login/')(DiscoversetMainPage.as_view()), name="discover_sets"),
    path('editdiscover_sets/<int:product_id>/',user_passes_test(staff_member_required,login_url='/login/')(EditDiscoverSet.as_view()),name="editdiscover_set"),
    path('add_discoverset_options/<int:product_id>/',user_passes_test(staff_member_required,login_url="/login/")(add_discoverset_options),name="adddiscoversetoptions")
]
