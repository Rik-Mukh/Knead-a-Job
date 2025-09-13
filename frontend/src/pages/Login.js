import React, { useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import GoogleLoginButton from '../components/GoogleLoginButton';

const Login = () => {
    const { isAuthenticated, loading } = useContext(AuthContext);
    const navigate = useNavigate();
    
    useEffect(() => {
        if (isAuthenticated && !loading) {
            navigate('/');
        }
    }, [isAuthenticated, loading, navigate]);
    
    return (
        <div style={{ 
            maxWidth: '400px',
            margin: '100px auto',
            padding: '20px',
            textAlign: 'center',
            borderRadius: '8px',
            boxShadow: '0 4px 8px rgba(0,0,0,0.1)'
        }}>
            <h2>Job Tracker</h2>
            <p>Track your job applications and manage your resumes</p>
            <GoogleLoginButton />
        </div>
    );
};

export default Login;