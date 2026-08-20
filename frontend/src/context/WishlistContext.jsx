import React, { createContext, useContext, useState, useCallback } from 'react';

const WishlistContext = createContext(null);

export const WishlistProvider = ({ children }) => {
  const [wishlist, setWishlist] = useState(new Set());
  const [loading, setLoading] = useState(false);

  const add = useCallback((productId) => {
    setWishlist((prev) => new Set(prev).add(productId));
  }, []);

  const remove = useCallback((productId) => {
    setWishlist((prev) => {
      const newSet = new Set(prev);
      newSet.delete(productId);
      return newSet;
    });
  }, []);

  const toggle = useCallback((productId) => {
    setWishlist((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(productId)) {
        newSet.delete(productId);
      } else {
        newSet.add(productId);
      }
      return newSet;
    });
  }, []);

  const clear = useCallback(() => {
    setWishlist(new Set());
  }, []);

  const setWishlistData = useCallback((products) => {
    setWishlist(new Set(products || []));
  }, []);

  const value = {
    wishlist,
    loading,
    count: wishlist.size,
    add,
    remove,
    toggle,
    clear,
    has: (productId) => wishlist.has(productId),
    setWishlistData,
    setLoading,
  };

  return (
    <WishlistContext.Provider value={value}>{children}</WishlistContext.Provider>
  );
};

export const useWishlist = () => {
  const context = useContext(WishlistContext);
  if (!context) {
    throw new Error('useWishlist must be used within WishlistProvider');
  }
  return context;
};
