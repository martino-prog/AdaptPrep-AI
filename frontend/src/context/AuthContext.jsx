import React, { createContext, useContext, useState, useEffect } from 'react';
import { loginUser, signupUser, fetchCurrentUser } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('adaptprep_user');
    return savedUser ? JSON.parse(savedUser) : null;
  });
  const [token, setToken] = useState(() => localStorage.getItem('adaptprep_token') || null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      if (token) {
        try {
          const userData = await fetchCurrentUser();
          setUser(userData);
          localStorage.setItem('adaptprep_user', JSON.stringify(userData));
        } catch (err) {
          console.error("Token verification failed:", err);
          logout();
        }
      }
      setLoading(false);
    };
    initAuth();
  }, [token]);

  const handleLogin = async (username_or_email, password) => {
    const data = await loginUser(username_or_email, password);
    setToken(data.access_token);
    setUser(data.user);
    localStorage.setItem('adaptprep_token', data.access_token);
    localStorage.setItem('adaptprep_user', JSON.stringify(data.user));
    return data;
  };

  const handleSignup = async (username, email, password) => {
    const data = await signupUser(username, email, password);
    setToken(data.access_token);
    setUser(data.user);
    localStorage.setItem('adaptprep_token', data.access_token);
    localStorage.setItem('adaptprep_user', JSON.stringify(data.user));
    return data;
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('adaptprep_token');
    localStorage.removeItem('adaptprep_user');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        login: handleLogin,
        signup: handleSignup,
        logout,
        isAuthenticated: !!token && !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
