import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // This is just a placeholder function for now
  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    // In the future, this would authenticate with your backend
    setTimeout(() => {
      // Simulate login completion
      setLoading(false);
      navigate('/');
    }, 1000);
  };

  const handleGoogleLogin = () => {
    // This will eventually redirect to your Google OAuth login
    window.location.href = 'http://localhost:8000/accounts/google/login/?process=login&next=/auth-success/';
  };

  return (
    <div style={{ 
      height: '100vh',
      backgroundColor: '#e8e8f7',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
      <div style={{ 
        backgroundColor: '#fff', 
        borderRadius: '24px',
        padding: '40px',
        maxWidth: '400px',
        width: '100%',
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        border: '1.5px solid black'
      }}>
        <h2 style={{
          color: '#040fDA',
          fontFamily: 'bree-serif',
          fontSize: '2.5rem',
          letterSpacing: '-0.15rem',
          textAlign: 'center',
          marginBottom: '24px'
        }}>
          Knead a Job
        </h2>
        <p style={{ textAlign: 'center', marginBottom: '32px', color: '#555' }}>
          Sign in to manage your job applications
        </p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input
              type="email"
              className="form-control"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          
          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-control"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <button 
            type="submit" 
            className="btn btn-primary" 
            style={{ width: '100%', marginTop: '16px' }}
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Sign In'}
          </button>
        </form>
        
        <div style={{ textAlign: 'center', margin: '24px 0', color: '#666' }}>
          <span>OR</span>
        </div>
        
        <button
          onClick={handleGoogleLogin}
          className="btn"
          style={{
            width: '100%',
            backgroundColor: '#fff',
            color: '#555',
            border: '1px solid #ddd',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '10px'
          }}
        >
          <svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
            <path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"/>
            <path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"/>
            <path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"/>
            <path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"/>
          </svg>
          Continue with Google
        </button>
        
        <p style={{ textAlign: 'center', marginTop: '24px', fontSize: '14px', color: '#666' }}>
          Don't have an account? <a href="#" style={{ color: '#040fDA', textDecoration: 'none' }}>Sign up</a>
        </p>
      </div>
    </div>
  );
};

export default Login;