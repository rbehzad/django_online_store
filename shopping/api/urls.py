from django.urls import path
from .views import *


urlpatterns = [
    path('shoptype/', ShopTypeView.as_view(), name='shopping_shoptypes'),
    path('shop/', ShopView.as_view(), name='shopping_shops'),
    path('shop/<int:pk>/product/', ProductView.as_view(), name='shopping_shop_product'),
    path('cart/product/<int:pk>/', CreateCartView.as_view(), name='shopping_create_cart'),
    path('cart/<int:cart_pk>/product/<int:product_pk>/', AddDeleteProductInCartView.as_view()),
    path('cart/<int:cart_pk>/pay/', PayCartView.as_view()),
    path('cart/pending/', PendingCartView.as_view(), name='shopping_pending'),
    path('cart/paid/', PaidCartView.as_view(), name='shopping_paid'),
]

