import React, { useState } from 'react';
import NotificationCard from '../components/NotificationCard';

const sampleNotifications = [
  { id: 1, title: "Interview Scheduled", message: "Your interview is on Sep 15", type: "info", date: "2025-09-12T22:00:00Z", read: false },
  { id: 2, title: "Resume Viewed", message: "Your resume was viewed by Microsoft", type: "success", date: "2025-09-10T14:30:00Z", read: true },
  { id: 3, title: "Application Rejected", message: "Your application at Amazon was rejected", type: "error", date: "2025-09-08T09:00:00Z", read: false },
];

const NotificationsPage = () => {
  const [notifications, setNotifications] = useState(sampleNotifications);

  const markAsRead = (id) => {
    setNotifications(notifications.map(n => n.id === id ? {...n, read: true} : n));
  };

  return (
    <div style={{ padding: '36px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '20px', font: "normal 500 2rem helvetica-neue-lt-pro" }}>Notifications</h1>
      {notifications.length === 0 ? (
        <p>No notifications</p>
      ) : (
        notifications.map(notification => (
          <NotificationCard 
            key={notification.id} 
            notification={notification} 
            onMarkRead={markAsRead} 
          />
        ))
      )}
    </div>
  );
};

export default NotificationsPage;
