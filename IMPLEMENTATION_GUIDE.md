# VARDAN Frontend Implementation Guide

Complete guide for finishing the React component implementation.

## Status Summary

✅ **Backend**: Fully implemented and tested
✅ **API Services**: All endpoints ready
✅ **Context Providers**: Auth, Cart, Wishlist ready
❌ **React Components**: Need to be built from Index.html

## Step 1: Copy CSS into React

The original `Index.html` contains extensive CSS. You need to:

1. Extract the `<style>` section from `/Index.html`
2. Paste it into `/frontend/src/index.css`
3. Add any missing imports for fonts (Archivo Black, Inter)

The CSS includes:
- Custom cursor system (with hover effects)
- Preloader with animation
- Three.js hero section styling
- Product grid with hover transforms
- Drawer systems (cart/wishlist)
- Newsletter section
- Footer
- All animations and transitions

## Step 2: Core Component Structure

Create these component files following the existing HTML structure:

### `/frontend/src/components/Header.jsx`
```
- Logo with animation
- Navigation menu
- Icons (search, wishlist, cart) with badges
- Header scroll effect
- Magnetic buttons
```

### `/frontend/src/components/Hero.jsx`
```
- Hero section with marquee
- Three.js blob animation
- Call-to-action button
- Floating tag
```

### `/frontend/src/components/ProductGrid.jsx`
```
- Fetch products from /api/products/
- Display in 4-column grid
- Filter buttons (all, track, vardan, sale)
- Product card hover effects
- Add to cart button
- Wishlist toggle button
```

### `/frontend/src/components/ProductCard.jsx`
```
- Product image/gradient
- Product name and price
- Old price (if on sale)
- Size selection (should open detail modal)
- Add to cart / Update quantity
- Wishlist heart button with animation
```

### `/frontend/src/components/CartDrawer.jsx`
```
- List cart items
- Update quantities
- Remove items
- Subtotal calculation
- "Place Order" button -> checkout flow
- Order confirmation screen
```

### `/frontend/src/components/WishlistDrawer.jsx`
```
- List wishlist items
- Remove from wishlist
- "Add to Cart" button for each
- Empty state message
```

### `/frontend/src/components/AuthModal.jsx`
```
- Signup form
- Login form
- Toggle between signup/login
- Call /api/auth/signup/ or /api/auth/login/
- Store token in localStorage
- Update AuthContext
```

### `/frontend/src/components/CheckoutForm.jsx`
```
- Shipping address fields
- Form validation
- Call /api/checkout/
- Handle pending order response
- Show order confirmation
```

### `/frontend/src/components/OrdersPage.jsx`
```
- Fetch /api/orders/ for authenticated user
- Display order list
- Click to view order detail
```

### `/frontend/src/components/OrderDetail.jsx`
```
- Fetch /api/orders/<order_id>/
- Display order items
- Show shipping info
- Show payment status
- Show order status
```

## Step 3: Connect Components to API

### Example: ProductGrid Component

```jsx
import { useState, useEffect } from 'react';
import { productsApi } from '../services/api';

export function ProductGrid() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await productsApi.getProducts();
        setProducts(response.data);
      } catch (error) {
        console.error('Failed to fetch products:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchProducts();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="product-grid">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

### Example: CartDrawer Component

```jsx
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { cartApi } from '../services/api';

export function CartDrawer() {
  const { cart, removeItem } = useCart();
  const { isAuthenticated } = useAuth();

  const handleRemove = async (itemId) => {
    try {
      await cartApi.remove(itemId);
      removeItem(itemId);
    } catch (error) {
      console.error('Failed to remove item:', error);
    }
  };

  return (
    <div className="drawer" id="cart-drawer">
      {/* Drawer markup */}
    </div>
  );
}
```

## Step 4: App.jsx Structure

```jsx
import Header from './components/Header';
import Hero from './components/Hero';
import ProductGrid from './components/ProductGrid';
import CartDrawer from './components/CartDrawer';
import WishlistDrawer from './components/WishlistDrawer';
import Footer from './components/Footer';
import Newsletter from './components/Newsletter';

function App() {
  return (
    <>
      <Header />
      <main>
        <Hero />
        <ProductGrid />
        <Newsletter />
        <Footer />
      </main>
      <CartDrawer />
      <WishlistDrawer />
    </>
  );
}
```

## Step 5: Component Interaction Flow

### Adding Product to Cart
```
ProductCard → addToCart button
  ↓
Call cartApi.add(product_id, size, quantity)
  ↓
Update CartContext with new item
  ↓
Show toast notification
  ↓
Update cart badge in header
```

### Checkout Flow
```
CartDrawer → "Place Order" button
  ↓
Show AuthModal if not authenticated
  ↓
