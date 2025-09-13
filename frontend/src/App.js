import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import JobApplications from './pages/JobApplications';
import ResumeManager from './pages/ResumeManager';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <div className="container">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/applications" element={<JobApplications />} />
            <Route path="/resumes" element={<ResumeManager />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
