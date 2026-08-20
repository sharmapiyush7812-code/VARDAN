from django.urls import path
from . import views

urlpatterns = [
    # Product Endpoints
    path('products/', views.get_products, name='get_products'),
    path('products/<str:product_id>/', views.get_product_detail, name='get_product_detail'),
    
    # Wishlist Endpoints
    path('wishlist/', views.get_wishlist, name='get_wishlist'),
    path('wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/<str:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Cart Endpoints
    path('cart/', views.get_cart, name='get_cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/<str:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/<str:item_id>/remove/', views.remove_from_cart, name='remove_from_cart'),
    
    # Authentication Endpoints
    path('auth/signup/', views.signup, name='signup'),
    path('auth/login/', views.login, name='login'),
    path('auth/me/', views.get_current_user, name='get_current_user'),
    
    # Checkout Endpoints
    path('checkout/', views.checkout, name='checkout'),
    
    # Order Endpoints
    path('orders/', views.get_orders, name='get_orders'),
    path('orders/<str:order_id>/', views.get_order_detail, name='get_order_detail'),
]
