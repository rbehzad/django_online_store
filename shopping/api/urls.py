from django.urls import path
from .views import *


urlpatterns = [
    path('shoptype/', ShopTypeView.as_view()),
    # path('shoptype/<int:pk>/shop/', ShopView.as_view()),
    path('shop/', ShopView.as_view()),
    path('shop/<int:pk>/product/', ProductView.as_view()),
    # path('shop/<id:shop_id>/products/<id:product_id>', ProductView.as_view()),
]

