from decimal import Decimal
from store.models import Product, Collection, Collection
from rest_framework import serializers


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title','slug', 'inventory', 'unit_price', 'collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    # price_with_tax = serializers.SerializerMethodField()
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )
    # collection = CollectionSerializer()

    # def get_calculate_tax(self, product: Product ):
    #     return product.unit_price * Decimal(1.1)


    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product
    
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance
