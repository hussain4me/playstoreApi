from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views
from pprint import pprint


# URLConfig

# router = SimpleRouter()
router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
# pprint(router.urls)

urlpatterns = router.urls

# urlpatterns = [
    # path('products/', views.ProductList.as_view()),
    # path('product/<int:pk>', views.ProductDetail.as_view()),
    # path('collections/', views.CollectionList.as_view()),
    # path('product/<int:pk>', views.CollectionDetail.as_view()),
# ]