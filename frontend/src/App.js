/**
 * Main App Component
 * 
 * This is the root component of the React application.
 * It sets up the routing structure and renders the main layout.
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import JobApplications from './pages/JobApplications';
import ResumeManager from './pages/ResumeManager';
import ResumeTemplate from './pages/ResumeTemplate';

/**
 * App Component
 * 
 * Main application component that provides routing and layout structure.
 * Uses React Router for navigation between different pages.
 * 
 * @returns {JSX.Element} The main app component
 */
function App() {
  return (
    <Router>
      <div className="App">
        {/* Navigation bar component */}
        <Navbar />
        
        {/* Main content container */}
        <div className="container">
          <Routes>
            {/* Dashboard route - shows overview and statistics */}
            <Route path="/" element={<Dashboard />} />
            
            {/* Job applications route - manage job applications */}
            <Route path="/applications" element={<JobApplications />} />
            
            {/* Resume manager route - manage resume files */}
            <Route path="/resumes" element={<ResumeManager />} />
            
            {/* Resume template route - manage structured resume data */}
            <Route path="/resume-template" element={<ResumeTemplate />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
