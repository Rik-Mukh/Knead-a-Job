import React, { useState, useEffect } from 'react';
import NotificationCard from '../components/NotificationCard';
import { notificationService } from '../services/notificationService';
import { useNotification } from '../contexts/NotificationContext';

const NotificationsPage = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { refreshUnreadCount } = useNotification();

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await notificationService.getAll();
      console.log('DEBUG: Fetched notifications data:', data);
      console.log('DEBUG: Data type:', typeof data);
      console.log('DEBUG: Is array:', Array.isArray(data));
      // Ensure data is an array, fallback to empty array if not
      setNotifications(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching notifications:', error);
      // Set to empty array on error to prevent map errors
      setNotifications([]);
      setError('Failed to load notifications. Please check if the backend is running and the database migration is applied.');
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (id) => {
    try {
      await notificationService.markAsRead(id);
      setNotifications(notifications.map(n => n.id === id ? {...n, is_read: true} : n));
      // Refresh the unread count in the navbar
      refreshUnreadCount();
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  if (loading) {
    return (
      <div style={{ padding: '36px', maxWidth: '800px', margin: '0 auto' }}>
        <h1 style={{ marginBottom: '20px' }}>Notifications</h1>
        <p>Loading notifications...</p>
      </div>
    );
  }

  // Ensure notifications is always an array
  const safeNotifications = Array.isArray(notifications) ? notifications : [];

  return (
    <div style={{ padding: '36px', maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1 style={{ margin: 0 }}>Notifications</h1>
        <button 
          onClick={fetchNotifications}
          disabled={loading}
          style={{
            padding: '8px 16px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.6 : 1
          }}
        >
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>
      
      {error ? (
        <div style={{ 
          padding: '16px', 
          backgroundColor: '#f8d7da', 
          color: '#721c24', 
          border: '1px solid #f5c6cb', 
          borderRadius: '4px',
          marginBottom: '16px'
        }}>
          {error}
        </div>
      ) : null}
      
      {safeNotifications.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <p>No notifications</p>
          <p style={{ color: '#666', fontSize: '14px' }}>
            Notifications will appear here when you change job application statuses.
          </p>
        </div>
      ) : (
        <div>
          <p style={{ marginBottom: '16px', color: '#666' }}>
            Showing {safeNotifications.length} notification{safeNotifications.length !== 1 ? 's' : ''}
          </p>
          {safeNotifications.map(notification => (
            <NotificationCard 
              key={notification.id} 
              notification={{
                ...notification,
                read: notification.is_read,
                date: notification.created_at,
                type: notification.notification_type === 'immediate' ? 'info' : 'warning'
              }} 
              onMarkRead={markAsRead} 
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default NotificationsPage;
