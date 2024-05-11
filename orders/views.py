from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from orders.permissions import (
    IsOrderByBuyerOrAdmin,
    IsOrderItemByBuyerOrAdmin,
    IsOrderItemPending,
    IsOrderPending,
)
from orders.serializers import (
    OrderItemSerializer,
    OrderWriteSerializer,
    OrderReadSerializer,
)
from orders.models import OrderItem, Order


class OrderItemViewSet(viewsets.ModelViewSet):
    """CRUD for order items that belong to a specific order"""

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsOrderItemByBuyerOrAdmin, IsOrderItemPending]

    def perform_create(self, serializer):
        order = get_object_or_404(Order, id=self.kwargs.get("order_id"))
        serializer.save(order=order)

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            self.permission_classes += [IsOrderItemPending]

        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    """CRUD for orders that belong to a specific buyer"""

    queryset = Order.objects.all()
    permission_classes = [IsOrderByBuyerOrAdmin]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return OrderWriteSerializer

        return OrderReadSerializer

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            self.permission_classes += [IsOrderPending]

        return super().get_permissions()
