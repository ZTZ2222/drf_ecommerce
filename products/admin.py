from django.contrib import admin
from django.utils.safestring import mark_safe
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

    list_display = ("name", "slug", "price", "quantity")
    list_display_links = ("name",)
    readonly_fields = ("get_image",)
    prepopulated_fields = {"slug": ("name",)}

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="100"')

    get_image.short_description = "Изображение"
