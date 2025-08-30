# Django REST API with CSRF Protection & Session Authentication

A comprehensive Django REST API for managing categories and products with **CSRF-Protected Session Authentication**.

## � Security Features

- ✅ **CSRF Protection**: All state-changing requests require CSRF tokens
- ✅ **Session-based Authentication**: Cookie-only authentication (no token headers)
- ✅ **Secure Cookies**: HttpOnly and SameSite flags enabled
- ✅ **User registration and login**: Complete user management
- ✅ **Protected API endpoints**: Authentication required for all CRUD operations
- ✅ **Input validation**: Data validation for all models
- ✅ **CORS configuration**: Cross-origin request support
- ✅ **Swagger documentation**: Interactive API documentation with auth support

### Security Settings Implemented:
```python
# CSRF Protection
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = False  # True in production
CSRF_COOKIE_SAMESITE = 'Lax'

# Session Security  
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # True in production
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 3600  # 1 hour

# Additional Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

## 🚀 Quick Start

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 4. Populate Sample Data
```bash
python manage.py populate_db
```

### 5. Start Development Server
```bash
python manage.py runserver
```

## 🔑 Authentication Endpoints

### Get CSRF Token (Required First)
```http
GET /api/auth/csrf/
```
**Response:**
```json
{
    "csrf_token": "csrf_token_value",
    "message": "CSRF token set in cookie"
}
```

### Register New User
```http
POST /api/auth/register/
X-CSRFToken: your_csrf_token_here
Content-Type: application/json

{
    "username": "your_username", 
    "password": "your_password",
    "email": "your_email@example.com"
}
```

**Response:**
```json
{
    "user_id": 1,
    "username": "your_username",
    "message": "User registered and logged in successfully",
    "csrf_token": "csrf_token_value"
}
```

### Login
```http
POST /api/auth/login/
X-CSRFToken: your_csrf_token_here
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "user_id": 1,
    "username": "your_username", 
    "message": "Successfully logged in",
    "csrf_token": "csrf_token_value"
}
```

### Logout
```http
POST /api/auth/logout/
X-CSRFToken: your_csrf_token_here
```

## 📡 API Usage

### CSRF Protection
All POST/PUT/PATCH/DELETE requests require a CSRF token in the header:

```http
X-CSRFToken: your_csrf_token_here
```

### Session Authentication
Authentication is handled via session cookies. After login, session cookies are automatically included in requests.

### Example API Calls

#### Get CSRF Token First
```bash
curl -c cookies.txt http://127.0.0.1:8000/api/auth/csrf/
```

#### Get All Products (Authenticated with CSRF)
```bash
curl -b cookies.txt -H "X-CSRFToken: your_token_here" http://127.0.0.1:8000/api/products/
```

#### Create New Product (Authenticated with CSRF)
```bash
curl -X POST \
  -b cookies.txt \
  -H "X-CSRFToken: your_token_here" \
  -H "Content-Type: application/json" \
  -d '{"name":"New Product","description":"Product description","price":19.99,"category":1,"stock_quantity":100}' \
  http://127.0.0.1:8000/api/products/
```

## 📊 API Endpoints

### Authentication
- `GET /api/auth/csrf/` - Get CSRF token (no auth required)
- `POST /api/auth/register/` - Register new user (requires CSRF)
- `POST /api/auth/login/` - Login user (requires CSRF) 
- `POST /api/auth/logout/` - Logout user (requires auth + CSRF)

### Base URL
`http://127.0.0.1:8000/api/`

### Swagger/OpenAPI Documentation
- **Swagger UI**: `http://127.0.0.1:8000/api/docs/` - Interactive API documentation
- **ReDoc**: `http://127.0.0.1:8000/api/redoc/` - Alternative documentation interface
- **OpenAPI Schema**: `http://127.0.0.1:8000/api/schema/` - Raw OpenAPI schema

### Available Endpoints

### Categories (All require authentication)
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create new category
- `GET /api/categories/{id}/` - Get category details
- `PUT /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

### Products (All require authentication)
- `GET /api/products/` - List all products
- `GET /api/products/?category=1` - Filter by category
- `GET /api/products/?is_active=true` - Filter active products
- `POST /api/products/` - Create new product
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product

### Other
- `GET /api/` - API overview (no auth required)
- `GET /api/stats/` - API statistics (requires auth)

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

## 🧪 Testing

### Test CSRF Authentication
Run the CSRF authentication test script:
```bash
python test_csrf.py
```

### Test Basic Authentication (Legacy)
```bash
python test_auth.py
```

### Manual Testing
You can test the API using:
- curl commands (see examples above)
- Postman or similar API testing tools
- Django REST Framework's browsable API interface
- Python requests library

Visit `http://127.0.0.1:8000/api/` in your browser to see the API overview.
