from rest_framework.viewsets import ModelViewSet

from orders.permissions import (
    IsOrderByBuyerOrAdmin,
    IsOrderPending,
)
from orders.serializers import (
    OrderWriteSerializer,
    OrderReadSerializer,
)
from orders.models import Order


class OrderViewSet(ModelViewSet):
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
