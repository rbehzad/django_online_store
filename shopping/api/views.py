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
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['shop_type']
    
    def get(self):
        shops = Shop.objects.get(status='Confirmed')
        srz_data = ProductSerializer(instance=shops, many=True).data
        return Response(srz_data, status=status.HTTP_200_OK)


class ProductFilter(filters.FilterSet):
    # name = filters.CharFilter(lookup_expr='iexact')
    available = filters.BooleanFilter()
    price = filters.NumberFilter()
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lt')
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    class Meta:
        model = Product
        fields = ('available', 'price')

class ProductView(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated,]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get(self, request, pk):
        shop = Shop.objects.filter(id=pk).first()
        if not shop:
            return Response(f'Not Found Shop Object With {pk} id', status=status.HTTP_404_NOT_FOUND)
        products = Product.objects.filter(shop=shop).exclude(amount=0)
        srz_data = ProductSerializer(instance=products, many=True).data
        return Response(srz_data, status=status.HTTP_200_OK)

    # def get_queryset(self, *args, **kwargs):
    #     return self.queryset.filter(tag=self.kwargs.get('tag'))


class CartView(APIView):# create cart with add a product
    def post(self, request, shop_pk, product_pk, product_amount):
        # if Cart.objects.filter(status='Pending').first():
        #     return Response(f'You can not create new cart because your last cart has pending status.', status=status.HTTP_403_FORBIDDEN)
        try:
            shop = Shop.objects.get(id=shop_pk)
            cart = Cart.objects.create(title='cart', user=request.user, shop=shop)
            product = Product.objects.get(id=product_pk)
            CartItem.objects.create(cart=cart, product=product, amount=product_amount)
        except:
            return Response(f'Try Again', status=status.HTTP_400_BAD_REQUEST)
        finally:
            return Response(f'Cart was created with {cart.id} id', status=status.HTTP_201_CREATED)


class AddProductToCartView(APIView):
    def post():
        pass

