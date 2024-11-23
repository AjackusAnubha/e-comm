from django.urls import path
from .views import ProductListCreateAPIView, OrderCreateAPIView

urlpatterns = [
    path('products', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('orders', OrderCreateAPIView.as_view(), name='order-create'),
]
