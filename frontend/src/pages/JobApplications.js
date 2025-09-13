import React, { useState, useEffect } from 'react';
import { applicationService } from '../services/applicationService';
import ApplicationCard from '../components/ApplicationCard';
import JobApplicationForm from '../components/JobApplicationForm';
import MeetingMinutesForm from '../components/MeetingMinutesForm';
import SankeyDiagram from '../components/SankeyDiagram';
import { processApplicationsForSankey } from '../utils/sankeyDataProcessor';

const JobApplications = () => {
  const [applications, setApplications] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingApplication, setEditingApplication] = useState(null);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('all');
  const [selectedApplicationForTracking, setSelectedApplicationForTracking] = useState(null);
  const [selectedApplicationForMeetingMinutes, setSelectedApplicationForMeetingMinutes] = useState(null);


  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      setLoading(true);
      const data = await applicationService.getAll();
      setApplications(data);
    } catch (error) {
      console.error('Error fetching applications:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddApplication = async (formData) => {
    try {
      await applicationService.create(formData);
      setShowForm(false);
      fetchApplications();
    } catch (error) {
      console.error('Error creating application:', error);
    }
  };

  const handleEditApplication = async (formData) => {
    try {
      await applicationService.update(editingApplication.id, formData);
      setEditingApplication(null);
      fetchApplications();
    } catch (error) {
      console.error('Error updating application:', error);
    }
  };

  const handleDeleteApplication = async (id) => {
    if (window.confirm('Are you sure you want to delete this application?')) {
      try {
        await applicationService.delete(id);
        fetchApplications();
      } catch (error) {
        console.error('Error deleting application:', error);
      }
    }
  };

  const handleEdit = (application) => {
    setEditingApplication(application);
    setShowForm(false);
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingApplication(null);
  };

  const handleTrackApplication = (application) => {
    setSelectedApplicationForTracking(application);
    setShowForm(false);
    setEditingApplication(null);
  };

  const handleAddMeetingMinutes = (application) => {
    setSelectedApplicationForMeetingMinutes(application);
    setShowForm(false);
    setEditingApplication(null);
  };

  const handleCloseMeetingMinutes = () => {
    setSelectedApplicationForMeetingMinutes(null);
  };

  const handleMeetingMinutesSuccess = () => {
    fetchApplications(); // Refresh the applications list
  };
  

  const filteredApplications = applications.filter(app => 
    statusFilter === 'all' || app.status === statusFilter
  );

  if (loading) {
    return (
      <div className="text-center">
        <h2>Job Applications</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2 style={{
          font: "normal 500 2rem helvetica-neue-lt-pro"
        }}>Job Applications</h2>
        <button 
          onClick={() => setShowForm(true)}
          className="btn btn-primary"
        >
          Add Application
        </button>
      </div>

      {/* Status Filter */}
      <div className="mb-3">
        <label className="form-label">Filter by Status:</label>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="form-control"
          style={{ width: '200px', display: 'inline-block', marginLeft: '10px' }}
        >
          <option value="all">All</option>
          <option value="applied">Applied</option>
          <option value="interview">Interview</option>
          <option value="rejected">Rejected</option>
          <option value="accepted">Accepted</option>
          <option value="withdrawn">Withdrawn</option>
        </select>
      </div>

      {/* Form */}
      {(showForm || editingApplication) && (
        <div className="mb-4">
          <JobApplicationForm
            onSubmit={editingApplication ? handleEditApplication : handleAddApplication}
            initialData={editingApplication || {}}
          />
          <button onClick={handleCancel} className="btn btn-secondary">
            Cancel
          </button>
        </div>
      )}

      {/* Applications List */}
      {filteredApplications.length > 0 ? (
        <div className="grid grid-2">
          {filteredApplications.map((application) => (
            <ApplicationCard
              key={application.id}
              application={application}
              onEdit={handleEdit}
              onDelete={handleDeleteApplication}
              onTrack={handleTrackApplication}
              onAddMeetingMinutes={handleAddMeetingMinutes}
            />
          ))}
        </div>
      ) : (
        <div className="card text-center">
          <h3>No Applications Found</h3>
          <p style={{ color: '#666' }}>
            {statusFilter === 'all' 
              ? "You haven't added any job applications yet. Click 'Add Application' to get started!"
              : `No applications with status '${statusFilter}' found.`
            }
          </p>
          {statusFilter === 'all' && (
            <button 
              onClick={() => setShowForm(true)}
              className="btn btn-primary"
            >
              Add Your First Application
            </button>
          )}
        </div>
      )}

      {/* Sankey Diagram Section */}
      {filteredApplications.length > 0 && (
        <div style={{ marginTop: '40px' }}>
          <div className="card">
            <div style={{ padding: '20px' }}>
              <h3 style={{ marginBottom: '20px', textAlign: 'center' }}>
                Application Flow Visualization
              </h3>
              <SankeyDiagram 
                data={processApplicationsForSankey(filteredApplications)} 
                height={400}
              />
            </div>
          </div>
        </div>
      )}

      {/* Meeting Minutes Form Modal */}
      {selectedApplicationForMeetingMinutes && (
        <MeetingMinutesForm
          application={selectedApplicationForMeetingMinutes}
          onClose={handleCloseMeetingMinutes}
          onSuccess={handleMeetingMinutesSuccess}
        />
      )}
    </div>
  );
};

export default JobApplications;
