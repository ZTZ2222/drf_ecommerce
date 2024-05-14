from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.pagination import LimitOffsetPagination

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductWriteOnlySerializer,
    ProductReadOnlySerializer,
)


class CategoryViewSet(ModelViewSet):
    """
    CRUD for categories.

    create:
    Create a new category.

    update:
    Update an existing category.

    partial_update:
    Partially update an existing category.

    destroy:
    Delete a category.

    retrieve:
    Retrieve a category.

    list:
    List all categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAdminUser()]
        return [AllowAny()]


class ProductViewSet(ModelViewSet):
    """
    Products viewset.

    create:
    Create a new product.

    update:
    Update an existing product.

    partial_update:
    Partially update an existing product.

    destroy:
    Delete a product.

    retrieve:
    Retrieve a product.

    list:
    List all products.
    """

    queryset = Product.objects.all()
    pagination_class = LimitOffsetPagination
    lookup_field = "slug"

    def get_queryset(self):
        """Filter products by category if specified."""
        category_id = self.request.query_params.get("category")
        if category_id:
            return self.queryset.filter(
                category_id__in=Category.objects.filter(
                    Q(id=category_id) | Q(parent_category_id=category_id)
                ).values_list("id", flat=True)
            )
        return self.queryset

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return ProductWriteOnlySerializer
        return ProductReadOnlySerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAdminUser()]
        return [AllowAny()]
