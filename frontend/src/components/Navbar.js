import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <nav style={{ backgroundColor: '#ffffff', padding: '10px 20px', height: '100px', paddingTop: '30px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        {/* App title/brand */}
        <Link to="/" style={{ color: '#000', fontWeight: 'bold', textDecoration: 'none', fontSize: '2.5rem' }}>
          Knead a Job
        </Link>

        {/* Navigation links */}
        <ul style={{ display: 'flex', listStyle: 'none', margin: 0, padding: 0, gap: '20px' }}>
          <li>
            <Link 
              to="/" 
              style={{ 
                color: isActive('/') ? '#007bff' : '#000', 
                textDecoration: 'none',
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
                fontWeight: isActive('/resumes') ? 'bold' : 'normal'
              }}
            >
              Resumes
            </Link>
          </li>
          <li>
            <Link 
            to="/responses" activeClassName="active"
              style={{ 
                color: isActive('/responses') ? '#007bff' : '#000', 
                textDecoration: 'none',
                fontWeight: isActive('/responses') ? 'bold' : 'normal'
              }}
            >
              Responses
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
