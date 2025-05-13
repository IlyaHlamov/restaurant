from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from restaurant.models import Supplier, Product, Menu, Order, OrderMenu
from restaurant.serializers import CreateUpdateSuppliersSerializer, SuppliersSerializer, CreateUpdateProductSerializer, \
    ProductSerializer, CreateUpdateMenuSerializer, MenuSerializer

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

class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    model = Product
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_serializer_class(self):
        classes = {

            "create": CreateUpdateProductSerializer,
            "partial_update": CreateUpdateProductSerializer,
        }
        return classes.get(self.action, ProductSerializer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        cost = validated_data.get('unit_cost', None)
        quantity = validated_data.get('quantity', None)
        total_cost = self.cal_cost(cost, quantity)

        validated_data['total_cost'] = total_cost

        created_product = serializer.save()
        return Response({'id':created_product.id,'total_cost':created_product.total_cost}, status=status.HTTP_201_CREATED)

    @staticmethod
    def cal_cost(cost, quantity):
        if cost is None or quantity is None:
            raise ValidationError('Нет кол-во или цены')
        return cost * quantity

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        cost = validated_data.get('unit_cost', instance.unit_cost)
        quantity = validated_data.get('quantity', instance.quantity)
        total_cost = self.cal_cost(cost, quantity)

        validated_data['total_cost'] = total_cost

        updated_product = serializer.save()
        return Response({'id': updated_product.id, 'total_cost': updated_product.total_cost}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MenuModelViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    model = Menu
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_serializer_class(self):
        classes = {
            "create": CreateUpdateMenuSerializer,
            "partial_update": CreateUpdateMenuSerializer,
        }
        return classes.get(self.action, MenuSerializer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        menu = serializer.save()
        return Response({'id': menu.id}, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        menu = serializer.save()
        return Response({'id': menu.id}, status=status.HTTP_200_OK)


