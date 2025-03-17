from rest_framework import serializers

from restaurant.models import Supplier


class CreateUpdateSuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ('created_at', 'updated_at' )


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'