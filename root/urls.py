from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/products/", include("products.urls", namespace="products")),
    path("api/users/", include("users.urls", namespace="users")),
    path("api/orders/", include("orders.urls", namespace="orders")),
]
