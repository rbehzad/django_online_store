
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from shop_managing.models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from django_filters import rest_framework as filters
from shopping.models import *


def cart_exist(id):
    if not Cart.objects.filter(id=id).exists():
        return Response(f'Cart Not Found', status=status.HTTP_404_NOT_FOUND)


def valid_user(cart_user, request_user):
    if cart_user != request_user:
        return Response(f'You do not have access to this cart!', status=status.HTTP_403_FORBIDDEN)


def enough_amount(product_amount, amount):
    if product_amount > amount:
        return Response("Not enough amount of the product in stock. Please re-adjust the quantity.", status=status.HTTP_403_FORBIDDEN)
