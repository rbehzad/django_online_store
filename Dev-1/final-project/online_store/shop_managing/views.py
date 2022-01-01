from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from shop_managing.models import Shop


#### view for image (file field):
# def upload(request):
#     if request.method == 'POST':
#         images = request.FILES.getlist('images')

#         for img in images:
#             Product.objects.create(image=img, ...)
#         images = Product.objects.all()
#         return render(request, 'index.html', {'images':images})


# class HomeListView(ListView):
#     model = Shop
#     template_name = 'accounts/index.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['myshops'] = Shop.objects.filter(user=request.user).order_by('-created_at')
#         return context


class MyShopList(LoginRequiredMixin, ListView):
    model = Shop
    context_object_name = 'shops'
    template_name = 'shop_managing/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shops'] = context['shops'].filter(user=self.request.user)
        # context['count'] = context['tasks'].filter(complete=False).count()

        # search_input = self.request.GET.get('search-area') or ''
        # if search_input:
        #     context['tasks'] = context['tasks'].filter(
        #         title__contains=search_input)

        # context['search_input'] = search_input

        return context

