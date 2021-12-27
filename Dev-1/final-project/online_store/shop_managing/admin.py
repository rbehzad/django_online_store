from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models.query import QuerySet
from .models import *


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
admin.site.register(Tag, TagAdmin)
 

class ShopAdmin(admin.ModelAdmin):
    models = Shop
    list_display = ('id', 'status', 'title', 'shop_type', 'created_at')
    list_filter = ('status', 'shop_type')
    search_fields = ('title',)

    actions = ['confirm_pending_shops', 'delete_pending_shops']    
    def confirm_pending_shops(self, request, queryset):
        queryset.update(status='Confirmed')

    def delete_pending_shops(self, request, queryset):
        queryset.update(status='Deleted')

admin.site.register(Shop, ShopAdmin)


class TagFilter(SimpleListFilter):
    title = 'Tag Filter'
    parameter_name = 'product_tag'

    def lookups(self, request, model_admin):
        return(
            ('has_tag', 'has_tag'),
            ('no_tag', 'no_tag'),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset 
        if self.value().lower() == 'has_tag':
            return queryset.exclude(tag=None)
        if self.value().lower() == 'no_tag':
            return queryset.filter(tag=None)


# below filter is for product(shop_type filter). because shop is ForeignKey we have to create filter Separately
# but in ShopAdmin we just need to give name of field(shop_type)
class ShopFilter(SimpleListFilter):
    title = 'Shop Filter'
    parameter_name = 'product_shop'
    
    def lookups(self, request, model_admin):
        return(
            Shop.SHOP_TYPE
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        for shoptype in Shop.SHOP_TYPE:
            if self.value().lower() == shoptype[0]:
                return queryset.filter(shop__shop_type=shoptype[0])

class ProductAdmin(admin.ModelAdmin):
    # list_display = ('admin_image', 'title', 'shop', 'amount')
    list_display = ('title', 'shop', 'amount')
    list_filter = ('shop', TagFilter, ShopFilter)
    search_fields = ('title',)
admin.site.register(Product, ProductAdmin)