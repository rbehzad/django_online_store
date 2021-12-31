from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from .forms import *
from .models import GuestEmail
from django.utils.http import is_safe_url
from django.contrib import messages
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from online_store.mixins import NextUrlMixin, RequestFormAttachMixin
from .models import User


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/pages-register.html'
    success_url = '/pages-login/'



class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/pages-login.html'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


# def register_page(request):
#     form = RegisterForm(request.POST or None)

#     if form.is_valid():
#         data = form.cleaned_data
#         email = data.get('email')
#         password = data.get('password')
#         first_name = data.get('first_name')
#         last_name = data.get('last_name')
#         new_user = User.objects.create_user(email, password, first_name, last_name)
#         if new_user is not None:
#             messages.success(request, "Created User.")
#             return redirect('accounts:login')
        
#         messages.warning(request, "Create Error !")


#     context = {
#         "form": form
#     }

#     return render(request, "accounts/register.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_url')

    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('home_url')
        else:
            messages.warning(request, 'Credentials error.')

    return render(request, "accounts/login.html", context)


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
