import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from tests.factories import SupplierFactory


@pytest.mark.django_db
class TestRestaurantFlow:
    def test_full_flow(self):
        client = APIClient()

        # 1. Create supplier
        supplier_url = reverse('restourant:supplier-list')
        supplier_data = {
            'name': 'Test Supplier',
            'address': '123 Test St',
            'mail': 'supplier@test.com',
            'phone_number': '+1234567890'  # Убедитесь, что длина <= 20
        }
        supplier_response = client.post(supplier_url, supplier_data)
        assert supplier_response.status_code == 201
        supplier_id = supplier_response.data['id']

        # 2. Create product
        product_url = reverse('restourant:Product-list')
        product_data = {
            'name': 'Test Product',
            'unit_of_measure': 'KG',
            'quantity': 10,
            'unit_cost': '5.99',  # Обязательно
            'supplier': supplier_id
        }
        product_response = client.post(product_url, product_data)
        assert product_response.status_code == 201
        assert 'total_cost' in product_response.data  # Проверка вычисления

        # 3. Create menu
        menu_url = reverse('restourant:Menu-list')
        menu_data = {
            'name': 'Test Menu',
            'price': '25.99',
            'description': 'Test menu with product',
            'ingredients': [{
                'product': 'product_id',
                'quantity': 2
            }]
        }
        menu_response = client.post(menu_url, menu_data, format='json')
        assert menu_response.status_code == 201
        menu_id = menu_response.data['id']

        # 4. Verify menu contains product
        menu_detail_url = reverse('restourant:Menu', kwargs={'pk': menu_id})
        menu_detail_response = client.get(menu_detail_url)
        assert menu_detail_response.status_code == 200
        assert 'Test Product' in menu_detail_response.data['ingredient_names']