from django.urls import path
from . import views


# URLConfig

urlpatterns = [
    path('products/', views.product_list),
    path('product/<int:pk>', views.product_detail),
]