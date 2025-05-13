from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SupplierModelViewSet, ProductModelViewSet, MenuModelViewSet
)

app_name = 'restourant'

router = DefaultRouter()
router.register(r'supplier', SupplierModelViewSet, basename='supplier')
router.register(r'Product', ProductModelViewSet, basename='Product')
router.register(r'Menu', MenuModelViewSet, basename='Menu')

urlpatterns = [
    path('', include(router.urls)),
]


