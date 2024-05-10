from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""

    list_display = ("name", "slug", "parent_category")
    list_display_links = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Товары"""

    list_display = ("name", "slug", "base_price", "sale_price", "quantity")
    list_display_links = ("name",)
    prepopulated_fields = {"slug": ("name",)}
