from django.urls import path

from .views import *

urlpatterns = [
    path('index/', MyShopList.as_view(), name='shop_home'),
]