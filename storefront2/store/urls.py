from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers
from . import views
from pprint import pprint


# URLConfig

# router = SimpleRouter()
# router = DefaultRouter()
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename = 'product-reviews' )

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename = 'cart-item' )

# pprint(router.urls)
# pprint(products_router.urls)

urlpatterns = router.urls + products_router.urls + cart_router.urls
# urlpatterns = router.urls + cart_router.urls

# urlpatterns = [
    # path('products/', views.ProductList.as_view()),
    # path('product/<int:pk>', views.ProductDetail.as_view()),
    # path('collections/', views.CollectionList.as_view()),
    # path('product/<int:pk>', views.CollectionDetail.as_view()),
# ]