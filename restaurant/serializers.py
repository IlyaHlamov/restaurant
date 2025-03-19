
from rest_framework import serializers

from restaurant.models import Supplier, Product, Menu, MenuProduct, Order, OrderMenu


class CreateUpdateSuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ('created_at', 'updated_at' )


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

    def get_created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M:%S')

    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%d.%m.%Y %H:%M:%S')

class CreateUpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at','total_cost' )


class ProductSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'

    def get_created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M:%S')

    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%d.%m.%Y %H:%M:%S')

class MenuProductSerializer(serializers.ModelSerializer):
        product_name = serializers.CharField(source='product.name', read_only=True)

        class Meta:
            model = MenuProduct
            fields = ['product_name', 'quantity']


class MenuSerializer(serializers.ModelSerializer):
    ingredient_names = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'created_at', 'updated_at', 'name', 'price', 'description', 'ingredient_names']

    def get_ingredient_names(self, obj):

        return [product.name for product in obj.ingredient.all()]

    def get_created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M:%S')

    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%d.%m.%Y %H:%M:%S')


class CreateUpdateMenuSerializer(serializers.ModelSerializer):
    ingredients = MenuProductSerializer(many=True)

    class Meta:
        model = Menu
        exclude = ('created_at', 'updated_at')

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        menu = Menu.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            MenuProduct.objects.create(menu=menu, **ingredient_data)
        return menu

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)

        instance.ingredient.clear()

        for ingredient_data in ingredients_data:
            MenuProduct.objects.create(menu=instance, **ingredient_data)

        return instance


