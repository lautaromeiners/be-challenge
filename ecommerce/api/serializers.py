from rest_framework import serializers
from .models import Product, Order, OrderDetail
from .services import get_usd_price

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('date_time', 'total', 'total_usd', 'order_detail')

    total = serializers.SerializerMethodField(method_name='get_total')
    total_usd = serializers.SerializerMethodField(method_name='get_total_usd')

    def get_total(self, order):
        total = 0
        for detail in order.order_detail.all():
            total = total + detail.product.price * detail.quantity
        return total

    def get_total_usd(self, order):
        usd = get_usd_price()
        total_usd = self.get_total(order) / usd

        return round(total_usd, 2)

