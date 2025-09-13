import React from 'react';

const NotificationCard = ({ notification, onMarkRead }) => {
  const getBackground = () => notification.read ? '#f5f5f5' : '#e8f0fe';

  return (
    <div 
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        backgroundColor: getBackground(),
        padding: '12px 24px',
        marginBottom: '8px',
        borderRadius: '12px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        cursor: 'pointer'
      }}
      onClick={() => onMarkRead(notification.id)}
    >
      <h4 style={{ margin: '0 0 4px 0', font: "normal 500 1.5rem helvetica-neue-lt-pro" }}>{notification.title}</h4>
      <p style={{ margin: '0 0 4px 0', fontSize: '14px', color: '#555' }}>{notification.message}</p>
      <span style={{ marginTop: '16px', fontSize: '12px', color: '#888' }}>
        {new Date(notification.date).toLocaleString()}
      </span>
    </div>
  );
};

export default NotificationCard;
