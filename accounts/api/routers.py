from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'user', ProfileView, basename='profile')
# router.register(r'update', UpdateUserProfile, basename='update_profile')


