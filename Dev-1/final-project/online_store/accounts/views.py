from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def email_login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
    return redirect(request.META.get('HTTP_REFERER'))


def username_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    return redirect(request.META.get('HTTP_REFERER'))


def phone_number_login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
    return redirect(request.META.get('HTTP_REFERER'))


def register(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
    return redirect(request.META.get('HTTP_REFERER'))


def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))