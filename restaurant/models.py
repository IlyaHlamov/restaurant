from django.db import models

class User(models.Model):
    USER_TYPE_CHOICES = [
        ('WAITER', 'Waiter'),
        ('MANAGER', 'Manager'),
        ('CHEF', 'Chef'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100,unique=True)
    address = models.CharField(max_length=200)
    mail = models.EmailField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    measure_TYPE_CHOICES = [
        ('KG', 'kg'),
        ('ML', 'ml'),
        ('UNIT', 'unit'),
    ]
    name = models.CharField(max_length=100,unique=True)
    unit_of_measure = models.CharField(max_length=50, choices=measure_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=100,unique=True)
    ingredient = models.ManyToManyField(Product, through= 'MenuProduct')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    #img = models.ImageField(upload_to='menu_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class MenuProduct(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.menu.name} - {self.product.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    table = models.IntegerField()
    reservation_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    waiter = models.ForeignKey(User, on_delete=models.CASCADE)
    full_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='Pending')
    menus = models.ManyToManyField(Menu, through='OrderMenu')

    def __str__(self):
        return f"Order {self.id} - Table {self.table}"

class OrderMenu(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.order.id} - {self.menu.name}"