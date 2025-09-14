/**
 * Main App Component
 * 
 * This is the root component of the React application.
 * It sets up the routing structure and renders the main layout.
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { NotificationProvider } from './contexts/NotificationContext';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import JobApplications from './pages/JobApplications';
import ResumeManager from './pages/ResumeManager';
import NotificationsPage from './pages/NotificationsPage'; 
import ResponsesPage from './pages/ResponsesPage'; 
import Login from './pages/Login';
import ResumeTemplate from './pages/ResumeTemplate';
import GmailMessages from './components/GmailMessages'

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
    <NotificationProvider>
      <Router>
        <div className="App">
          {/* Navigation bar component */}
          <Navbar />
          
          {/* Main content container */}
          <div className="container">
            <Routes>
              <Route path="/" element={<Login />} />

              {/* Dashboard route - shows overview and statistics */}
              <Route path="/dashboard" element={<Dashboard />} />
              
              {/* Job applications route - manage job applications */}
              <Route path="/applications" element={<JobApplications />} />
              
              {/* Resume template route - manage structured resume data */}
              <Route path="/resume-template" element={<ResumeTemplate />} />
              
              {/* Notifications route */}
              <Route path="/notifications" element={<NotificationsPage />} />
              
              <Route path="/responses" element={<ResponsesPage />} />

              <Route path="/gmail" element={<GmailMessages />} /> 
            </Routes>
          </div>
        </div>
      </Router>
    </NotificationProvider>
  );
}

export default App;


//function AppLayout() {
//  const location = useLocation();
//
//  return (
//    <div className="App">
//      {/* Only show Navbar if not on "/" */}
//      {location.pathname !== "/" && <Navbar />}
//      
//      <div className="container">
//        <Routes>
//          <Route path="/" element={<Login />} />
//          <Route path="/dashboard" element={<Dashboard />} />
//          <Route path="/applications" element={<JobApplications />} />
//          <Route path="/resumes" element={<ResumeManager />} />
//          <Route path="/notifications" element={<NotificationsPage />} />
//          <Route path="/responses" element={<ResponsesPage />} />
//        </Routes>
//      </div>
//    </div>
//  );
//}
//
//function App() {
//  return (
//    <NotificationProvider>
//      <Router>
//        <AppLayout />
//      </Router>
//    </NotificationProvider>
//  );
//}//////////////////////////////////////////////////////////////