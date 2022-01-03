from django.urls import path

from .views import *

urlpatterns = [
    path('index/', MyShopList.as_view(), name='shop_home'),
    path('delete-shop/<slug:slug>', deleteShop, name='delete_shop'),
    path('create-shop/', CreateShop.as_view(), name='create_shop'),
    path('update-shop/<slug:slug>', UpdateShop.as_view(), name='update_shop'),
]