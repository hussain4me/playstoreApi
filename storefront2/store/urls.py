from django.urls import path
from . import views


# URLConfig

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('product/<int:pk>', views.ProductDetail.as_view()),
    path('collections/', views.CollectionList.as_view()),
]