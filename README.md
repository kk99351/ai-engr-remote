# Django REST API Project

This is a Django REST API project that provides endpoints for managing categories and products.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Base URL
`http://127.0.0.1:8000/api/`

### Swagger/OpenAPI Documentation
- **Swagger UI**: `http://127.0.0.1:8000/api/docs/` - Interactive API documentation
- **ReDoc**: `http://127.0.0.1:8000/api/redoc/` - Alternative documentation interface
- **OpenAPI Schema**: `http://127.0.0.1:8000/api/schema/` - Raw OpenAPI schema

### Available Endpoints

#### API Overview
- **GET** `/api/` - Get API overview with all available endpoints

#### Categories
- **GET** `/api/categories/` - List all categories
- **POST** `/api/categories/` - Create a new category
- **GET** `/api/categories/{id}/` - Get category details
- **PUT** `/api/categories/{id}/` - Update category
- **PATCH** `/api/categories/{id}/` - Partial update category
- **DELETE** `/api/categories/{id}/` - Delete category

#### Products
- **GET** `/api/products/` - List all products
- **POST** `/api/products/` - Create a new product
- **GET** `/api/products/{id}/` - Get product details
- **PUT** `/api/products/{id}/` - Update product
- **PATCH** `/api/products/{id}/` - Partial update product
- **DELETE** `/api/products/{id}/` - Delete product

#### Query Parameters for Products
- `category` - Filter products by category ID
- `is_active` - Filter by active status (true/false)

Examples:
- `/api/products/?category=1` - Get products from category 1
- `/api/products/?is_active=true` - Get only active products

#### Statistics
- **GET** `/api/stats/` - Get API statistics

## Data Models

### Category
```json
{
  "id": 1,
  "name": "Electronics",
  "description": "Electronic products and gadgets",
  "products_count": 5,
  "created_at": "2025-08-30T10:00:00Z",
  "updated_at": "2025-08-30T10:00:00Z"
}
```

### Product
```json
{
  "id": 1,
  "name": "iPhone 15",
  "description": "Latest iPhone model",
  "price": "999.99",
  "category": 1,
  "category_name": "Electronics",
  "is_active": true,
  "stock_quantity": 10,
  "created_at": "2025-08-30T10:00:00Z",
  "updated_at": "2025-08-30T10:00:00Z"
}
```

## Example API Calls

### Create Category
```bash
curl -X POST http://127.0.0.1:8000/api/categories/ \
     -H "Content-Type: application/json" \
     -d '{"name": "Electronics", "description": "Electronic products"}'
```

### Create Product
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
     -H "Content-Type: application/json" \
     -d '{
       "name": "iPhone 15",
       "description": "Latest iPhone model",
       "price": "999.99",
       "category": 1,
       "is_active": true,
       "stock_quantity": 10
     }'
```

### Get All Products
```bash
curl http://127.0.0.1:8000/api/products/
```

## Admin Interface

Access the Django admin interface at: `http://127.0.0.1:8000/admin/`

You can manage categories and products through the admin interface after creating a superuser.

## Features

- Full CRUD operations for Categories and Products
- Product filtering by category and active status
- Data validation (price > 0, stock_quantity >= 0)
- Related field serialization (category name in product response)
- API statistics endpoint
- Django admin integration
- CORS support for frontend integration

## Testing the API

You can test the API using:
- curl commands (see examples above)
- Postman or similar API testing tools
- Django REST Framework's browsable API interface
- Python requests library

Visit `http://127.0.0.1:8000/api/` in your browser to see the API overview and use the browsable API interface.
