from rest_framework import serializers
from .models import Product, Order, OrderDetail

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
        for orderdetail in order.order_detail.all():
            total = total + orderdetail.product.price * orderdetail.cuantity
        return total

    def get_total_usd(self, order):
        pass