Navigate to CheckoutForm
  ↓
Collect shipping address
  ↓
Call checkoutApi.create(address)
  ↓
Clear cart from CartContext
  ↓
Show order confirmation
  ↓
Redirect to OrderDetail page
```

### Wishlist Toggle
```
ProductCard → Heart button
  ↓
Check if authenticated (if not, require login)
  ↓
Call wishlistApi.add/remove()
  ↓
Update WishlistContext
  ↓
Update heart icon state
  ↓
Update wishlist badge
```

## Step 6: Important CSS Classes to Preserve

These classes are critical and used throughout:

- `.drawer` - Drawer container with slide animation
- `.product-card` - Product grid item with hover effect
- `.badge` - Notification badge for cart/wishlist
- `.text-3d` - 3D text effect
- `.glitch-text` - Glitch hover effect
- `.reveal` - Scroll-in animation
- `.product-grid` - Grid layout with correct spacing
- `.filter-btn` - Filter button styling
- `.icon-btn` - Header icon buttons

## Step 7: Key Features to Implement

### Custom Cursor (if not touch device)
- Small cream dot follows cursor
- Larger ring expands on hover
- Mix-blend-mode: difference

### Preloader
- Shows on app load
- Progress animation
- Disappears after content loads

### Three.js Elements
- Hero blob with noise shader
- Manifesto diamond wireframe
- Smooth rotation animations

### Animations
- Text reveal on scroll
- Marquee scrolling text
- Magnetic buttons
- Card 3D perspective on hover

## Step 8: API Integration Checklist

- [ ] Products load and display
- [ ] Filter buttons work
- [ ] Product card add to cart works
- [ ] Wishlist heart toggle works
- [ ] Cart drawer shows items
- [ ] Cart item removal works
- [ ] Cart subtotal calculates correctly
- [ ] Login/Signup modal appears
- [ ] Authentication tokens persist on refresh
- [ ] Checkout form collects address
- [ ] Order confirmation shows
- [ ] Orders page loads for authenticated user
- [ ] Order detail page shows correct data

## Step 9: Testing Endpoints

Before implementing components, test all endpoints:

```bash
# Get products
curl http://localhost:8000/api/products/

# Create user
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","password":"Test123","phone":"1234567890"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123"}'

# Add to cart (with token)
curl -X POST http://localhost:8000/api/cart/add/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id":"p01","size":"M","quantity":1}'
```

## Step 10: Styling Approach

### Global Styles (in index.css)
- CSS variables for colors
- Reset styles
- Font imports
- Animation keyframes
- Responsive breakpoints

### Component Scoping
- Use CSS classes from original design
- Avoid creating new CSS unless necessary
- Preserve hover states and transitions
- Maintain responsive behavior

## Common Pitfalls to Avoid

1. **Forgetting to import Context providers in main App**
2. **Not handling authentication errors in forms**
3. **Not updating UI immediately after API calls**
4. **Breaking animations when adding React state**
5. **Not preserving CSS hover effects in interactive elements**
6. **Forgetting CORS headers in API calls**
7. **Not handling loading and error states**
8. **Modifying product prices on frontend (backend is source of truth)**

## Performance Tips

1. Lazy load product images
2. Implement image optimization
3. Cache product data in Context
4. Minimize re-renders with useCallback
5. Use React.memo for ProductCard
6. Defer Three.js animations if needed
7. Implement proper error boundaries

## File Structure After Completion

```
frontend/src/
├── components/
│   ├── Header.jsx
│   ├── Hero.jsx
│   ├── ProductGrid.jsx
│   ├── ProductCard.jsx
│   ├── ProductDetail.jsx
│   ├── CartDrawer.jsx
│   ├── WishlistDrawer.jsx
│   ├── AuthModal.jsx
│   ├── CheckoutForm.jsx
│   ├── OrdersPage.jsx
│   ├── OrderDetail.jsx
│   ├── Footer.jsx
│   ├── Newsletter.jsx
│   └── Preloader.jsx
├── services/
│   └── api.js
├── context/
│   ├── AuthContext.jsx
│   ├── CartContext.jsx
│   └── WishlistContext.jsx
├── hooks/
│   ├── useAuth.js
│   ├── useCart.js
│   └── useWishlist.js
├── App.jsx
├── main.jsx
└── index.css
```

## Next Developer: Getting Started

1. Start the backend: `cd backend && source env/bin/activate && python manage.py runserver 8000`
2. Install frontend deps: `cd frontend && npm install`
3. Copy CSS from Index.html to index.css
4. Create Header component first
5. Create ProductGrid component second
6. Test API connection
7. Build remaining components iteratively
8. Test each component as you build

Good luck! 🚀
