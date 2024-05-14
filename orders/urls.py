from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders.views import OrderViewSet


app_name = "orders"

router = DefaultRouter()
router.register(r"order", OrderViewSet)

urlpatterns = router.urls
