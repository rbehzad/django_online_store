from rest_framework import serializers
from shop_managing.models import ShopType, Shop
from accounts.models import User
from rest_framework.validators import UniqueValidator


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

class ShopTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopType
        fields = ('slug', 'title',)

class ShopSerializer(serializers.ModelSerializer):
    shop_type = ShopTypeSerializer()
    user = ProfileSerializer()
    class Meta:
        model = Shop
        fields = ('slug', 'title', 'shop_type', 'user')



