from django.urls import path

from .views import *

urlpatterns = [
    path('index/', MyShopList.as_view(), name='shop_home'),
    path('delete-shop/<slug:slug>', DeleteShop.as_view(), name='delete_shop'),
    path('create-shop/', CreateShop.as_view(), name='create_shop'),
    path('update-shop/<slug:slug>', UpdateShop.as_view(), name='update_shop'),
    path('create-tag/', CreateTag.as_view(), name='create_tag'),
    path('add-product/', AddProduct.as_view(), name='add_product'),
    path('cart-list/<slug:slug>', CartList.as_view(), name='cart_list'),
    # path('delete-cart/<slug:slug>', DeleteCart.as_view(), name='delete_cart'),
]