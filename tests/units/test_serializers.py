import pytest
from rest_framework.exceptions import ValidationError
from restaurant.serializers import (
    CreateUpdateProductSerializer,
    ProductSerializer,
    CreateUpdateMenuSerializer,
    MenuSerializer
)
from tests.factories import ProductFactory, MenuFactory, MenuProductFactory,SupplierFactory


@pytest.mark.django_db
class TestProductSerializers:
    def test_create_product_serializer(self):
        supplier = SupplierFactory()
        data = {
            'name': 'Test Product',
            'unit_of_measure': 'KG',
            'quantity': 10,
            'unit_cost': '15.99',
            'supplier': supplier.id
        }
        serializer = CreateUpdateProductSerializer(data=data)
        assert serializer.is_valid()
        product = serializer.save()
        assert product.total_cost == 15.99 * 10

    def test_product_serializer_output(self):
        product = ProductFactory()
        serializer = ProductSerializer(product)
        assert 'created_at' in serializer.data
        assert 'updated_at' in serializer.data
        assert serializer.data['name'] == product.name


@pytest.mark.django_db
class TestMenuSerializers:
    def test_create_menu_serializer(self):
        product = ProductFactory()
        data = {
            'name': 'Test Menu',
            'price': '25.99',
            'description': 'Test description',
            'ingredients': [{
                'product': product.id,
                'quantity': 2
            }]
        }
        serializer = CreateUpdateMenuSerializer(data=data)
        assert serializer.is_valid()
        menu = serializer.save()
        assert menu.menuproduct_set.count() == 1

    def test_menu_serializer_output(self):
        menu = MenuFactory()
        MenuProductFactory.create_batch(2, menu=menu)
        serializer = MenuSerializer(menu)
        assert 'ingredient_names' in serializer.data
        assert len(serializer.data['ingredient_names']) == 2