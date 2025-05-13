import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from tests.factories import (
    SupplierFactory,
    ProductFactory,
    MenuFactory,
    OrderFactory,
    MenuProductFactory
)


@pytest.mark.django_db
class TestSupplierViewSet:
    def setup_method(self, method):
        self.client = APIClient()
        self.supplier = SupplierFactory()

    def test_retrieve_supplier(self):
        url = reverse('restourant:supplier-detail', kwargs={'pk': self.supplier.pk})
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data['name'] == self.supplier.name

    def test_list_suppliers(self):
        url = reverse('restourant:supplier-list')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_supplier(self):
        url = reverse('restourant:supplier-list')
        data = {
            'name': 'New Supplier',
            'address': '123 Test St',
            'mail': 'test@example.com',
            'phone_number': '+1234567890'
        }
        response = self.client.post(url, data)
        assert response.status_code == 201


@pytest.mark.django_db
class TestProductViewSet:
    def setup_method(self, method):
        self.client = APIClient()
        self.supplier = SupplierFactory()
        self.product = ProductFactory(supplier=self.supplier)

    def test_create_product(self):
        url = reverse('restourant:Product-list')
        data = {
            'name': 'New Product',
            'unit_of_measure': 'KG',
            'quantity': 5,
            'unit_cost': '10.50',
            'supplier': self.supplier.id
        }
        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_partial_update_product(self):
        url = reverse('restourant:Product-detail', kwargs={'pk': self.product.pk})
        data = {'quantity': 20}
        response = self.client.patch(url, data)
        assert response.status_code == 200


@pytest.mark.django_db
class TestMenuViewSet:
    def setup_method(self, method):
        self.client = APIClient()
        self.product = ProductFactory()
        self.menu = MenuFactory()
        MenuProductFactory(menu=self.menu, product=self.product)

    def test_menu_list(self):
        url = reverse('restourant:Menu-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) > 0
        assert 'ingredient_names' in response.data[0]

    def test_create_menu(self):
        url = reverse('restourant:Menu-list')
        data = {
            'name': 'New Menu',
            'price': '30.00',
            'description': 'New menu description',
            'ingredients': [{
                'product': self.product.id,
                'quantity': 3
            }]
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 201