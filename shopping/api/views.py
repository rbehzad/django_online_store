import re
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
    def post(self, request, product_pk):
        product = Product.objects.filter(id=product_pk).first()
        if not product:
            return Response(f"There is no product with {product_pk} id", status=status.HTTP_404_NOT_FOUND)
        shop = product.shop
        cart = Cart.objects.create(title='cart', user=request.user, shop=shop)
        if product.amount == 0:
            return Response(f"You can only add {product.amount} units of the product with {product.id} id to your cart as we don't have more in stock. Please re-adjust the quantity.", status=status.HTTP_403_FORBIDDEN)
        CartItem.objects.create(cart=cart, product=product, amount=1)
        product.amount -= 1
        product.save()
        return Response(f'Cart was created with {cart.id} id', status=status.HTTP_201_CREATED)


# class CartView(generics.CreateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartItemSerializer
#     def post(self, request):
#         data = request.data # include poduct id and amount
#         product = Product.objects.get(id=data['id'])
#         if(data['amount'] > product.amount):
#             return Response("Not enough amount of the product in stock. Please re-adjust the quantity.", status=status.HTTP_400_BAD_REQUEST)

#         data['user'] = self.request.user
#         data['shop'] = product.shop
#         cart = CartSerializer(data=request.data)
#         if cart.is_valid():
#             cart.save()
#             CartItem.objects.create(cart=cart, product=product, amount=data['amount'])
#             product.amount -= int(data['amount'])
#             product.save()
#             return Response(cart.data['id'], status=status.HTTP_201_CREATED)
#         return Response(cart.errors, status=status.HTTP_400_BAD_REQUEST)





class AddDeleteProductInCartView(APIView):
    def post(self, request, cart_pk, product_pk):
        cart = Cart.objects.filter(id=cart_pk).first()
        if not cart:
            return Response(f'Cart with {cart_pk} id Not Found', status=status.HTTP_404_NOT_FOUND)
        if cart.status != 'Pending':
            return Response(f'You can not add product to this cart with {cart_pk} id', status=status.HTTP_403_FORBIDDEN)
        if cart.user != request.user:
            return Response(f'You do not have access to this cart!', status=status.HTTP_403_FORBIDDEN)
        product = Product.objects.filter(id=product_pk).first()
        if not product:
            return Response(f"There is no product with {product_pk} id", status=status.HTTP_404_NOT_FOUND)
        if product.shop != cart.shop:
            return Response("product shop and cart shop is not same", status=status.HTTP_403_FORBIDDEN)
        if product.amount == 0:
            return Response("Not enough amount of the product in stock. Please re-adjust the quantity.", status=status.HTTP_403_FORBIDDEN)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            cart_item.amount += 1
        else:
            CartItem.objects.create(cart=cart, product=product, amount=1)
        product.amount -= 1
        product.save()
        return Response(f'Product with {product_pk} id added to cart with {cart_pk} id', status=status.HTTP_201_CREATED)

    def delete(self, request, cart_pk, product_pk):
        cart = Cart.objects.filter(id=cart_pk).first()
        if not cart:
            return Response(f'Cart with {cart_pk} id Not Found', status=status.HTTP_404_NOT_FOUND)
        if cart.user != request.user:
            return Response(f'You do not have access to this cart!', status=status.HTTP_403_FORBIDDEN)
        product = Product.objects.filter(id=product_pk).first()
        if not product:
            return Response(f"There is no product with {product_pk} id", status=status.HTTP_404_NOT_FOUND)
        cart_item = CartItem.objects.filter(product=product, cart=cart).first()
        if not cart_item:
            return Response(f'There is no product with {product_pk} id in cart with {cart_pk} id', status=status.HTTP_404_NOT_FOUND)
        else:
            if cart_item.amount - 1 <= 0:
                cart_item.delete()
                product.amount += 1
                product.save()
                return Response(f'Product with {product_pk} id deleted from cart with {cart_pk} id', status=status.HTTP_200_OK)
            else:
                cart_item.amount -= 1
                cart_item.save()
                product.amount += 1
                product.save()
                return Response(f'Reduce the 1 units of product with id {product_pk} in cartitem with {cart_item.id} id.', status=status.HTTP_200_OK)


class PayCartView(APIView):
    def post(self, request, cart_pk):
        cart = Cart.objects.filter(id=cart_pk).first()
        if not cart or cart.status != 'Pending':
            return Response(f'Cart with {cart_pk} id Not Found or cart status is not pending', status=status.HTTP_404_NOT_FOUND)
        if cart.user != request.user:
            return Response(f'You do not have access to this cart!', status=status.HTTP_403_FORBIDDEN)
        cart.status = 'Paid'
        cart.save()
        return Response(f'Cart with {cart_pk} id paid.', status=status.HTTP_200_OK)


class PendingCartView(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated,]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return super().get_queryset().filter(status='Pending')

class PaidCartView(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated,]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return super().get_queryset().filter(status='Paid')