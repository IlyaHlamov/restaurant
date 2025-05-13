import factory
import django.contrib.auth.models
from restaurant.models import Supplier, Product, Menu, MenuProduct, Order, OrderMenu
import random
from datetime import datetime, timedelta


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    name = factory.Sequence(lambda n: f'supplier {n}')
    address = factory.Faker('address')
    mail = factory.Faker('email')
    phone_number = factory.Faker('msisdn')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'roduct {n}')
    unit_of_measure = factory.Iterator(['KG', 'ML', 'UNIT'])
    quantity = factory.Faker('random_int', min=1, max=100)
    unit_cost = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    supplier = factory.SubFactory(SupplierFactory)

    @factory.post_generation
    def set_total_cost(self, create, extracted, **kwargs):
        self.total_cost = self.unit_cost * self.quantity
        if create:
            self.save()


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu

    name = factory.Sequence(lambda n: f'Menu {n}')
    price = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    description = factory.Faker('text', max_nb_chars=200)


class MenuProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MenuProduct

    menu = factory.SubFactory(MenuFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 1


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    table = factory.Faker('random_int', min=1, max=20)
    reservation_time = factory.LazyFunction(lambda: datetime.now() + timedelta(days=1))
    waiter = factory.Faker('random_int', min=1, max=10)
    full_price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    status = factory.Iterator(['PENDING', 'COMPLETED', 'CANCELLED'])


class OrderMenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderMenu

    order = factory.SubFactory(OrderFactory)
    menu = factory.SubFactory(MenuFactory)
    quantity = factory.Faker('random_int', min=1, max=5)