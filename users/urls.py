from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import AddressViewSet, UserRegisterView, UserRetrieveView


app_name = "users"

router = DefaultRouter()
router.register(r"", AddressViewSet, basename="addresses")

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", UserRetrieveView.as_view(), name="user_detail"),
    path("me/address/", include(router.urls)),
]
