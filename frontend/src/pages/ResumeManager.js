import React, { useState, useEffect } from 'react';
import { resumeService } from '../services/resumeService';
import ResumeUpload from '../components/ResumeUpload';

const ResumeManager = () => {
  const [resumes, setResumes] = useState([]);
  const [showUploadForm, setShowUploadForm] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    try {
      setLoading(true);
      const data = await resumeService.getAll();
      setResumes(data);
    } catch (error) {
      console.error('Error fetching resumes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadResume = async (formData, file) => {
    try {
      const uploadData = new FormData();
      uploadData.append('title', formData.title);
      uploadData.append('is_default', formData.is_default);
      uploadData.append('file', file);

      await resumeService.create(uploadData);
      setShowUploadForm(false);
      fetchResumes();
    } catch (error) {
      console.error('Error uploading resume:', error);
    }
  };

  const handleDeleteResume = async (id) => {
    if (window.confirm('Are you sure you want to delete this resume?')) {
      try {
        await resumeService.delete(id);
        fetchResumes();
      } catch (error) {
        console.error('Error deleting resume:', error);
      }
    }
  };

  const handleSetDefault = async (id) => {
    try {
      await resumeService.setDefault(id);
      fetchResumes();
    } catch (error) {
      console.error('Error setting default resume:', error);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="text-center">
        <h2>Resume Manager</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2 style={{
          font: "normal 500 2rem helvetica-neue-lt-pro"
        }}>Resume Manager</h2>
        <button 
          onClick={() => setShowUploadForm(true)}
          className="btn btn-primary"
        >
          Upload Resume
        </button>
      </div>

      {/* Upload Form */}
      {showUploadForm && (
        <div className="mb-4">
          <ResumeUpload onSubmit={handleUploadResume} />
          <button 
            onClick={() => setShowUploadForm(false)} 
            className="btn btn-secondary"
          >
            Cancel
          </button>
        </div>
      )}

      {/* Resumes List */}
      {resumes.length > 0 ? (
        <div className="grid grid-2">
          {resumes.map((resume) => (
            <div key={resume.id} className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                <div>
                  <h4 style={{ margin: '0 0 8px 0' }}>{resume.title}</h4>
                  {resume.is_default && (
                    <span
                      style={{
                        backgroundColor: '#28a745',
                        color: 'white',
                        padding: '2px 8px',
                        borderRadius: '12px',
                        fontSize: '12px'
                      }}
                    >
                      Default
                    </span>
                  )}
                </div>
                <p style={{ margin: '0', fontSize: '12px', color: '#666' }}>
                  {formatDate(resume.created_at)}
                </p>
              </div>
              
              <div style={{ marginBottom: '12px' }}>
                <button 
                  className="btn btn-primary"
                  style={{ marginRight: '8px', fontSize: '12px' }}
                  onClick={() => window.open(resume.file, '_blank')}
                >
                  Download
                </button>
                {!resume.is_default && (
                  <button 
                    className="btn btn-secondary"
                    style={{ marginRight: '8px', fontSize: '12px' }}
                    onClick={() => handleSetDefault(resume.id)}
                  >
                    Set as Default
                  </button>
                )}
                <button 
                  className="btn btn-danger"
                  style={{ fontSize: '12px' }}
                  onClick={() => handleDeleteResume(resume.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card text-center">
          <h3>No Resumes Uploaded</h3>
          <p style={{ color: '#666', marginBottom: '20px' }}>
            Upload your first resume to get started with your job applications.
          </p>
          <button 
            onClick={() => setShowUploadForm(true)}
            className="btn btn-primary"
          >
            Upload Your First Resume
          </button>
        </div>
      )}
    </div>
  );
};

export default ResumeManager;
