import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();

  // Example: unread notifications count
  const [unreadCount, setUnreadCount] = useState(3); // you can fetch this from backend

  const isActive = (path) => location.pathname === path;

  return (
    <nav style={{ 
      backgroundColor: '#ffffff', padding: '16px 48px', height: 'fit-content',}}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        {/* App title/brand */}
        <Link to="/" style={{
            color: '#040fDA',
            textDecoration: 'none', 
            fontFamily: 'bree-serif',
            fontSize: '2.5rem',
            letterSpacing: '-0.15rem',
          }}>
          Knead a Job
        </Link>

        {/* Navigation links */}
        <ul style={{ display: 'flex', listStyle: 'none', margin: 0, padding: 0, gap: '48px', alignItems: 'center' }}>
          <li>
            <Link 
              to="/responses" 
              style={{ 
                color: isActive('/responses') ? '#007bff' : '#000', 
                textDecoration: 'none',
                fontFamily: 'helvetica-neue-lt-pro',
                fontWeight: isActive('/') ? 'bold' : 'normal'
              }}
            >
              Responses
            </Link>
          </li>
          <li>
            <Link 
              to="/applications"
              style={{ 
                color: isActive('/applications') ? '#007bff' : '#000', 
                textDecoration: 'none',
                fontFamily: 'helvetica-neue-lt-pro',
                fontWeight: isActive('/applications') ? 'bold' : 'normal'
              }}
            >
              Applications
            </Link>
          </li>
          <li>
            <Link 
              to="/resumes"
              style={{ 
                color: isActive('/resumes') ? '#007bff' : '#000', 
                textDecoration: 'none',
                fontFamily: 'helvetica-neue-lt-pro',
                fontWeight: isActive('/resumes') ? 'bold' : 'normal'
              }}
            >
              Resumes
            </Link>
          </li>

          {/* Notifications link */}
          <li style={{ position: 'relative' }}>
            <Link 
              to="/notifications"
              style={{ 
                color: isActive('/notifications') ? '#007bff' : '#000', 
                textDecoration: 'none',
                fontWeight: isActive('/notifications') ? 'bold' : 'normal',
                display: 'flex',
                alignItems: 'center',
              }}
            >
              Notifications
              {unreadCount > 0 && (
                <span 
                  style={{
                    marginLeft: '6px',
                    backgroundColor: '#dc3545',
                    color: '#fff',
                    borderRadius: '50%',
                    padding: '2px 6px',
                    fontSize: '12px',
                    fontWeight: 'bold',
                  }}
                >
                  {unreadCount}
                </span>
              )}
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
