from django.urls import path
from django.urls.conf import include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from .routers import router




urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('user/<int:pk>/', RetrieveUpdateUser.as_view()),

]

