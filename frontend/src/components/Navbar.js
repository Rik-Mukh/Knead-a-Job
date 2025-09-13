import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();

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
        <ul style={{ display: 'flex', listStyle: 'none', margin: 0, padding: 0, gap: '48px' }}>
          <li>
            <Link 
              to="/" 
              style={{ 
                color: isActive('/') ? '#007bff' : '#000', 
                textDecoration: 'none',
                fontFamily: 'helvetica-neue-lt-pro',
                fontWeight: isActive('/') ? 'bold' : 'normal'
              }}
            >
              Dashboard
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
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
