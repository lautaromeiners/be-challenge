from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters

from .models import Product, OrderDetail, Order
from .serializers import ProductSerializer, OrderSerializer, OrderDetailSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.products.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_fields = ['name']
    permission_classes = (IsAuthenticated,)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.orders.all().prefetch_related('order_detail', 'order_detail__product')
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        for detail in instance.order_detail.all():
            product = detail.product
            product.stock = product.stock + detail.quantity
            product.save()

        return instance

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.details.all()
    serializer_class = OrderDetailSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['product__name']
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        if quantity <= 0:
            raise ValidationError('Quantity cannot be negative.')

        detail = OrderDetail.details.filter(order=serializer.validated_data['order'].id, product=product.id)
        if detail.exists():
            raise ValidationError('Product is already in order.')

        stock_after_purchase = product.stock - quantity
        
        if product.stock <= 0 or stock_after_purchase < 0:
            raise ValidationError('Not enough stock.')
        else:
            product.stock = stock_after_purchase
            product.save()

        return serializer.save()
