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
from shopping.api import object_exist

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

    def get_queryset(self):
        return super().get_queryset().filter(status='Confirmed')


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
    def post(self, request, shop_pk, product_pk, amount):
        shop = Shop.objects.get(id=shop_pk)
        cart = Cart.objects.create(title='cart', user=request.user, shop=shop)
        product = Product.objects.get(id=product_pk)
        if int(amount) > int(product.amount):
            return Response(f"You can only add {product.amount} units of the product to your cart as we don't have more in stock. Please re-adjust the quantity.", status=status.HTTP_403_FORBIDDEN)
        CartItem.objects.create(cart=cart, product=product, amount=amount)
        product.amount -= amount
        product.save()

        return Response(f'Cart was created with {cart.id} id', status=status.HTTP_201_CREATED)


class AddDeleteProductInCartView(APIView):
    def post(self, request, product_pk, amount, cart_pk):
        cart = Cart.objects.filter(id=cart_pk).first()
        # if not cart:
        #     return Response(f'Cart Not Found', status=status.HTTP_404_NOT_FOUND)
        object_exist.cart_exist(cart_pk)
        object_exist.valid_user(cart.user, request.user)
        # if cart.user != request.user:
        #     return Response(f'You do not have access to this cart!', status=status.HTTP_403_FORBIDDEN)
        product = Product.objects.get(id=product_pk)
        object_exist.enough_amount(amount, product.amount)
        # if not object_exist.enough_amount(amount, product.amount):
            # return Response("Not enough amount of the product in stock. Please re-adjust the quantity.", status=status.HTTP_403_FORBIDDEN)
        CartItem.objects.create(cart=cart, product=product, amount=amount)
        product.amount -= amount
        product.save()
        return Response(f'Product with {product_pk} id added to cart with {cart_pk} id', status=status.HTTP_201_CREATED)

    def delete(self, request, product_pk, product_amount, cart_pk):
        cart = Cart.objects.get(id=cart_pk)
        if cart.user != request.user:
            return Response(f'You do not have access to this cart!', status=status.HTTP_403_FORBIDDEN)
        product = Product.objects.get(id=product_pk)
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        if cart_item.first():
            if cart_item.amount - product_amount <= 0:
                cart_item.delete()
                return Response(f'Product with {product_pk} id deleted from cart with {cart_pk} id', status=status.HTTP_200_OK)
            else:
                cart_item.amount -= product_amount
                return Response(f'Reduce the {product_amount} units of product with id {product_pk} in cartitem with {cart_item.id} id.', status=status.HTTP_200_OK)
        else:
            return Response(f'There is no product with {product_pk} id in cart with {cart_pk} id', status=status.HTTP_404_NOT_FOUND)


