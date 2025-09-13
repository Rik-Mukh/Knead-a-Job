import React from 'react';

const NotificationCard = ({ notification, onMarkRead }) => {
  const getBackground = () => notification.read ? '#f5f5f5' : '#e8f0fe';

  return (
    <div 
      style={{
        backgroundColor: getBackground(),
        padding: '12px 16px',
        marginBottom: '8px',
        borderRadius: '8px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        cursor: 'pointer'
      }}
      onClick={() => onMarkRead(notification.id)}
    >
      <h4 style={{ margin: '0 0 4px 0' }}>{notification.title}</h4>
      <p style={{ margin: '0 0 4px 0', fontSize: '14px', color: '#555' }}>{notification.message}</p>
      <span style={{ fontSize: '12px', color: '#888' }}>
        {new Date(notification.date).toLocaleString()}
      </span>
    </div>
  );
};

export default NotificationCard;
