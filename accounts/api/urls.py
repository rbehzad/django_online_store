from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='jwt_login'),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('user/', RetrieveUpdateUser.as_view()),
    path('otp/request-id/', OTP_get_request_id_view.as_view(), name='otp_request'),
    path('otp/validate/', OTP_validate_view.as_view(), name='otp_validate'),
]

