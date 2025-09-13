import React, { createContext, useState, useEffect } from 'react';
import authService from '../services/authService';

// Create the context
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);
    
    const checkAuthStatus = async () => {
        setLoading(true);
        try {
            const data = await authService.checkAuthStatus();
            setIsAuthenticated(data.isAuthenticated);
            setUser(data.user || null);
        } catch (error) {
            console.error('Auth check failed:', error);
            setIsAuthenticated(false);
            setUser(null);
        } finally {
            setLoading(false);
        }
    };
    
    const logout = async () => {
        await authService.logout();
        setUser(null);
        setIsAuthenticated(false);
        window.location.href = '/login';
    };
    
    useEffect(() => {
        checkAuthStatus();
    }, []);
    
    return (
        <AuthContext.Provider value={{ user, isAuthenticated, loading, checkAuthStatus, logout }}>
            {children}
        </AuthContext.Provider>
    );
};