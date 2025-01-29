from django.urls import path
from Product import views

urlpatterns = [
    path('product/', views.product),
    path('product/<int:pk>', views.product_detail)
]
