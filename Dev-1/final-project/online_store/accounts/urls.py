from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.email_login, name='email_login'),
    # path('login/', views.username_login, name='username_login'),
    # path('login/', views.phone_number_login, name='phone_number_login'),
    # path('login/', views.register, name='register'),
    path('', views.log_out, name='log_out'),
]