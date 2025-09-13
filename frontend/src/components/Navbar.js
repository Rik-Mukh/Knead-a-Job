import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="navbar">
      <div className="container">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Link to="/" className="navbar-brand">
            Job Tracker
          </Link>
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
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
