import React from 'react';

const NotificationCard = ({ notification, onMarkRead }) => {
  const getBackground = () => notification.read ? '#f5f5f5' : '#007bff'
  const getColor = () => notification.read ? '#000' : '#fff';
  const getDateColor = () => notification.read ? '#1e1e1e' : '#f1f1f1'

  return (
    <div 
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        backgroundColor: getBackground(),
        color: getColor(),
        padding: '12px 24px',
        marginBottom: '8px',
        borderRadius: '12px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        cursor: 'pointer'
      }}
      onClick={() => onMarkRead(notification.id)}
    >
      <h4 style={{ margin: '0 0 4px 0', font: "normal 500 1.5rem helvetica-neue-lt-pro", color: {getColor} }}>{notification.title}</h4>
      <p style={{ margin: '0 0 4px 0', fontSize: '14px', color: {getColor} }}>{notification.message}</p>
      <span style={{ marginTop: '16px', fontSize: '12px', color: {getDateColor} }}>
        {new Date(notification.date).toLocaleString()}
      </span>
    </div>
  );
};

export default NotificationCard;
