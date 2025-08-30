from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductCreateUpdateSerializer

# Create your views here.

# Category Views
@extend_schema_view(
    get=extend_schema(
        summary="List all categories",
        description="Get a list of all categories with product counts",
    ),
    post=extend_schema(
        summary="Create a new category",
        description="Create a new category with name and description",
    ),
)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema_view(
    get=extend_schema(
        summary="Get category details",
        description="Get detailed information about a specific category",
    ),
    put=extend_schema(
        summary="Update category",
        description="Update all fields of a specific category",
    ),
    patch=extend_schema(
        summary="Partially update category",
        description="Update specific fields of a category",
    ),
    delete=extend_schema(
        summary="Delete category",
        description="Delete a specific category",
    ),
)
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Product Views
@extend_schema_view(
    get=extend_schema(
        summary="List all products",
        description="Get a list of all products with optional filtering by category and active status",
        parameters=[
            OpenApiParameter(name='category', description='Filter by category ID', required=False, type=int),
            OpenApiParameter(name='is_active', description='Filter by active status', required=False, type=bool),
        ],
    ),
    post=extend_schema(
        summary="Create a new product",
        description="Create a new product with all required information",
    ),
)
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductSerializer
    
    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
            
        return queryset


@extend_schema_view(
    get=extend_schema(
        summary="Get product details",
        description="Get detailed information about a specific product",
    ),
    put=extend_schema(
        summary="Update product",
        description="Update all fields of a specific product",
    ),
    patch=extend_schema(
        summary="Partially update product",
        description="Update specific fields of a product",
    ),
    delete=extend_schema(
        summary="Delete product",
        description="Delete a specific product",
    ),
)
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateUpdateSerializer
        return ProductSerializer


# Function-based views for additional endpoints
@extend_schema(
    summary="API Overview",
    description="Get an overview of all available API endpoints",
    responses={200: {"description": "API endpoints overview"}},
)
@api_view(['GET'])
def api_overview(request):
    """
    API Overview endpoint that lists all available endpoints
    """
    api_urls = {
        'API Overview': '/api/',
        'Swagger Documentation': '/api/docs/',
        'ReDoc Documentation': '/api/redoc/',
        'Categories': {
            'List/Create': '/api/categories/',
            'Detail': '/api/categories/<int:pk>/',
        },
        'Products': {
            'List/Create': '/api/products/',
            'Detail': '/api/products/<int:pk>/',
            'By Category': '/api/products/?category=<category_id>',
            'Active Only': '/api/products/?is_active=true',
        },
        'Statistics': '/api/stats/',
    }
    return Response(api_urls)


@extend_schema(
    summary="API Statistics",
    description="Get statistical information about the API data including counts of categories, products, and stock status",
    responses={200: {"description": "API statistics"}},
)
@api_view(['GET'])
def api_statistics(request):
    """
    Get basic statistics about the API data
    """
    stats = {
        'total_categories': Category.objects.count(),
        'total_products': Product.objects.count(),
        'active_products': Product.objects.filter(is_active=True).count(),
        'inactive_products': Product.objects.filter(is_active=False).count(),
        'out_of_stock_products': Product.objects.filter(stock_quantity=0).count(),
    }
    return Response(stats)
