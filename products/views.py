from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination

from .models import Category, Product
from .serializers import (
    CategoryReadSerializer,
    CategoryWriteSerializer,
    ProductReadSerializer,
    ProductWriteSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
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

    def get_serializer_class(self):
        """
        Determines and returns the appropriate serializer class based on the action being performed.

        Parameters:
            self (object): The instance of the class.

        Returns:
            CategoryWriteSerializer: If the action is "create", "update", "partial_update", or "destroy".
            CategoryReadSerializer: Otherwise.
        """
        if self.action in ("create", "update", "partial_update", "destroy"):
            return CategoryWriteSerializer
        return CategoryReadSerializer

    def get_permissions(self):
        """
        A function that returns permissions based on the action being performed.

        Parameters:
            self (object): The instance of the class.

        Returns:
            list: A list of permissions based on the action.
        """
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD for products.

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

    pagination_class = LimitOffsetPagination
    lookup_field = "slug"

    def get_queryset(self):
        """
        Returns a queryset of products filtered by the specified category.

        Parameters:
            self (object): The instance of the class.

        Returns:
            queryset: A queryset of products filtered by the specified category.
        """
        queryset = Product.objects.all()
        category = self.request.query_params.get("category")

        if category:
            category_ids = Category.objects.filter(
                Q(id=category) | Q(parent_category_id=category)
            ).values_list("id", flat=True)
            queryset = queryset.filter(category_id__in=category_ids)

        return queryset

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return ProductWriteSerializer
        return ProductReadSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
