from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import *
from .models import *
from shopping.models import *
from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.contrib import messages

#### view for image (file field):
# def upload(request):
#     if request.method == 'POST':
#         images = request.FILES.getlist('images')

#         for img in images:
#             Product.objects.create(image=img, ...)
#         images = Product.objects.all()
#         return render(request, 'index.html', {'images':images})


class MyShopList(LoginRequiredMixin, ListView):
    model = Shop
    context_object_name = 'shops'
    template_name = 'shop_managing/shop_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['shops'] = context['shops'].filter(user=self.request.user).exclude(status='Deleted')
        context['shops'] = Shop.objects.filter(user=self.request.user).exclude(status='Deleted')
        # context['count'] = context['tasks'].filter(complete=False).count()
        return context


class CreateShop(CreateView):
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


class CreateTag(CreateView):
    model = Tag
    form_class = CreateTagForm
    template_name = 'shop_managing/create_tag.html'
    success_url = reverse_lazy('shop_home')



class UpdateShop(UpdateView):
    model = Shop
    form_class = CreateShopForm
    template_name = 'shop_managing/create_shop.html'
    success_url = reverse_lazy('shop_home')


class AddProduct(CreateView):
    def get(self, request, *args, **kwargs):
        form = AddProductForm(user=request.user)
        return render(request, 'shop_managing/add_product.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = AddProductForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            form.save_m2m()
            return render(request, 'shop_managing/add_product.html', {'form': form})
        return render(request, 'shop_managing/add_product.html', {'form': form})


# def DeleteShop(request, slug):
#     page = 'shop'
#     shop = Shop.objects.get(slug=slug)
#     context = {
#         'page': page,
#     }
#     if request.method == 'POST': # confirmation deleting
#         shop.status = 'Deleted'
#         shop.save()
#         if not Shop.objects.filter(user=request.user).exclude(status='Deleted').exists():
#             request.user.seller = False
#             request.user.save()
#         return redirect('shop_home')
#     return render(request, 'shop_managing/delete_confirm.html', context)

# class DeleteShopConfirm(View):
#     def post(self, request, *args, **kwargs):
#         shop = Shop.objects.get(slug=slug)
#         shop.status = 'Deleted'
#         shop.save()
#         if not Shop.objects.filter(user=request.user).exclude(status='Deleted').exists():
#             request.user.seller = False
#             request.user.save()

#         return render(request, 'shop_managing/add_product.html', {})

# class DeleteShop(DeleteView):
#     model = Shop
#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         self.object.status = 'Deleted'
#         self.object.save()
#         return redirect('shop_managing/shop_dashboard.html')


class DeleteShop(View):
    model = Shop
    def post(self, request, *args, **kwargs):
        shop = Shop.objects.get(slug=self.kwargs['slug'])
        shop.status = 'Deleted'
        shop.save()
        return render(request, "shop_managing/shop_dashboard.html", {})

    def get(self, request, *args, **kwargs):
        shop = Shop.objects.get(slug=self.kwargs['slug'])
        return render(request, "shop_managing/delete_confirm.html", {'page': 'shop'})


class CartList(LoginRequiredMixin, ListView):
    model = Cart
    context_object_name = 'shops'
    template_name = 'shop_managing/shop_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shops'] = Shop.objects.filter(user=self.request.user).exclude(status='Deleted')
        return context