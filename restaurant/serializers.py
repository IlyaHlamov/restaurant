from rest_framework import serializers

from restaurant.models import Supplier, Product


class CreateUpdateSuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ('created_at', 'updated_at' )


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class CreateUpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at','total_cost' )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'