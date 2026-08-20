from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .services import JsonStorage, StorageService
from .authentication import JWTAuthentication
from .serializers import (
    ProductSerializer, CartItemSerializer, WishlistSerializer,
    SignUpSerializer, LoginSerializer, CheckoutSerializer, OrderSerializer
)


def api_response(success=True, data=None, message='', error_code=None, http_status=200):
    """Standardized API response format."""
    response = {
        'success': success,
        'message': message,
    }
    if success:
        response['data'] = data or {}
    else:
        response['error'] = {
            'code': error_code or 'ERROR',
            'message': message
        }
    return Response(response, status=http_status)


# ===================== PRODUCT ENDPOINTS =====================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_products(request):
    """Get all products with optional filtering."""
    products = JsonStorage.read('products')
    
    # Filter by category if provided
    category = request.query_params.get('category')
    if category:
        products = [p for p in products if category in p.get('category', [])]
    
    # Filter by search term if provided
    search = request.query_params.get('search', '').lower()
    if search:
        products = [p for p in products if search in p.get('name', '').lower()]
    
    # Only return active products
    products = [p for p in products if p.get('active', True)]
    
    serializer = ProductSerializer(products, many=True)
    return api_response(data=serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_detail(request, product_id):
    """Get a specific product by ID."""
    product = JsonStorage.find_by_id('products', product_id)
    
    if not product:
        return api_response(
            success=False,
            message='Product not found',
            error_code='PRODUCT_NOT_FOUND',
            http_status=404
        )
    
    serializer = ProductSerializer(product)
    return api_response(data=serializer.data)


# ===================== WISHLIST ENDPOINTS =====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist(request):
    """Get user's wishlist."""
    user_id = JWTAuthentication.get_user_from_token(request)
    if not user_id:
        return api_response(
            success=False,
            message='Unauthorized',
            error_code='UNAUTHORIZED',
            http_status=401
        )
    
    wishlists = JsonStorage.read('wishlists')
    wishlist = wishlists.get(user_id, {'user_id': user_id, 'products': []})
    
    serializer = WishlistSerializer(wishlist)
    return api_response(data=serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    """Add a product to wishlist."""
    user_id = JWTAuthentication.get_user_from_token(request)
    if not user_id:
        return api_response(
            success=False,
            message='Unauthorized',
            error_code='UNAUTHORIZED',
            http_status=401
        )
    
    product_id = request.data.get('product_id')
    if not product_id:
        return api_response(
            success=False,
            message='product_id is required',
            error_code='MISSING_FIELD',
            http_status=400
        )
    
    # Verify product exists
    if not JsonStorage.find_by_id('products', product_id):
        return api_response(
            success=False,
            message='Product not found',
            error_code='PRODUCT_NOT_FOUND',
            http_status=404
        )
    
    wishlists = JsonStorage.read('wishlists')
    if not isinstance(wishlists, dict):
        wishlists = {}
    
    if user_id not in wishlists:
        wishlists[user_id] = {'user_id': user_id, 'products': []}
    
    if product_id not in wishlists[user_id]['products']:
        wishlists[user_id]['products'].append(product_id)
    
    JsonStorage.write('wishlists', wishlists)
    serializer = WishlistSerializer(wishlists[user_id])
    return api_response(data=serializer.data, message='Added to wishlist', http_status=201)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, product_id):
    """Remove a product from wishlist."""
    user_id = JWTAuthentication.get_user_from_token(request)
    if not user_id:
        return api_response(
            success=False,
            message='Unauthorized',
            error_code='UNAUTHORIZED',
            http_status=401
        )
    
    wishlists = JsonStorage.read('wishlists')
    if not isinstance(wishlists, dict):
        wishlists = {}
    
    if user_id in wishlists and product_id in wishlists[user_id]['products']:
        wishlists[user_id]['products'].remove(product_id)
        JsonStorage.write('wishlists', wishlists)
    
    wishlist = wishlists.get(user_id, {'user_id': user_id, 'products': []})
    serializer = WishlistSerializer(wishlist)
    return api_response(data=serializer.data, message='Removed from wishlist')


# ===================== CART ENDPOINTS =====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    """Get user's cart."""
    user_id = JWTAuthentication.get_user_from_token(request)
    if not user_id:
        return api_response(
            success=False,
            message='Unauthorized',
            error_code='UNAUTHORIZED',
            http_status=401
        )
    
    carts = JsonStorage.read('carts')
    if not isinstance(carts, dict):
        carts = {}
    
    cart_items = carts.get(user_id, [])
    
    # Calculate subtotal
    subtotal = sum(item.get('subtotal', 0) for item in cart_items)
    
    response_data = {
        'user_id': user_id,
        'items': cart_items,
        'subtotal': subtotal,
        'item_count': len(cart_items)
    }
    return api_response(data=response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """Add an item to cart."""
    user_id = JWTAuthentication.get_user_from_token(request)
    if not user_id:
        return api_response(
            success=False,
            message='Unauthorized',
            error_code='UNAUTHORIZED',
            http_status=401
        )
    
    serializer = CartItemSerializer(data=request.data)
    if not serializer.is_valid():
        return api_response(
            success=False,
            message='Invalid data',
            error_code='INVALID_DATA',
            http_status=400
        )
    
    product_id = serializer.validated_data['product_id']
    size = serializer.validated_data['size']
    quantity = serializer.validated_data['quantity']
    
    # Verify product exists
    product = JsonStorage.find_by_id('products', product_id)
    if not product:
        return api_response(
            success=False,
            message='Product not found',
            error_code='PRODUCT_NOT_FOUND',
            http_status=404
        )
    
    # Verify size is available
    if size not in product.get('sizes', []):
        return api_response(
            success=False,
            message='Invalid size',
            error_code='INVALID_SIZE',
            http_status=400
        )
    
    # Check stock
    stock = product.get('stock', {}).get(size, 0)
    if quantity > stock:
        return api_response(
            success=False,
            message=f'Only {stock} items available for this size',
            error_code='INSUFFICIENT_STOCK',
            http_status=400
        )
    
    carts = JsonStorage.read('carts')
    if not isinstance(carts, dict):
        carts = {}
    
    if user_id not in carts:
        carts[user_id] = []
    
    # Check if item already exists
    item_id = f"{product_id}-{size}"
    existing_item = next((item for item in carts[user_id] if item['id'] == item_id), None)
    
    unit_price = product['price']
    subtotal = unit_price * quantity
    
    if existing_item:
        existing_item['quantity'] += quantity
        existing_item['subtotal'] = existing_item['unit_price'] * existing_item['quantity']
    else:
        carts[user_id].append({
            'id': item_id,
            'product_id': product_id,
            'size': size,
            'quantity': quantity,
            'unit_price': unit_price,
            'subtotal': subtotal
        })
    
    JsonStorage.write('carts', carts)
    
    cart_items = carts[user_id]
    subtotal = sum(item['subtotal'] for item in cart_items)
    
    response_data = {
        'user_id': user_id,
        'items': cart_items,
        'subtotal': subtotal,
        'item_count': len(cart_items)
    }
    return api_response(data=response_data, message='Added to cart', http_status=201)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    """Update quantity of a cart item."""
    user_id = JWTAuthentication.get_user_from_token(request)
    if not user_id:
        return api_response(
            success=False,
            message='Unauthorized',
            error_code='UNAUTHORIZED',
            http_status=401
        )
    
    quantity = request.data.get('quantity')
    if quantity is None or quantity < 1:
        return api_response(
            success=False,
            message='Valid quantity is required',
            error_code='INVALID_QUANTITY',
            http_status=400
        )
    
    carts = JsonStorage.read('carts')
    if not isinstance(carts, dict):
        carts = {}
    
    if user_id not in carts:
        return api_response(
            success=False,
            message='Cart not found',
            error_code='CART_NOT_FOUND',
            http_status=404
        )
    
    item = next((i for i in carts[user_id] if i['id'] == item_id), None)
    if not item:
        return api_response(
            success=False,
            message='Item not found in cart',
            error_code='ITEM_NOT_FOUND',
            http_status=404
        )
    
    item['quantity'] = quantity
    item['subtotal'] = item['unit_price'] * quantity
    
    JsonStorage.write('carts', carts)
    
    cart_items = carts[user_id]
    subtotal = sum(item['subtotal'] for item in cart_items)
    
    response_data = {
        'user_id': user_id,
        'items': cart_items,
        'subtotal': subtotal,
        'item_count': len(cart_items)
    }
    return api_response(data=response_data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    """Remove an item from cart."""
    user_id = JWTAuthentication.get_user_from_token(request)
    if not user_id:
        return api_response(
            success=False,
            message='Unauthorized',
            error_code='UNAUTHORIZED',
            http_status=401
        )
    
    carts = JsonStorage.read('carts')
    if not isinstance(carts, dict):
        carts = {}
    
    if user_id not in carts:
        return api_response(
            success=False,
            message='Cart not found',
            error_code='CART_NOT_FOUND',
            http_status=404
        )
    
    carts[user_id] = [item for item in carts[user_id] if item['id'] != item_id]
    JsonStorage.write('carts', carts)
    
    cart_items = carts[user_id]
    subtotal = sum(item['subtotal'] for item in cart_items)
    
    response_data = {
        'user_id': user_id,
        'items': cart_items,
        'subtotal': subtotal,
        'item_count': len(cart_items)
    }
    return api_response(data=response_data)


# ===================== AUTHENTICATION ENDPOINTS =====================

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Create a new user account."""
    serializer = SignUpSerializer(data=request.data)
    if not serializer.is_valid():
        return api_response(
            success=False,
            message='Invalid data',
            error_code='INVALID_DATA',
            http_status=400
        )
    
    email = serializer.validated_data['email']
    
    # Check if user already exists
    users = JsonStorage.read('users')
    if not isinstance(users, dict):
        users = {}
    
    existing_user = next((u for u in users.values() if u['email'] == email), None)
    if existing_user:
        return api_response(
            success=False,
            message='Email already registered',
            error_code='EMAIL_EXISTS',
            http_status=409
        )
    
    # Create new user
    user_id = StorageService.generate_id('USR')
    password_hash = make_password(serializer.validated_data['password'])
    
    user = {
        'id': user_id,
        'name': serializer.validated_data['name'],
        'email': email,
        'password_hash': password_hash,
        'phone': serializer.validated_data['phone'],
        'created_at': StorageService.get_timestamp()
    }
    
    users[user_id] = user
    JsonStorage.write('users', users)
    
    # Generate JWT token
    token = JWTAuthentication.generate_token(user_id)
    
    response_data = {
        'user_id': user_id,
        'name': user['name'],
        'email': user['email'],
        'token': token
    }
    return api_response(data=response_data, message='User created successfully', http_status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Authenticate a user and return JWT token."""
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return api_response(
            success=False,
            message='Invalid data',
            error_code='INVALID_DATA',
            http_status=400
        )
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    
    users = JsonStorage.read('users')
    if not isinstance(users, dict):
        users = {}
    
    user = next((u for u in users.values() if u['email'] == email), None)
    if not user or not check_password(password, user['password_hash']):
        return api_response(
            success=False,
            message='Invalid email or password',
            error_code='AUTH_FAILED',
            http_status=401
        )
    
    # Generate JWT token
    token = JWTAuthentication.generate_token(user['id'])
    
    response_data = {
        'user_id': user['id'],
        'name': user['name'],
        'email': user['email'],
        'token': token
    }
    return api_response(data=response_data, message='Login successful')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Get current authenticated user info."""
    user_id = JWTAuthentication.get_user_from_token(request)
    if not user_id:
        return api_response(
            success=False,
            message='Unauthorized',
            error_code='UNAUTHORIZED',
            http_status=401
        )
    
    users = JsonStorage.read('users')
    if not isinstance(users, dict):
        users = {}
    
    user = users.get(user_id)
    if not user:
        return api_response(
            success=False,
            message='User not found',
            error_code='USER_NOT_FOUND',
            http_status=404
        )
    
    response_data = {
        'user_id': user['id'],
        'name': user['name'],
        'email': user['email'],
        'phone': user['phone'],
        'created_at': user['created_at']
    }
    return api_response(data=response_data)


# ===================== CHECKOUT ENDPOINTS =====================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    """Process checkout and create a pending order."""
    user_id = JWTAuthentication.get_user_from_token(request)
    if not user_id:
        return api_response(
            success=False,
            message='Unauthorized',
            error_code='UNAUTHORIZED',
            http_status=401
        )
    
    serializer = CheckoutSerializer(data=request.data)
    if not serializer.is_valid():
        return api_response(
            success=False,
            message='Invalid data',
            error_code='INVALID_DATA',
            http_status=400
        )
    
    # Get user's cart
    carts = JsonStorage.read('carts')
    if not isinstance(carts, dict):
        carts = {}
    
    cart_items = carts.get(user_id, [])
    if not cart_items:
        return api_response(
            success=False,
            message='Cart is empty',
            error_code='EMPTY_CART',
            http_status=400
        )
    
    # Validate cart and calculate total
    products = {p['id']: p for p in JsonStorage.read('products')}
    order_items = []
    total = 0
    
    for cart_item in cart_items:
        product = products.get(cart_item['product_id'])
        if not product:
            return api_response(
                success=False,
                message=f"Product {cart_item['product_id']} not found",
                error_code='PRODUCT_NOT_FOUND',
                http_status=404
            )
        
        # Verify stock
        stock = product.get('stock', {}).get(cart_item['size'], 0)
        if cart_item['quantity'] > stock:
            return api_response(
                success=False,
                message=f"Insufficient stock for {product['name']} size {cart_item['size']}",
                error_code='INSUFFICIENT_STOCK',
                http_status=400
            )
        
        # Verify price hasn't changed (server-side validation)
        unit_price = product['price']
        subtotal = unit_price * cart_item['quantity']
        
        order_items.append({
            'product_id': product['id'],
            'name': product['name'],
            'size': cart_item['size'],
            'quantity': cart_item['quantity'],
            'unit_price': unit_price,
            'subtotal': subtotal
        })
        
        total += subtotal
    
    # Create order
    order_id = StorageService.generate_id('VRD')
    shipping_address = serializer.validated_data['shipping_address']
    
    order = {
        'id': order_id,
        'user_id': user_id,
        'items': order_items,
        'shipping_address': shipping_address,
        'subtotal': total,
        'payment_status': 'pending',
        'order_status': 'placed',
        'created_at': StorageService.get_timestamp()
    }
    
    # Save order
    orders = JsonStorage.read('orders')
    if not isinstance(orders, list):
        orders = []
    orders.append(order)
    JsonStorage.write('orders', orders)
    
    # Clear cart
    del carts[user_id]
    JsonStorage.write('carts', carts)
    
    response_data = {
        'order_id': order['id'],
        'status': order['order_status'],
        'payment_status': order['payment_status'],
        'subtotal': order['subtotal'],
        'currency': 'INR'
    }
    return api_response(data=response_data, message='Order placed successfully', http_status=201)


# ===================== ORDER ENDPOINTS =====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    """Get all orders for the current user."""
    user_id = JWTAuthentication.get_user_from_token(request)
    if not user_id:
        return api_response(
            success=False,
            message='Unauthorized',
            error_code='UNAUTHORIZED',
            http_status=401
        )
    
    orders = JsonStorage.read('orders')
    if not isinstance(orders, list):
        orders = []
    
    user_orders = [o for o in orders if o.get('user_id') == user_id]
    serializer = OrderSerializer(user_orders, many=True)
    
    return api_response(data=serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_detail(request, order_id):
    """Get a specific order by ID."""
    user_id = JWTAuthentication.get_user_from_token(request)
    if not user_id:
        return api_response(
            success=False,
            message='Unauthorized',
            error_code='UNAUTHORIZED',
            http_status=401
        )
    
    orders = JsonStorage.read('orders')
    if not isinstance(orders, list):
        orders = []
    
    order = next((o for o in orders if o['id'] == order_id), None)
    if not order:
        return api_response(
            success=False,
            message='Order not found',
            error_code='ORDER_NOT_FOUND',
            http_status=404
        )
    
    # Verify ownership
    if order['user_id'] != user_id:
        return api_response(
            success=False,
            message='Forbidden',
            error_code='FORBIDDEN',
            http_status=403
        )
    
    serializer = OrderSerializer(order)
    return api_response(data=serializer.data)
