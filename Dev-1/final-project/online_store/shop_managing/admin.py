from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models.query import QuerySet
from .models import *


admin.site.register(ShopType)

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('title',)
admin.site.register(Tag, TagAdmin)
 

class ShopAdmin(admin.ModelAdmin):
    models = Shop
    list_display = ('id', 'status', 'title', 'shop_type', 'created_at')
    list_filter = ('status', 'shop_type')
    search_fields = ('title',)
    list_editable = ('status',)
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


# there is no shoptype field in Product model and because of that we wrote seperatly code then add to it
# class ShopTypeFilter(SimpleListFilter):
#     title = 'ShopType Filter'
#     parameter_name = 'product_shoptype'
#     shoptypes = ShopType.objects.all()
#     shoptype_list = []
#     for shoptype in shoptypes:
#         shoptype_list.append((shoptype.title, shoptype.title,))

#     def lookups(self, request, model_admin):
#         return tuple(ShopTypeFilter.shoptype_list)

#     def queryset(self, request, queryset):
#         if not self.value():
#             return queryset

#         for shoptype in ShopTypeFilter.shoptype_list:
#             if self.value().lower() == shoptype[0]:
#                 return queryset.filter(shop__shop_type__title=shoptype[0])

class ProductAdmin(admin.ModelAdmin):
    list_display = ('admin_image', 'title', 'shop', 'amount')
    # list_filter = ('shop', TagFilter, ShopTypeFilter)
    list_filter = ('shop', TagFilter)
    search_fields = ('title',)
admin.site.register(Product, ProductAdmin)
