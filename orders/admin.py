from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "total_cost")
    list_display_links = ("id", "buyer", "total_cost")
    list_filter = ("buyer",)
    search_fields = ("buyer__email", "id")
    ordering = ("buyer",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "cost")
    list_display_links = ("order", "product")
    list_filter = ("order", "product")
    search_fields = ("order__buyer__email", "product__name")
    ordering = ("order", "product")
