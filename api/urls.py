from django.urls import path
from . import views

urlpatterns = [
    # API Overview
    path('', views.api_overview, name='api_overview'),
    
    # Category URLs
    path('categories/', views.CategoryListCreateView.as_view(), name='category_list_create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Product URLs
    path('products/', views.ProductListCreateView.as_view(), name='product_list_create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Statistics
    path('stats/', views.api_statistics, name='api_statistics'),
]
