from django.urls import path
from django.urls.conf import include
from .views import *
# from .routers import router

urlpatterns = [
    path('shoptype/', ShopTypeView.as_view()),
    path('shop/', ShopView.as_view()),
    # path('', include(router.urls)),
]

