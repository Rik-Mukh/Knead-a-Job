import React, { useState } from 'react';

const JobApplicationForm = ({ onSubmit, initialData = {} }) => {
  const [formData, setFormData] = useState({
    company_name: initialData.company_name || '',
    position: initialData.position || '',
    job_url: initialData.job_url || '',
    status: initialData.status || 'applied',
    applied_date: initialData.applied_date || new Date().toISOString().split('T')[0],
    notes: initialData.notes || '',
    salary_range: initialData.salary_range || '',
    location: initialData.location || '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="card">
      <h3>{initialData.id ? 'Edit Application' : 'Add New Application'}</h3>
      
      <div className="form-group">
        <label className="form-label">Company Name *</label>
        <input
          type="text"
          name="company_name"
          value={formData.company_name}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>

      <div className="form-group">
        <label className="form-label">Position *</label>
        <input
          type="text"
          name="position"
          value={formData.position}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>

      <div className="form-group">
        <label className="form-label">Job URL</label>
        <input
          type="url"
          name="job_url"
          value={formData.job_url}
          onChange={handleChange}
          className="form-control"
        />
      </div>

      <div className="form-group">
        <label className="form-label">Status</label>
        <select
          name="status"
          value={formData.status}
          onChange={handleChange}
          className="form-control"
        >
          <option value="applied">Applied</option>
          <option value="interview">Interview</option>
          <option value="rejected">Rejected</option>
          <option value="accepted">Accepted</option>
          <option value="withdrawn">Withdrawn</option>
        </select>
      </div>

      <div className="form-group">
        <label className="form-label">Applied Date *</label>
        <input
          type="date"
          name="applied_date"
          value={formData.applied_date}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>

      <div className="form-group">
        <label className="form-label">Location</label>
        <input
          type="text"
          name="location"
          value={formData.location}
          onChange={handleChange}
          className="form-control"
        />
      </div>

      <div className="form-group">
        <label className="form-label">Salary Range</label>
        <input
          type="text"
          name="salary_range"
          value={formData.salary_range}
          onChange={handleChange}
          className="form-control"
        />
      </div>


      <div className="form-group">
        <label className="form-label">Notes</label>
        <textarea
          name="notes"
          value={formData.notes}
          onChange={handleChange}
          className="form-control"
          rows="4"
        />
      </div>

      <div className="form-group">
        <button type="submit" className="btn btn-primary">
          {initialData.id ? 'Update Application' : 'Add Application'}
        </button>
      </div>

    </form>
  );
};

export default JobApplicationForm;
