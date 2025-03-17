from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import (
    SupplierModelViewSet, ProductModelViewSet
)

app_name = 'restourant'

router = DefaultRouter()
router.register(r'Supplier', SupplierModelViewSet, basename='Supplier')
router.register(r'Product', ProductModelViewSet, basename='Product')
urlpatterns = [
    path('', include(router.urls)),
]


