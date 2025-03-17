from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import (
    SupplierModelViewSet
)

app_name = 'restourant'

router = DefaultRouter()
router.register(r'Supplier', SupplierModelViewSet, basename='Supplier')
urlpatterns = [
    path('', include(router.urls)),
]
