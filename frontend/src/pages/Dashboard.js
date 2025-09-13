import React, { useState, useEffect } from 'react';
import { applicationService } from '../services/applicationService';
import { resumeService } from '../services/resumeService';

const Dashboard = () => {
  const [stats, setStats] = useState({
    total: 0,
    applied: 0,
    interview: 0,
    rejected: 0,
    accepted: 0,
  });
  const [recentApplications, setRecentApplications] = useState([]);
  const [defaultResume, setDefaultResume] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch application statistics
      const statsData = await applicationService.getStats();
      setStats(statsData);
      
      // Fetch recent applications
      const applicationsData = await applicationService.getAll();
      setRecentApplications(applicationsData.slice(0, 5)); // Show only 5 most recent
      
      // Fetch default resume
      try {
        const resumeData = await resumeService.getDefault();
        setDefaultResume(resumeData);
      } catch (error) {
        // No default resume found
        setDefaultResume(null);
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="text-center">
        <h2>Dashboard</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div>
      <h2>Dashboard</h2>
      
      {/* Statistics Cards */}
      <div className="grid grid-3 mb-4">
        <div className="card text-center">
          <h3 style={{ margin: '0 0 8px 0', color: '#007bff' }}>{stats.total}</h3>
          <p style={{ margin: '0', color: '#666' }}>Total Applications</p>
        </div>
        <div className="card text-center">
          <h3 style={{ margin: '0 0 8px 0', color: '#28a745' }}>{stats.applied}</h3>
          <p style={{ margin: '0', color: '#666' }}>Applied</p>
        </div>
        <div className="card text-center">
          <h3 style={{ margin: '0 0 8px 0', color: '#ffc107' }}>{stats.interview}</h3>
          <p style={{ margin: '0', color: '#666' }}>Interviews</p>
        </div>
        <div className="card text-center">
          <h3 style={{ margin: '0 0 8px 0', color: '#dc3545' }}>{stats.rejected}</h3>
          <p style={{ margin: '0', color: '#666' }}>Rejected</p>
        </div>
        <div className="card text-center">
          <h3 style={{ margin: '0 0 8px 0', color: '#17a2b8' }}>{stats.accepted}</h3>
          <p style={{ margin: '0', color: '#666' }}>Accepted</p>
        </div>
      </div>

      <div className="grid grid-2">
        {/* Recent Applications */}
        <div>
          <h3>Recent Applications</h3>
          {recentApplications.length > 0 ? (
            <div>
              {recentApplications.map((app) => (
                <div key={app.id} className="card" style={{ marginBottom: '12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div>
                      <h4 style={{ margin: '0 0 4px 0', fontSize: '16px' }}>{app.position}</h4>
                      <p style={{ margin: '0 0 4px 0', color: '#666', fontSize: '14px' }}>{app.company_name}</p>
                    </div>
                    <span
                      style={{
                        backgroundColor: app.status === 'applied' ? '#17a2b8' : 
                                       app.status === 'interview' ? '#ffc107' :
                                       app.status === 'rejected' ? '#dc3545' :
                                       app.status === 'accepted' ? '#28a745' : '#6c757d',
                        color: 'white',
                        padding: '2px 6px',
                        borderRadius: '8px',
                        fontSize: '10px',
                        textTransform: 'capitalize'
                      }}
                    >
                      {app.status}
                    </span>
                  </div>
                  <p style={{ margin: '8px 0 0 0', fontSize: '12px', color: '#666' }}>
                    Applied: {formatDate(app.applied_date)}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <div className="card">
              <p style={{ margin: '0', color: '#666', textAlign: 'center' }}>
                No applications yet. Start by adding your first job application!
              </p>
            </div>
          )}
        </div>

        {/* Default Resume */}
        <div>
          <h3>Default Resume</h3>
          {defaultResume ? (
            <div className="card">
              <h4 style={{ margin: '0 0 8px 0' }}>{defaultResume.title}</h4>
              <p style={{ margin: '0 0 8px 0', color: '#666', fontSize: '14px' }}>
                Uploaded: {formatDate(defaultResume.created_at)}
              </p>
              <button className="btn btn-primary" style={{ fontSize: '14px' }}>
                Download Resume
              </button>
            </div>
          ) : (
            <div className="card">
              <p style={{ margin: '0 0 16px 0', color: '#666' }}>
                No default resume set. Upload a resume to get started!
              </p>
              <button className="btn btn-primary" style={{ fontSize: '14px' }}>
                Upload Resume
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
