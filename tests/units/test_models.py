import pytest
from django.core.exceptions import ValidationError
from restaurant.models import Product, Menu, Order
from tests.factories import ProductFactory, MenuFactory, OrderFactory
from datetime import timedelta


@pytest.mark.django_db
class TestProductModel:
    def test_product_creation(self):
        product = ProductFactory(name="Test Product", unit_of_measure='KG')
        assert product.name == "Test Product"
        assert product.unit_of_measure == "KG"
        assert product.total_cost == product.unit_cost * product.quantity
        assert str(product) == "Test Product"

    def test_product_unit_cost_validation(self):
        product = ProductFactory.build(unit_cost=-10)
        with pytest.raises(ValidationError):
            product.full_clean()


@pytest.mark.django_db
class TestMenuModel:
    def test_menu_creation(self):
        menu = MenuFactory(name="Test Menu")
        assert menu.name == "Test Menu"
        assert str(menu) == "Test Menu"

    def test_add_ingredients(self):
        menu = MenuFactory()
        product = ProductFactory()
        # Добавляем quantity
        menu.ingredient.add(product, through_defaults={'quantity': 1})
        assert product in menu.ingredient.all()

# @pytest.mark.django_db
# class TestOrderModel:
#     def test_order_creation(self):
#         order = OrderFactory(table=5)
#         assert order.table == 5
#         assert order.status in ['PENDING', 'COMPLETED', 'CANCELLED']
#         assert str(order) == f"Order {order.id} - Table 5"
#
#     def test_order_reservation_time_future(self):
#         from django.utils import timezone
#         order = OrderFactory.build(reservation_time=timezone.now() - timedelta(days=1))
#         with pytest.raises(ValidationError):
#             order.full_clean()