from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from .models import *
from shopping.models import *
from blog.models import Post
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    View,
)
from django.db.models import Q
from django.contrib import messages
from django.db.models import Count, Sum, Max
from rest_framework.views import APIView
from rest_framework.response import Response


def get_customers_with_all_information(logined_user):
    # find number of paid carts
    customers = []
    for customer in User.objects.all():
        paid_carts = list(Cart.objects.filter(user=customer, status='Paid'))
        customer.num_carts = len(paid_carts)
        if customer != logined_user and customer.num_carts != 0:
            customers.append(customer) # customer2 is request.user's customers

    for customer in customers:
        carts = Cart.objects.filter(user=customer, status='Paid')
        if carts.exists():
            customer.last_cart_date = carts.last().created_at # find last cart date
        sum = 0
        total_paid = 0
        for cart in carts:
            sum = cart.get_products_number()
            total_paid = cart.get_total_price()
        customer.num_products = sum
        customer.total_paid = total_paid
    return customers


class MyShopList(LoginRequiredMixin, ListView):
    model = Shop
    context_object_name = 'shops'
    template_name = 'shop_managing/shop_dashboard.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        customers = get_customers_with_all_information(user)
        context = {
            'shops': Shop.objects.filter(user=user).exclude(status='Deleted'),
            'customers': customers,
            'phone_number_confirmation': user.phone_number_confirmation,
        }
        return context


class CreateShop(LoginRequiredMixin, CreateView):
    model = Shop
    form_class = CreateShopForm
    template_name = 'shop_managing/create_shop.html'
    def form_valid(self, form):
        if Shop.objects.filter(user=self.request.user).filter(status='Pending'):
            messages.error(self.request, 'Your are not allowed to create new shop till the last shop get confirmed.')
            return redirect('create_shop')

        shop = form.save(commit=False)
        shop.user = self.request.user
        shop.save()
        self.request.user.seller = True
        self.request.user.save()
        return redirect('shop_home')


class CreateTag(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = CreateTagForm
    template_name = 'shop_managing/create_tag.html'
    success_url = reverse_lazy('shop_home')


class UpdateShop(LoginRequiredMixin, UpdateView):
    model = Shop
    form_class = CreateShopForm
    template_name = 'shop_managing/create_shop.html'
    def form_valid(self, form):
        shop = form.save(commit=False)
        shop.user = self.request.user
        shop.status = 'Pending'
        shop.save()
        return redirect('shop_home')


class AddProduct(LoginRequiredMixin, CreateView):
    def get(self, request, *args, **kwargs):
        form = AddProductForm(user=request.user)
        return render(request, 'shop_managing/add_product.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = AddProductForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            form.save_m2m()
            return redirect('shop_home')

        return render(request, 'shop_managing/add_product.html', {'form': form})


class DeleteShop(LoginRequiredMixin, View):
    model = Shop
    def post(self, request, *args, **kwargs):
        shop = Shop.objects.get(slug=self.kwargs['slug'])
        shop.status = 'Deleted'
        shop.save()
        return redirect('shop_home')

    def get(self, request, *args, **kwargs):
        shop = Shop.objects.get(slug=self.kwargs['slug'])
        return render(request, "shop_managing/delete_confirm.html", {'page': 'shop'})


class CartList(LoginRequiredMixin, View):
    model = Cart
    def get(self, request, *args, **kwargs):
        context = {
            'carts': Cart.objects.filter(shop__slug=self.kwargs['slug']).order_by('created_at'),
            'shop': Shop.objects.get(slug=self.kwargs['slug']),
            'status': ['Pending', 'Confirmed', 'Deleted', 'Paid'],
            
        }
        return render(request, 'shop_managing/cart_list.html', context)


class ChangeCartStatus(LoginRequiredMixin, View):
    model = Cart
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(slug=self.kwargs['slug'])
        cart.status = self.kwargs['status']
        cart.save()
        shop = Cart.objects.get(slug=self.kwargs['slug']).shop
        context = {
            'shop': shop,
            'carts': Cart.objects.filter(shop=shop).order_by('created_at'),
            'status': ['Pending', 'Confirmed', 'Deleted', 'Paid']
        }
        return render(request, 'shop_managing/cart_list.html', context)


class SearchCart(LoginRequiredMixin, View):
    model = Cart
    def post(self, request, *args, **kwargs):
        searched = request.POST['search']
        context = {
            'carts': Cart.objects.filter(shop__slug=self.kwargs['slug']).filter(title__contains=searched).order_by('created_at'),
            'shop': Shop.objects.get(slug=self.kwargs['slug']),
            'status': ['Pending', 'Confirmed', 'Deleted', 'Paid']
        }
        return render(request, 'shop_managing/cart_list.html', context)


class FilterCart(LoginRequiredMixin, View):
    model = Cart
    def get(self, request, *args, **kwargs):
        context = dict()
        context['shop'] = Shop.objects.get(slug=self.kwargs['slug'])
        context['status'] = ['Pending', 'Confirmed', 'Deleted', 'Paid']

        if self.kwargs['status'] == 'All':
            context['carts'] = Cart.objects.filter(shop__slug=self.kwargs['slug']).order_by('created_at')
        else:
            context['carts'] = Cart.objects.filter(shop__slug=self.kwargs['slug']).filter(status=self.kwargs['status']).order_by('created_at')

        return render(request, 'shop_managing/cart_list.html', context)


class CartDetail(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'shop_managing/cart_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'items': CartItem.objects.filter(cart__slug=self.kwargs['slug']),
            'cart': Cart.objects.get(slug=self.kwargs['slug'])
        }
        return context


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'shop_managing/product_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = Shop.objects.get(slug=self.kwargs['slug'])
        num_carts = len(list(Cart.objects.filter(shop=shop, status='Paid')))
        cart_items = CartItem.objects.filter(product__shop=shop, cart__status='Paid')
        num_products = 0
        for cart_item in cart_items:
            num_products += cart_item.amount
        context = {
            'products': Product.objects.filter(shop__slug=self.kwargs['slug']),
            'shop': shop,
            'num_carts': num_carts,
            'num_products': num_products
        }
        return context

