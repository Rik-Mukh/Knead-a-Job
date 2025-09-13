import React, { useContext } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Navbar = () => {
    const location = useLocation();
    const { logout, user } = useContext(AuthContext);
    
    const isActive = (path) => {
        return location.pathname === path;
    };
    
    return (
        <nav className="navbar">
            <div className="container">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    {/* App title/brand */}
                    <Link to="/" className="navbar-brand">
                        Job Tracker
                    </Link>
                    
                    {/* Navigation links */}
                    <ul className="navbar-nav">
                        <li>
                            <Link 
                                to="/" 
                                style={{ color: isActive('/') ? '#fff' : '#ccc' }}
                            >
                                Dashboard
                            </Link>
                        </li>
                        <li>
                            <Link 
                                to="/applications"
                                style={{ color: isActive('/applications') ? '#fff' : '#ccc' }}
                            >
                                Applications
                            </Link>
                        </li>
                        <li>
                            <Link 
                                to="/resumes"
                                style={{ color: isActive('/resumes') ? '#fff' : '#ccc' }}
                            >
                                Resumes
                            </Link>
                        </li>
                        <li>
                            <button 
                                onClick={logout} 
                                style={{ 
                                    background: 'none',
                                    border: 'none',
                                    color: '#ccc',
                                    cursor: 'pointer'
                                }}
                            >
                                Logout
                            </button>
                        </li>
                    </ul>
                </div>
                {user && (
                    <div style={{ textAlign: 'right', color: '#ccc', fontSize: '12px' }}>
                        Logged in as: {user.email}
                    </div>
                )}
            </div>
        </nav>
    );
};

export default Navbar;