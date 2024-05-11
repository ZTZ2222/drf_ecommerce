from rest_framework import serializers

from .models import Category, Product


class CategoryReadSerializer(serializers.ModelSerializer):
    """Serializer class for category read."""

    class Meta:
        model = Category
        fields = "__all__"


class CategoryWriteSerializer(serializers.ModelSerializer):
    """Serializer class for category write."""

    class Meta:
        model = Category
        fields = (
            "name",
            "parent_category",
            "slug",
        )

    def create(self, attrs):
        instance, created = Category.objects.get_or_create(**attrs)
        return instance


class ProductReadSerializer(serializers.ModelSerializer):
    """Serializer class for product read."""

    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductWriteSerializer(serializers.ModelSerializer):
    """Serializer class for product write."""

    category = CategoryWriteSerializer()

    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "base_price",
            "sale_price",
            "quantity",
            "category",
            "slug",
        )

    def create(self, attrs):
        category = attrs.pop("category")
        instance, created = Category.objects.get_or_create(**category)
        product = Product.objects.create(category=instance, **attrs)

        return product

    def update(self, instance, attrs):
        if "category" in attrs:
            nested_setializer = self.fields["category"]
            nested_instance = instance.category
            nested_data = attrs.pop("category")
            nested_setializer.update(nested_instance, nested_data)

        return super(ProductWriteSerializer, self).update(instance, attrs)
