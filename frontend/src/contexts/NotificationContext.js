import React, { createContext, useContext, useState, useEffect, useRef } from 'react';
import { notificationService } from '../services/notificationService';
import { playNotificationSound } from '../utils/sound';

const NotificationContext = createContext();

export const useNotification = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return context;
};

export const NotificationProvider = ({ children }) => {
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const prevUnreadRef = useRef(null);
  const initializedRef = useRef(false);

  const fetchUnreadCount = async (silent = false) => {
    try {
      if (!silent) setLoading(true);
      const response = await notificationService.getUnreadCount();
      const newCount = response.unread_count || 0;

      if (initializedRef.current && prevUnreadRef.current != null && newCount > prevUnreadRef.current) {
        playNotificationSound();
      }

      setUnreadCount(newCount);
      prevUnreadRef.current = newCount;
      if (!initializedRef.current) initializedRef.current = true;
    } catch (error) {
      console.error('Error fetching unread notification count:', error);
      setUnreadCount(0);
    } finally {
      if (!silent) setLoading(false);
    }
  };

  useEffect(() => {
    fetchUnreadCount(false);
    const interval = setInterval(() => fetchUnreadCount(true), 15000);
    return () => clearInterval(interval);
  }, []);

  const refreshUnreadCount = () => {
    fetchUnreadCount(true);
  };

  const value = {
    unreadCount,
    loading,
    refreshUnreadCount
  };

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
};
