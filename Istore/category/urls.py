from django.urls import path
from category import views

urlpatterns = [
    path('category/', views.category),
    path('category/<int:pk>', views.category_detail)
]