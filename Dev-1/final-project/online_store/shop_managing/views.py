from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import *
from shop_managing.models import Shop
from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

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
        context['shops'] = context['shops'].filter(user=self.request.user).exclude(status='Deleted')
        # context['count'] = context['tasks'].filter(complete=False).count()
        return context


class CreateShop(CreateView):
    model = Shop
    form_class = CreateShopForm
    template_name = 'shop_managing/create_shop.html'

    def form_valid(self, form):
        shop = form.save(commit=False)
        shop.user = self.request.user
        shop.save()
        return redirect('shop_home')



# def CreateShop(request):
#     page = 'add_shop'
#     form = CreateShopForm()
#     if request.method == 'POST':
#         form = CreateShopForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.user = request.user
#             post.save()
#             form.save_m2m()
#             return redirect('shop_home')


#     return render(request, 'shop_managing/create_shop.html', {})



class UpdateShop(UpdateView):
    model = Shop
    form_class = CreateShopForm
    template_name = 'shop_managing/create_shop.html'
    success_url = reverse_lazy('shop_home')


# class DeletePostView(LoginRequiredMixin, DeleteView):
#     model = Post
#     template_name = 'feed/delete_post.html'
#     success_url = reverse_lazy('feed')
#     login_url = '/members/login/'

def deleteShop(request, slug):
    page = 'shop'
    shop = Shop.objects.get(slug=slug)
    context = {
        'page': page,
    }
    if request.method == 'POST': # confirming delete
        shop.status = 'Deleted'
        shop.save()
        return redirect('shop_home')
    return render(request, 'shop_managing/delete_confirm.html', context)