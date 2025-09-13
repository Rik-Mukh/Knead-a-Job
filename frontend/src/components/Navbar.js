/**
 * Navigation Bar Component
 * 
 * This component provides the main navigation for the application.
 * It displays the app title and navigation links with active state styling.
 */

import React from 'react';
import { Link, useLocation } from 'react-router-dom';

/**
 * Navbar Component
 * 
 * Renders the main navigation bar with links to different sections of the app.
 * Uses React Router's useLocation hook to determine the current route and
 * applies active styling to the current page link.
 * 
 * @returns {JSX.Element} The navigation bar component
 */
const Navbar = () => {
  // Get the current location from React Router
  const location = useLocation();
  
  /**
   * Check if a given path is the current active route
   * 
   * @param {string} path - The path to check
   * @returns {boolean} True if the path matches the current location
   */
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="navbar">
      <div className="container">
        {/* Navigation content with flex layout */}
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
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
