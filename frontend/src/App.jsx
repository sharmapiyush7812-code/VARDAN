import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import { WishlistProvider } from './context/WishlistContext';

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <WishlistProvider>
          <div className="app">
            <h1>VARDAN — Built Different</h1>
            <p>E-Commerce Backend Integration Ready</p>
            
            {/* 
              TODO: Integrate the existing Index.html components here:
              1. Header with navigation
              2. Hero section with Three.js canvas
              3. Product grid connected to /api/products/
              4. Cart drawer connected to /api/cart/
              5. Wishlist drawer connected to /api/wishlist/
              6. Authentication pages
              7. Checkout flow connected to /api/checkout/
              8. Order history page
              
              Reference: /Index.html for existing design and animations
              Use: Preserve all existing CSS, animations, and visual design
              Connect: Use API services from src/services/api.js
              State: Use AuthContext, CartContext, WishlistContext
            */}

            <section style={{ padding: '40px', textAlign: 'center' }}>
              <h2>Backend API Status</h2>
              <p>Django API running on: <code>http://localhost:8000/api</code></p>
              <p>Available endpoints:</p>
              <ul style={{ textAlign: 'left', maxWidth: '600px', margin: '20px auto' }}>
                <li>GET /api/products/ - List all products</li>
                <li>POST /api/auth/signup/ - Create account</li>
                <li>POST /api/auth/login/ - Login</li>
                <li>POST /api/cart/add/ - Add to cart (authenticated)</li>
                <li>GET /api/orders/ - View orders (authenticated)</li>
              </ul>
            </section>
          </div>
        </WishlistProvider>
      </CartProvider>
    </AuthProvider>
  );
}

export default App;
