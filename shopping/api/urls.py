from django.urls import path
from .views import *


urlpatterns = [
    path('shoptype/', ShopTypeView.as_view()),
    # path('shoptype/<int:pk>/shop/', ShopView.as_view()),
    path('shop/', ShopView.as_view()),
    path('shop/<int:pk>/product/', ProductView.as_view()),
    # path('shop/<id:shop_id>/products/<id:product_id>', ProductView.as_view()),
    # path('shop/<int:shop_pk>/product/<int:product_pk>/<int:product_amount>/', CartView.as_view()),
    path('cart/product/<int:product_pk>/', CartView.as_view()),
    path('cart/<int:cart_pk>/product/<int:product_pk>/', AddDeleteProductInCartView.as_view()),
    path('cart/<int:cart_pk>/pay/', PayCartView.as_view()),
    path('cart/pending/', PendingCartView.as_view()),
    path('cart/paid/', PaidCartView.as_view()),
]

