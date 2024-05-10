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

    def create(self, validated_data):
        instance, created = Category.objects.get_or_create(**validated_data)
        return instance


class ProductReadSerializer(serializers.ModelSerializer):
    """Serializer class for product read."""

    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductWriteSerializer(serializers.ModelSerializer):
    """Serializer class for product write."""

    category = CategoryReadSerializer()

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

    def create(self, validated_data):
        category = validated_data.pop("category")
        instance, created = Category.objects.get_or_create(**category)
        product = Product.objects.create(category=instance, **validated_data)

        return product

    def update(self, instance, validated_data):
        if "category" in validated_data:
            nested_setializer = self.fields["category"]
            nested_instance = instance.category
            nested_data = validated_data.pop("category")
            nested_setializer.update(nested_instance, nested_data)

        return super(ProductWriteSerializer, self).update(instance, validated_data)
