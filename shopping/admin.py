from django.contrib import admin

from .models import *




class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'shop', 'status')

admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cart')

admin.site.register(CartItem, CartItemAdmin)