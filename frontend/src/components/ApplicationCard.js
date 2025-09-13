import React from 'react';

const ApplicationCard = ({ application, onEdit, onDelete, onTrack }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'applied': return '#17a2b8';
      case 'interview': return '#ffc107';
      case 'rejected': return '#dc3545';
      case 'accepted': return '#28a745';
      case 'withdrawn': return '#6c757d';
      default: return '#6c757d';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h4 style={{ margin: '0 0 8px 0' }}>{application.position}</h4>
          <p style={{ margin: '0 0 8px 0', color: '#666' }}>{application.company_name}</p>
          {application.location && (
            <p style={{ margin: '0 0 8px 0', color: '#666' }}>📍 {application.location}</p>
          )}
          {application.salary_range && (
            <p style={{ margin: '0 0 8px 0', color: '#666' }}>💰 {application.salary_range}</p>
          )}
        </div>
        <div style={{ textAlign: 'right' }}>
          <span
            style={{
              backgroundColor: getStatusColor(application.status),
              color: 'white',
              padding: '4px 8px',
              borderRadius: '12px',
              fontSize: '12px',
              textTransform: 'capitalize'
            }}
          >
            {application.status}
          </span>
          <p style={{ margin: '8px 0 0 0', fontSize: '14px', color: '#666' }}>
            Applied: {formatDate(application.applied_date)}
          </p>
        </div>
      </div>
      
      {application.notes && (
        <div style={{ marginTop: '12px' }}>
          <p style={{ margin: '0', fontSize: '14px' }}>{application.notes}</p>
        </div>
      )}
      
      {application.job_url && (
        <div style={{ marginTop: '12px' }}>
          <a 
            href={application.job_url} 
            target="_blank" 
            rel="noopener noreferrer"
            style={{ color: '#007bff', textDecoration: 'none' }}
          >
            View Job Posting →
          </a>
        </div>
      )}
      
      <div style={{ marginTop: '16px', display: 'flex', gap: '8px' }}>
        <button 
          onClick={() => onEdit(application)}
          className="btn btn-secondary"
          style={{ padding: '6px 12px', fontSize: '12px' }}
        >
          Edit
        </button>
        <button 
          onClick={() => onDelete(application.id)}
          className="btn btn-danger"
          style={{ padding: '6px 12px', fontSize: '12px' }}
        >
          Delete
        </button>
        <button 
          onClick={() => onTrack(application.id)}
          className="btn btn-outline-primary"
          style={{ padding: '6px 12px', fontSize: '12px' }}
        >
          Track Response
        </button>
      </div>
    </div>
  );
};

export default ApplicationCard;
