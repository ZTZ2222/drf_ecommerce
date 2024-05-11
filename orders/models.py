from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from products.models import Product
from users.models import Address, User


class Order(models.Model):
    PENDING = "P"
    COMPLETED = "C"

    STATUS_CHOICES = ((PENDING, _("pending")), (COMPLETED, _("completed")))

    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        related_name="shipping_orders",
        null=True,
        blank=True,
    )
    billing_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        related_name="billing_orders",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id}"

    @cached_property
    def total_cost(self):
        """
        Calculates the total cost of the order by summing the cost of each order item.

        Returns:
            float: The total cost of the order, rounded to 2 decimal places.
        """
        return round(sum([order_item.cost for order_item in self.order_items.all()]), 2)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_orders"
    )
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order.buyer.email} - {self.product.name}"

    @cached_property
    def cost(self):
        """
        Calculates the cost of the order item by multiplying the price of the product and the quantity.

        Returns:
            float: The cost of the order item, rounded to 2 decimal places.

        Raises:
            TypeError: If the product is None.
        """
        if self.product is None:
            raise TypeError("Product cannot be None")
        return round(
            self.product.sale_price or self.product.base_price * self.quantity, 2
        )
