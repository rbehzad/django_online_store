from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from shop_managing.models import *
from shopping.api.filters import ProductFilter
from .serializers import *
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from shopping.models import *


class ShopTypeView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = ShopType.objects.all()
    serializer_class = ShopTypeSerializer


class ShopView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['shop_type']

    def get_queryset(self):
        return super().get_queryset().filter(status='Confirmed')


class ProductView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        shop = Shop.objects.filter(id=self.kwargs['pk']).first()
        return super().get_queryset().filter(shop=shop)


class CreateCartView(APIView):# create cart with add a product
    permission_classes = [IsAuthenticated,]

    def post(self, request, pk):
        product = Product.objects.filter(id=pk).first()
        if not product:
            return Response(f"There is no product with {pk} id", status=status.HTTP_404_NOT_FOUND)
        if product.amount == 0:
            return Response(f"You can only add {product.amount} units of the product with {product.id} id to your cart as we don't have more in stock. Please re-adjust the quantity.", status=status.HTTP_403_FORBIDDEN)
        shop = product.shop
        cart = Cart.objects.create(title='cart', user=request.user, shop=shop)
        CartItem.objects.create(cart=cart, product=product, amount=1)
        product.amount -= 1
        product.save()
        product.check_availablity()
        return Response(f'Cart created with {cart.id} id', status=status.HTTP_201_CREATED)


class AddDeleteProductInCartView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request, cart_pk, product_pk):
        cart = Cart.objects.filter(id=cart_pk).first()
        product = Product.objects.filter(id=product_pk).first()
        if not cart or not product:
            return Response(f'the cart or the product not found!', status=status.HTTP_404_NOT_FOUND)
        conditions = [
            cart.status != 'Pending',
            cart.user != request.user,
            product.shop != cart.shop,
            product.amount <= 0,
        ]
        if all(conditions):
            return Response(f'Reauest is not valid!', status=status.HTTP_400_BAD_REQUEST)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            cart_item.amount += 1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart=cart, product=product, amount=1)
        product.amount -= 1
        product.save()
        product.check_availablity()
        return Response(f'Product with {product_pk} id added to cart with {cart_pk} id. now there are {cart_item.amount} units of this product in the cart', status=status.HTTP_201_CREATED)

    def delete(self, request, cart_pk, product_pk):
        cart = Cart.objects.filter(id=cart_pk).first()
        product = Product.objects.filter(id=product_pk).first()
        cart_item = CartItem.objects.filter(product=product, cart=cart).first()
        if not cart or not cart_item or not product:
            return Response(f'the cart or the product or the cart item not found!', status=status.HTTP_404_NOT_FOUND)
        if cart.user != request.user:
            return Response(f'You do not have access to this cart!', status=status.HTTP_403_FORBIDDEN)     
        if cart_item.amount - 1 <= 0:
            cart_item_id = cart_item.id
            cart_item.delete()
            product.amount += 1
            product.save()
            product.check_availablity()
            if not CartItem.objects.filter(cart=cart).first():
                cart_id = cart.id
                cart.delete()
                return Response(f'cart with {cart_id} id deleted', status=status.HTTP_200_OK)
            return Response(f'Product with {product_pk} id deleted from cart with {cart_pk} id. cart item with {cart_item_id} id deleted.', status=status.HTTP_200_OK)
        else:
            cart_item.amount -= 1
            cart_item.save()
            product.amount += 1
            product.save()
            product.check_availablity()
            return Response(f'Reduce the 1 units of product with id {product_pk} in cartitem with {cart_item.id} id. now there are {cart_item.amount} units of this product in the cart', status=status.HTTP_200_OK)


class PayCartView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request, cart_pk):
        cart = Cart.objects.filter(id=cart_pk).first()
        if not cart or cart.status != 'Confirmed':
            return Response(f'Cart with {cart_pk} id Not Found or cart status is not confirmed', status=status.HTTP_404_NOT_FOUND)
        if cart.user != request.user:
            return Response(f'You do not have access to this cart!', status=status.HTTP_403_FORBIDDEN)
        cart.status = 'Paid'
        cart.save()
        return Response(f'Cart with {cart_pk} id paid.', status=status.HTTP_200_OK)


class PendingCartView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return super().get_queryset().filter(status='Pending')


class PaidCartView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return super().get_queryset().filter(status='Paid')



