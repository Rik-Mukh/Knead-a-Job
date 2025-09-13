import React, { useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const AuthSuccess = () => {
    const { checkAuthStatus } = useContext(AuthContext);
    const navigate = useNavigate();
    
    useEffect(() => {
        const handleSuccess = async () => {
            await checkAuthStatus();
            // Redirect to dashboard
            navigate('/');
        };
        
        handleSuccess();
    }, [checkAuthStatus, navigate]);
    
    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <p>Authentication successful, redirecting...</p>
        </div>
    );
};

export default AuthSuccess;