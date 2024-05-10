from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet


app_name = "products"

router = DefaultRouter()
router.register(r"categories", viewset=CategoryViewSet, basename="categories")
router.register(r"", viewset=ProductViewSet, basename="products")

urlpatterns = [path("", include(router.urls))]
