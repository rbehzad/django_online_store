from django.urls import path
from django.urls.conf import include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from .routers import router

urlpatterns = [
    path('login', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='auth_register'),
    path('user/<int:pk>', UpdateUserProfile.as_view()),
    path('', include(router.urls)),

]

