from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from shop_managing.models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend


class ShopTypeView(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated,]
    queryset = ShopType.objects.all()
    serializer_class = ShopTypeSerializer


class ShopView(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated,]
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['shop_type']


class ProductView(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated,]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tag']