from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import CategoryViewSet, ProductViewSet


app_name = "products"

router = DefaultRouter()
router.register(r"category", viewset=CategoryViewSet, basename="category")
router.register(r"product", viewset=ProductViewSet, basename="product")

urlpatterns = [path("", include(router.urls))]
