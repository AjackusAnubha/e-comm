from django.db import transaction

from rest_framework import generics, serializers

from .models import Product
from .serializers import ProductSerializer, OrderSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        total_price = 0
        product_updates = []

        # Extract product IDs from the validated data
        products = serializer.validated_data['products']
        product_ids = [item['product_id'] for item in products]

        # Fetch all required products in a single query
        all_products = Product.objects.filter(id__in=product_ids)
        product_map = {product.id: product for product in all_products}

        # Iterate over the products in the request
        for item in products:
            product_id = item['product_id']
            quantity = item['quantity']

            if quantity <= 0:
                raise serializers.ValidationError('Quantity must be greater than 0')

            # Fetch the product from the preloaded data
            product = product_map.get(product_id)
            if not product:
                raise serializers.ValidationError(
                    {"error": f"Product with ID {product_id} does not exist."}
                )

            if product.stock < quantity:
                raise serializers.ValidationError(
                    {"error": f"Insufficient stock for product {product.name}."}
                )

            # Calculate total price and update stock
            total_price += product.price * quantity
            product.stock -= quantity
            product_updates.append(product)

        # Update stock quantities for all products
        Product.objects.bulk_update(product_updates, ['stock'])

        # Save the order with the calculated total price
        serializer.save(total_price=total_price)
