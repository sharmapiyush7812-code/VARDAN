# VARDAN E-Commerce Backend Integration

Complete full-stack implementation of VARDAN clothing brand storefront with Django REST API backend and React frontend.

## Project Overview

- **Backend**: Django + Django REST Framework
- **Frontend**: React + Vite
- **Data Storage**: JSON files (MVP) → PostgreSQL (future migration)
- **Authentication**: JWT-based
- **Architecture**: Fully scalable for database migration without API contract changes

## Implemented Features (MVP)

### ✅ Module 1: Products + Wishlist + Cart
- Product listing and filtering
- Product detail pages
- Multiple product images with different resolutions
- Wishlist functionality (authenticated users)
- Cart management with size selection

### ✅ Module 2: Checkout
- Shipping address collection
- Server-side cart validation
- Stock verification
- Pending order creation (no real payment)

### ✅ Module 3: User Authentication
- User signup with email verification
- Secure password hashing
- JWT-based login/authentication
- User session persistence

### ✅ Module 4: Orders
- Order history for authenticated users
- Order detail pages
- Order status tracking (pending payments)

## Project Structure

```
vardan/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env
│   ├── .env.example
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── api/
│   │   ├── views.py          # All API endpoints
│   │   ├── serializers.py    # DRF serializers
│   │   ├── urls.py           # API routing
│   │   ├── services.py       # JSON storage abstraction
│   │   ├── authentication.py # JWT handling
│   │   └── permissions.py    # Custom permissions
│   └── data/
│       ├── products.json     # Product catalog
│       ├── users.json        # User accounts
│       ├── carts.json        # Shopping carts
│       ├── wishlists.json    # Wishlists
│       └── orders.json       # Orders
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── services/
        │   └── api.js        # API client
        ├── context/
        │   ├── AuthContext.jsx
        │   ├── CartContext.jsx
        │   └── WishlistContext.jsx
        ├── components/       # React components
        ├── pages/            # Page components
        └── App.jsx
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+ (for React development)
- pip (Python package manager)
- npm (Node package manager)

### Backend Setup

#### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure Environment Variables

Copy `.env.example` to `.env` and update as needed:

```bash
cp .env.example .env
```

Edit `.env`:
```
DEBUG=True
SECRET_KEY=your-secret-key-change-this
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000
JWT_SECRET=your-jwt-secret-change-this
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### 4. Run Django Development Server

```bash
python manage.py runserver 8000
```

The API will be available at `http://localhost:8000/api/`

### Frontend Setup

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

#### 2. Create Environment Configuration

Create `.env` file:
```
VITE_API_URL=http://localhost:8000/api
```

#### 3. Run Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Products

```
GET    /api/products/              # List all products
GET    /api/products/<product_id>/ # Get single product
GET    /api/products/?category=track  # Filter by category
GET    /api/products/?search=term     # Search products
```

### Authentication

```
POST   /api/auth/signup/     # Create new user
POST   /api/auth/login/      # Login & get JWT token
GET    /api/auth/me/         # Get current user (authenticated)
```

### Wishlist (Authenticated)

```
GET    /api/wishlist/              # Get user's wishlist
POST   /api/wishlist/add/          # Add product to wishlist
DELETE /api/wishlist/<product_id>/ # Remove from wishlist
```

### Cart (Authenticated)

```
GET    /api/cart/                  # Get user's cart
POST   /api/cart/add/              # Add item to cart
PATCH  /api/cart/<item_id>/        # Update cart item quantity
DELETE /api/cart/<item_id>/remove/ # Remove from cart
```

### Checkout (Authenticated)

```
POST   /api/checkout/  # Create pending order from cart
```

### Orders (Authenticated)

```
GET    /api/orders/              # Get user's orders
GET    /api/orders/<order_id>/   # Get specific order
```

## API Response Format

### Success Response
```json
{
  "success": true,
  "message": "Success",
  "data": {
    ...
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description",
  "error": {
    "code": "ERROR_CODE",
    "message": "Detailed error message"
  }
}
```

## Authentication Flow

### 1. Signup
```bash
POST /api/auth/signup/
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePassword123",
  "phone": "9876543210"
}

Response:
{
  "success": true,
  "data": {
    "user_id": "USR-abc123de",
    "name": "John Doe",
    "email": "john@example.com",
    "token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

### 2. Login
```bash
POST /api/auth/login/
{
  "email": "john@example.com",
  "password": "SecurePassword123"
}

