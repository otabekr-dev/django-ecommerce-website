from django.urls import path
from .views import ProductView, ProductDetailView

urlpatterns = [
    path('', ProductView.as_view(), name='product-list'),
    path('<int:id>/', ProductDetailView.as_view(), name='product-detail'),
]