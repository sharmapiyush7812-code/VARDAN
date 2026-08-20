import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error);
    throw error;
  }
);

export const productsApi = {
  getProducts: (filters = {}) => api.get('/products/', { params: filters }),
  getProduct: (id) => api.get(`/products/${id}/`),
};

export const authApi = {
  signup: (data) => api.post('/auth/signup/', data),
  login: (data) => api.post('/auth/login/', data),
  me: () => api.get('/auth/me/'),
};

export const wishlistApi = {
  get: () => api.get('/wishlist/'),
  add: (productId) => api.post('/wishlist/add/', { product_id: productId }),
  remove: (productId) => api.delete(`/wishlist/${productId}/`),
};

export const cartApi = {
  get: () => api.get('/cart/'),
  add: (item) => api.post('/cart/add/', item),
  update: (itemId, quantity) => api.patch(`/cart/${itemId}/`, { quantity }),
  remove: (itemId) => api.delete(`/cart/${itemId}/remove/`),
};

export const checkoutApi = {
  create: (data) => api.post('/checkout/', data),
};

export const ordersApi = {
  getOrders: () => api.get('/orders/'),
  getOrder: (id) => api.get(`/orders/${id}/`),
};

export default api;