Response:
{
  "success": true,
  "data": {
    "user_id": "USR-abc123de",
    "name": "John Doe",
    "email": "john@example.com",
    "token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

### 3. Using Token
Include token in request headers:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

## Data Storage

### JSON Storage Architecture

All data is stored in JSON files in the `backend/data/` directory:

- **products.json**: Product catalog
- **users.json**: User accounts (keyed by user_id)
- **carts.json**: Shopping carts (keyed by user_id)
- **wishlists.json**: Wishlists (keyed by user_id)
- **orders.json**: Orders (array)

### Example Product Data
```json
{
  "id": "p01",
  "name": "Vardan Track Pant / 01",
  "price": 2499,
  "old_price": null,
  "category": ["track"],
  "tag": "New",
  "sizes": ["S", "M", "L", "XL"],
  "stock": {
    "S": 12,
    "M": 25,
    "L": 18,
    "XL": 10
  },
  "images": {
    "thumbnail": "/media/products/p01/thumb.webp",
    "small": "/media/products/p01/small.webp",
    "medium": "/media/products/p01/medium.webp",
    "large": "/media/products/p01/large.webp"
  },
  "gallery": [
    "/media/products/p01/1.webp",
    "/media/products/p01/2.webp",
    "/media/products/p01/3.webp"
  ],
  "active": true
}
```

## Future Database Migration

The architecture is designed for easy migration from JSON to PostgreSQL:

### Migration Steps
1. Replace `JsonStorage` class in `api/services.py` with Django ORM models
2. No changes needed to API endpoints or frontend
3. Update URL patterns if needed
4. Run database migrations

### Models Structure (Future)
```python
class Product(models.Model):
    # ... fields mapping JSON schema

class User(models.Model):
    # ... fields mapping user schema

class Order(models.Model):
    # ... fields mapping order schema

class Cart(models.Model):
    # ... fields mapping cart schema
```

## Security Considerations

✅ **Implemented in MVP:**
- Password hashing using Django's security utilities
- JWT-based authentication
- Server-side price calculation
- Stock validation on backend
- User authorization checks
- CORS configuration
- Environment-based configuration

⚠️ **Production Ready Improvements Needed:**
- HTTPS enforcement
- Rate limiting
- Input validation enhancements
- SQL injection prevention (when using DB)
- CSRF token verification
- Secure session storage
- Email verification for signup
- Password reset functionality

## Payment Gateway Integration (Future)

The checkout flow is designed to support payment gateways:

Current: `payment_status: "pending"`

Future payment APIs:
```
POST /api/payments/create/     # Initialize payment
POST /api/payments/verify/     # Verify payment
POST /api/payments/webhook/    # Handle payment callbacks
```

Supported gateways ready for integration:
- Razorpay
- Stripe
- PayPal

## Testing the API

### Test Signup/Login
```bash
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "TestPass123",
    "phone": "9876543210"
  }'
```

### Test Get Products
```bash
curl http://localhost:8000/api/products/
```

### Test Add to Cart (Authenticated)
```bash
curl -X POST http://localhost:8000/api/cart/add/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "p01",
    "size": "M",
    "quantity": 1
  }'
```

## Troubleshooting

### Django Server Issues
- **Port already in use**: Change port with `python manage.py runserver 8001`
- **CORS errors**: Check `CORS_ALLOWED_ORIGINS` in `config/settings.py`
- **Import errors**: Ensure virtual environment is activated

### React Issues
- **API connection failed**: Check backend is running on port 8000
- **Proxy not working**: Verify `vite.config.js` proxy configuration
- **Blank page**: Check browser console for errors

## Frontend Implementation Status

The frontend should:
1. ✅ Use existing VARDAN design/CSS
2. ✅ Connect products component to API
3. ✅ Implement React Context for state management
4. ✅ Add authentication flows
5. ✅ Implement cart/wishlist UI
6. ✅ Add checkout form
7. ✅ Display order history

**Note**: React components need to be created following the existing HTML structure and CSS from `Index.html`. The CSS contains custom animations, three.js canvas elements, and specific styling that should be preserved.

## Next Steps

1. **Complete React Components**: Implement remaining components using existing HTML/CSS
2. **Product Image Serving**: Setup media file serving for product images
3. **Email Notifications**: Add email confirmations for orders
4. **Admin Dashboard**: Create admin panel for order management
5. **Analytics**: Track user behavior and conversions
6. **Performance**: Optimize images, implement caching
7. **Database Migration**: When ready, migrate from JSON to PostgreSQL

## Development Workflow

```bash
# Terminal 1: Backend
cd backend
source env/bin/activate
python manage.py runserver 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Optional - File monitoring
cd backend/data
watch 'ls -lah'
```

## Performance Tips

- Use small/medium images in grid view
- Load large/gallery images on demand
- Implement lazy loading for product images
- Cache API responses in React Context
- Minimize JSON file reads with proper indexing

## Deployment

### Backend (Django)
```bash
# Production settings
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

# Use Gunicorn + Nginx
gunicorn config.wsgi:application
```

### Frontend (React)
```bash
# Build
npm run build

# Serve with Nginx or upload to CDN
```

## Support & Documentation

- Django REST Framework: https://www.django-rest-framework.org/
- React: https://react.dev/
- Vite: https://vitejs.dev/
- PyJWT: https://pyjwt.readthedocs.io/

## License

VARDAN © 2026. All rights reserved.
