from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import status
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin,UpdateModelMixin,RetrieveModelMixin, ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminOrReadOnly
from .pagination import DefaultPagination
from .models import Product, Collection,OrderItem,Review,Cart,CartItem, Customer
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer, CustomerSerializer

# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    filterset_fileds = ['collection_id']
    search_fields = ['title', 'description']
    ordering_fields = ['unit-price', 'last_updated']

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id = collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}
    

    def destroy(self, request, *args, **kwargs):
          if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response({'error':'product cannot be deleted because it is associated with order item'}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
          
          return super().destroy(request, *args, **kwargs)

    

class CollectionViewSet(ModelViewSet):

    queryset = Collection.objects.annotate(products_count = Count('featured_product')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted'})
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id =self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,ListModelMixin,GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    

class CartItemViewSet(ModelViewSet):
   http_method_names = ['get','post','patch','delete']
   
   def get_queryset(self):
        return  CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])
   
   def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
   def get_serializer_context(self):
       return {'cart_id': self.kwargs['cart_pk']}
   

# class CustomerViewSet(CreateModelMixin, RetrieveModelMixin,UpdateModelMixin, GenericViewSet):
class CustomerViewSet(ModelViewSet):
    queryset =  Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['GET','PUT'])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer =  CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    


    
   




    


# ------------------- Class based api view using ListCreateApiView --------------------------------
# class ProductList(ListCreateAPIView):

#     def get_queryset(self):
#         return  Product.objects.all()
#         serializer = ProductSerializer(queryset, many=True,context={'request': request})
    
#     def get_serializer_class(self):
#         return ProductSerializer 
    
#     def get_serializer_context(self):
#         return {'request': self.request}
    

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()

#     serializer_class = ProductSerializer
        
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitem_set.count() > 0:
#             return Response({'error':'product cannot be deleted because it is associated with order item'}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)
    

# class CollectionList(ListCreateAPIView):

#     def get_queryset(self):
#         return Collection.objects.annotate(products_count = Count('featured_product')).all()
    
#     def get_serializer_class(self):
#         return CollectionSerializer
    

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     pass
#     queryset = Collection.objects.annotate(products_count = Count('product'))
#     serializer_class = CollectionSerializer

#     def delete(self, request,pk):
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted'})
#         collection.delete()
#         return super().delete(status=status.HTTP_204_NO_CONTENT) 

#  ----------------- Class based Api view with APIView Module ----------------
    

# class ProductList(APIView):

#     def get(self, request):
#         queryset = Product.objects.all()
#         serializer = ProductSerializer(queryset, many=True,context={'request': request})
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         print(serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class ProductDetail(APIView):

#     def get(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitem_set.count() > 0:
#             return Response({'error':'product cannot be deleted because it is associated with order item'}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)


# class CollectionList(APIView):

#     pass


# ---- Function based api view

# @api_view(['GET', 'POST'])
# def product_list(request):

#     if request.method == 'GET':
#         queryset = Product.objects.all()
#         serializer = ProductSerializer(queryset, many=True)
#         return Response(serializer.data)  
    
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         print(serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif  request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.orderitem_set.count() > 0:
#             return Response({'error':'product cannot be deleted because it is associated with order item'}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)

 

# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(
#             products_count = Count('products')).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count = Count('products')), pk=pk)

#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exceptions=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_200_OK)
