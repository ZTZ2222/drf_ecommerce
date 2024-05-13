from rest_framework import serializers

from users.serializers import BillingAddressSerializer, ShippingAddressSerializer

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer class for OrderItem model
    """

    price = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for OrderItemSerializer
        """

        model = OrderItem
        fields = "__all__"

    def validate(self, attrs):
        """
        Validate the order item data

        Ensure that the order quantity is not greater than the product quantity
        Ensure that the total quantity of the product in the order is not greater than the product quantity
        Ensure that the product is not already in the order
        Ensure that the user is authenticated

        Args:
            attrs (dict): The order item data

        Returns:
            dict: The validated order item data

        Raises:
            serializers.ValidationError: If the order quantity is greater than the product quantity
            serializers.ValidationError: If the total quantity of the product in the order is greater than the product quantity
            serializers.ValidationError: If the product is already in the order
            serializers.ValidationError: If the user is not authenticated
        """
        order_quantity = attrs.get("quantity")
        product_quantity = attrs.get("product").quantity

        order_id = self.context["view"].kwargs.get("order_id")
        product = attrs.get("product")
        current_item = OrderItem.objects.filter(order__id=order_id, product=product)

        if order_quantity > product_quantity:
            raise serializers.ValidationError(
                "Quantity cannot be greater than product quantity"
            )
        if current_item and current_item.quantity + order_quantity > product_quantity:
            raise serializers.ValidationError(
                "Quantity cannot be greater than product quantity"
            )

        if not self.instance and current_item.count() > 0:
            raise serializers.ValidationError("Product already in order")

        if self.context["request"].user.is_anonymous:
            raise serializers.ValidationError("User is not authenticated")

        return attrs

    def get_price(self, obj) -> float:
        """
        Get the sale price of the product

        Args:
            obj (OrderItem): The order item

        Returns:
            float: The sale price of the product
        """
        return obj.product.sale_price or obj.product.base_price

    def get_cost(self, obj) -> float:
        """
        Get the cost of the order item

        Args:
            obj (OrderItem): The order item

        Returns:
            float: The cost of the order item
        """
        return obj.cost


class OrderReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for Order model
    """

    buyer = serializers.CharField(source="buyer.email", read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_cost = serializers.SerializerMethodField()
    shipping_address = ShippingAddressSerializer(read_only=True)
    billing_address = BillingAddressSerializer(read_only=True)

    class Meta:
        """
        Meta class for OrderReadSerializer
        """

        model = Order
        fields = "__all__"

    def get_total_cost(self, obj) -> float:
        """
        Get the total cost of the order

        Args:
                        obj (Order): The order

        Returns:
                        float: The total cost of the order
        """
        return obj.total_cost


class OrderWriteSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating orders and order items

    Shipping address, billing address and payment are not included here
    They will be created/updated on checkout
    """

    buyer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("status",)

    def create(self, attrs):
        order_items = attrs.pop("order_items")
        order = Order.objects.create(**attrs)

        for order_item in order_items:
            OrderItem.objects.create(order=order, **order_item)

        return order

    def update(self, instance, attrs):
        orders_data = attrs.pop("order_items", None)
        orders = list((instance.order_items).all())

        if orders_data:
            for order_data in orders_data:
                order = orders.pop(0)
                order.product = order_data.get("product", order.product)
                order.quantity = order_data.get("quantity", order.quantity)
                order.save()

        return instance
