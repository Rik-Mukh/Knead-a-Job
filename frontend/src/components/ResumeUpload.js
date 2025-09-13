import React, { useState } from 'react';

const ResumeUpload = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    title: '',
    is_default: false,
  });
  const [file, setFile] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.type === 'checkbox' ? e.target.checked : e.target.value,
    });
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      onSubmit(formData, file);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card">
      <h3>Upload Resume</h3>
      
      <div className="form-group">
        <label className="form-label">Title *</label>
        <input
          type="text"
          name="title"
          value={formData.title}
          onChange={handleChange}
          className="form-control"
          placeholder="e.g., Software Engineer Resume 2024"
          required
        />
      </div>

      <div className="form-group">
        <label className="form-label">Resume File *</label>
        <input
          type="file"
          onChange={handleFileChange}
          className="form-control"
          accept=".pdf,.doc,.docx"
          required
        />
        <small style={{ color: '#666' }}>
          Supported formats: PDF, DOC, DOCX
        </small>
      </div>

      <div className="form-group">
        <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <input
            type="checkbox"
            name="is_default"
            checked={formData.is_default}
            onChange={handleChange}
          />
          Set as default resume
        </label>
      </div>

      <div className="form-group">
        <button type="submit" className="btn btn-primary">
          Upload Resume
        </button>
      </div>
    </form>
  );
};

export default ResumeUpload;
