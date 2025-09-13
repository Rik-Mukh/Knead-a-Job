import React from 'react';
import authService from '../services/authService';

const GoogleLoginButton = () => {
  const handleLogin = () => {
    // Redirect to Django's Google OAuth URL
    window.location.href = authService.getGoogleLoginURL();
  };

  return (
    <button 
      onClick={handleLogin}
      style={{
        backgroundColor: '#4285F4',
        color: 'white',
        border: 'none',
        padding: '10px 20px',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '16px'
      }}
    >
      Login with Google
    </button>
  );
};

export default GoogleLoginButton;