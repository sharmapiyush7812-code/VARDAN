from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    """Serializer for Product objects."""
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    price = serializers.IntegerField()
    old_price = serializers.IntegerField(required=False, allow_null=True)
    category = serializers.ListField(child=serializers.CharField())
    tag = serializers.CharField(required=False)
    sizes = serializers.ListField(child=serializers.CharField())
    stock = serializers.DictField()
    images = serializers.DictField()
    gallery = serializers.ListField(child=serializers.CharField())
    active = serializers.BooleanField(default=True)


class CartItemSerializer(serializers.Serializer):
    """Serializer for Cart Item."""
    id = serializers.CharField(required=False)
    product_id = serializers.CharField()
    size = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.IntegerField(required=False)
    subtotal = serializers.IntegerField(required=False)


class WishlistSerializer(serializers.Serializer):
    """Serializer for Wishlist."""
    user_id = serializers.CharField()
    products = serializers.ListField(child=serializers.CharField())


class SignUpSerializer(serializers.Serializer):
    """Serializer for user signup."""
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    phone = serializers.CharField(max_length=20)


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ShippingAddressSerializer(serializers.Serializer):
    """Serializer for shipping address."""
    name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)
    address = serializers.CharField()
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    pincode = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=100)


class CheckoutSerializer(serializers.Serializer):
    """Serializer for checkout request."""
    shipping_address = ShippingAddressSerializer()


class OrderItemSerializer(serializers.Serializer):
    """Serializer for items in an order."""
    product_id = serializers.CharField()
    name = serializers.CharField()
    size = serializers.CharField()
    quantity = serializers.IntegerField()
    unit_price = serializers.IntegerField()
    subtotal = serializers.IntegerField()


class OrderSerializer(serializers.Serializer):
    """Serializer for Order."""
    id = serializers.CharField()
    user_id = serializers.CharField()
    items = OrderItemSerializer(many=True)
    shipping_address = ShippingAddressSerializer()
    subtotal = serializers.IntegerField()
    payment_status = serializers.CharField()
    order_status = serializers.CharField()
    created_at = serializers.CharField()
