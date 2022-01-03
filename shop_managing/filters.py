import django_filters
from .models import *


class ShopFilter(django_filters.FilterSet):
    class Meta:
        model = Shop
        fields = ['status', 'shop_type']