from rest_framework import serializers
from shop_managing.models import Product, ShopType, Shop
from accounts.models import User
from rest_framework.validators import UniqueValidator

from shopping.models import Cart, CartItem

class ProfileSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

class ShopTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopType
        fields = ('id', 'title',)

class ShopSerializer(serializers.ModelSerializer):
    shop_type = ShopTypeSerializer()
    user = ProfileSerializer2()
    class Meta:
        model = Shop
        fields = ('id', 'title', 'shop_type', 'user')

class ProductSerializer(serializers.ModelSerializer):
    shop = ShopTypeSerializer()
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'shop', 'tag', 'amount', 'available')

class ShopSerializer2():
    shop_type = ShopTypeSerializer()
    class Meta:
        model = Shop
        fields = ('title', 'shop_type')

class CartSerializer(serializers.ModelSerializer):
    shop = ShopSerializer2()
    user = ProfileSerializer2()
    class Meta:
        model = Cart
        fields = ('id', 'shop', 'user', 'status', 'created_at')


class CartCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ''