from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from .forms import *
from .models import GuestEmail
from django.utils.http import is_safe_url
from django.contrib import messages
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from online_store.mixins import NextUrlMixin, RequestFormAttachMixin
from .models import User
from django.contrib.auth import login, logout, views as auth_views
from django.urls import reverse_lazy


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/pages-register.html'
    success_url = reverse_lazy('shop_home')


def LoginView(request):
    if request.user.is_authenticated:
        return redirect('shop_home')
    else:
        if request.method == 'POST':
            username = request.POST['email']
            password = request.POST['password']
            # if user authenticated below function return user object
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # this is gonna create that session and put into that coockies
                login(request, user)
                return redirect('shop_home')

        return render(request, 'accounts/pages-login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('shop_login')


def guest_register_view(request):
    if request.user.is_authenticated:
        return redirect('carts:home')

    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('home_url')

    return render(request, "accounts/login.html", context)
