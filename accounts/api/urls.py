from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profile', ProfileView, basename='profile')

urlpatterns = [
    path('login', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='auth_register'),
    # path('profile', ProfileView.as_view(), name='profile'),

]

