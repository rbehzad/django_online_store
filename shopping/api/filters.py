from pyexpat import model
from statistics import mode
from django_filters import rest_framework
from shop_managing import models

class ProductFilter(rest_framework.FilterSet):
    price_gt = rest_framework.NumberFilter(field_name='price', lookup_expr='gt')
    price_lt = rest_framework.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = models.Product
        fields = ['tag', 'available']
