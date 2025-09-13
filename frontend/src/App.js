import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './context/AuthContext';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import JobApplications from './pages/JobApplications';
import ResumeManager from './pages/ResumeManager';
import Login from './pages/Login';
import AuthSuccess from './components/AuthSuccess';

// Protected route component
const ProtectedRoute = ({ element }) => {
    const { isAuthenticated, loading } = useContext(AuthContext);
    
    if (loading) return <div className="loading">Loading...</div>;
    
    return isAuthenticated ? element : <Navigate to="/login" />;
};

// Routes component to access context
const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/auth-success" element={<AuthSuccess />} />
            <Route path="/" element={<ProtectedRoute element={<><Navbar /><Dashboard /></>} />} />
            <Route path="/applications" element={<ProtectedRoute element={<><Navbar /><JobApplications /></>} />} />
            <Route path="/resumes" element={<ProtectedRoute element={<><Navbar /><ResumeManager /></>} />} />
        </Routes>
    );
};

function App() {
    return (
        <AuthProvider>
            <Router>
                <div className="App">
                    <div className="container">
                        <AppRoutes />
                    </div>
                </div>
            </Router>
        </AuthProvider>
    );
}

export default App;