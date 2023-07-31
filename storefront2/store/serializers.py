from decimal import Decimal
from store.models import Product, Collection, Collection
from rest_framework import serializers


class CollectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title','slug', 'inventory', 'unit_price', 'collection']


# class CollectionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Collection
#         fields = []

