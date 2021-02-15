from rest_framework.serializers import ModelSerializer

from foodcartapp.models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):  # noqa: D101

    class Meta:  # noqa: D106, WPS306
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):  # noqa: D101

    products = OrderItemSerializer(many=True, write_only=True)

    class Meta:  # noqa: D106, WPS306
        model = Order
        fields = ['id', 'firstname', 'lastname', 'address', 'phonenumber', 'products']
