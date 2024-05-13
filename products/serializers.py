from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serializer class for category."""

    class Meta:
        model = Category
        fields = "__all__"


class ProductWriteOnlySerializer(serializers.ModelSerializer):
    """Serializer class for product."""

    class Meta:
        model = Product
        fields = "__all__"


class ProductReadOnlySerializer(serializers.ModelSerializer):
    """Serializer class for product."""

    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
