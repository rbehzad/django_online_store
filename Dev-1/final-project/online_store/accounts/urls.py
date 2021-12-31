from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(), name="shop_login"),
    path('register/', RegisterView.as_view(), name="shop_register"),
    # path('logout/', LogoutView.as_view(), name="logout"),
    # path('guest/register/', guest_register_view, name="guest_register"),

]