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
    path('change-cart-status/<slug:slug>/<str:status>', ChangeCartStatus.as_view(), name='change_cart_status'),
    path('search-cart/<slug:slug>', SearchCart.as_view(), name='search_cart'),
    path('filter-cart/<slug:slug>/<str:status>', FilterCart.as_view(), name='filter_cart'),
    path('cart-detail/<slug:slug>', CartDetail.as_view(), name='cart_detail'),
    path('product-list/<slug:slug>', ProductList.as_view(), name='product_list'),
    # path('delete-cart/<slug:slug>', DeleteCart.as_view(), name='delete_cart'),

]