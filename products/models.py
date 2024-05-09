from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def product_image_path(instance, filename):
    return f"mediafiles/products/{instance.slug}/{filename}"


class Category(models.Model):
    name = models.CharField(
        ("Категория"),
        max_length=100,
    )
    parent_category = models.ForeignKey(
        "self",
        related_name="Подкатегории",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        ("Slug"),
        max_length=100,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(("Название"), max_length=100)
    description = models.TextField(("Описание"), blank=True)
    image = models.ImageField(("Изображение"), upload_to=product_image_path, blank=True)
    price = models.DecimalField(("Цена"), decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=1)
    category = models.ForeignKey(
        Category,
        related_name="product_list",
        on_delete=models.SET_NULL,
        null=True,
    )
    slug = models.SlugField(
        ("Slug"),
        max_length=100,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
