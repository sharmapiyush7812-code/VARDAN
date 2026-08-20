import React, { createContext, useContext, useState, useCallback } from 'react';

const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState([]);
  const [subtotal, setSubtotal] = useState(0);
  const [loading, setLoading] = useState(false);

  const addItem = useCallback((item) => {
    setCart((prevCart) => {
      const existingItem = prevCart.find((i) => i.id === item.id);
      if (existingItem) {
        return prevCart.map((i) =>
          i.id === item.id ? { ...i, quantity: i.quantity + item.quantity } : i
        );
      }
      return [...prevCart, item];
    });
  }, []);

  const removeItem = useCallback((itemId) => {
    setCart((prevCart) => prevCart.filter((i) => i.id !== itemId));
  }, []);

  const updateItem = useCallback((itemId, quantity) => {
    if (quantity <= 0) {
      removeItem(itemId);
      return;
    }
    setCart((prevCart) =>
      prevCart.map((i) => (i.id === itemId ? { ...i, quantity } : i))
    );
  }, [removeItem]);

  const clear = useCallback(() => {
    setCart([]);
    setSubtotal(0);
  }, []);

  const setCartData = useCallback((cartData) => {
    setCart(cartData.items || []);
    setSubtotal(cartData.subtotal || 0);
  }, []);

  const value = {
    cart,
    subtotal,
    loading,
    itemCount: cart.length,
    addItem,
    removeItem,
    updateItem,
    clear,
    setCartData,
    setLoading,
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within CartProvider');
  }
  return context;
};
