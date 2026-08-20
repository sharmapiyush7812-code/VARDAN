# Quick Start Guide

Get VARDAN backend and frontend running in 5 minutes.

## Prerequisites

- Python 3.9+
- Node.js 18+
- Terminal/Command line access

## Backend Setup (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python3 -m venv env
source env/bin/activate    # Mac/Linux
# or: env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run Django server
python manage.py runserver 8000
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
```

## Frontend Setup (Terminal 2)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Expected output:
```
Local: http://localhost:5173/
```

## Test the API (Terminal 3)

```bash
# Test products endpoint
curl http://localhost:8000/api/products/

# Test signup
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "TestPass123",
    "phone": "9876543210"
  }'
```

## Key Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/products/ | No | List all products |
| POST | /api/auth/signup/ | No | Create account |
| POST | /api/auth/login/ | No | Login |
| GET | /api/auth/me/ | Yes | Current user |
| POST | /api/cart/add/ | Yes | Add to cart |
| GET | /api/cart/ | Yes | Get cart |
| POST | /api/wishlist/add/ | Yes | Add to wishlist |
| POST | /api/checkout/ | Yes | Create order |
| GET | /api/orders/ | Yes | User's orders |

## Default Test Account

After running signup, you have an account:
- Email: test@example.com
- Password: TestPass123
- Phone: 9876543210

## Project Structure

```
vardan/
├── backend/          # Django REST API
│   ├── api/          # API endpoints
│   ├── config/       # Django config
│   ├── data/         # JSON data storage
│   └── manage.py
├── frontend/         # React + Vite
│   ├── src/          # React components (TODO: Complete)
│   ├── index.html
│   └── package.json
└── README.md         # Full documentation
```

## What's Implemented

✅ Backend
- All 4 modules (Products, Auth, Cart, Orders)
- JWT authentication
- JSON storage with thread safety
- Complete API endpoints

✅ Frontend Setup
- Vite configuration
- Context providers (Auth, Cart, Wishlist)
- API service layer
- Basic styling

❌ Frontend Components
- Need to convert Index.html components to React
- See IMPLEMENTATION_GUIDE.md for details

## Common Issues

**Error: Port 8000 already in use**
```bash
python manage.py runserver 8001
```

**Error: npm not found**
- Install Node.js from nodejs.org

**Error: env/bin/activate not found**
- Make sure you're in the backend folder
- Run: `python3 -m venv env` first

**Error: ModuleNotFoundError**
- Activate virtual environment: `source env/bin/activate`
- Install requirements: `pip install -r requirements.txt`

## Next Steps

1. ✅ Backend is ready
2. ✅ API endpoints are working
3. ⏭️  Complete React components (see IMPLEMENTATION_GUIDE.md)
4. ⏭️  Test end-to-end flows
5. ⏭️  Deploy to production

## Documentation

- **README.md** - Full project documentation
- **IMPLEMENTATION_GUIDE.md** - Frontend component guide
- **Backend API** - http://localhost:8000/api/ (with DRF browsable API)

## Support

All endpoints return JSON responses with this format:

**Success:**
```json
{
  "success": true,
  "message": "Success",
  "data": { }
}
```

**Error:**
```json
{
  "success": false,
  "message": "Error message",
  "error": {
    "code": "ERROR_CODE",
    "message": "Detailed error"
  }
}
```

## Authentication Token

After login, you get a JWT token:
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user_id": "USR-xxxxx",
    "name": "Your Name"
  }
}
```

Use it in requests:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/cart/
```

Enjoy building! 🚀
