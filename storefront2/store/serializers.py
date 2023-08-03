from decimal import Decimal
from store.models import Product, Collection, Collection,Review
from rest_framework import serializers


# class CollectionSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title','slug', 'inventory', 'unit_price', 'collection']


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title','products_count']
        
    products_count = serializers.IntegerField(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','date','name','description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id['product_id'], **validated_data)
