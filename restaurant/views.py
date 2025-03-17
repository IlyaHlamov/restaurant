from rest_framework.viewsets import ModelViewSet
from restaurant.models import Supplier
from restaurant.serializers import CreateUpdateSuppliersSerializer, SuppliersSerializer


class SupplierModelViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    model = Supplier
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_serializer_class(self):
        classes = {

            "create": CreateUpdateSuppliersSerializer,
            "partial_update": CreateUpdateSuppliersSerializer,
        }
        return classes.get(self.action, SuppliersSerializer)

