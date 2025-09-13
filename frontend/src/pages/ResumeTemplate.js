import React, { useState, useEffect } from 'react';
import { marked } from 'marked';
import { resumeTemplateService } from '../services/resumeTemplateService';

const ResumeTemplate = () => {
  const [template, setTemplate] = useState(null);
  const [experiences, setExperiences] = useState([]);
  const [projects, setProjects] = useState([]);
  const [educations, setEducations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [activeTab, setActiveTab] = useState('resume-preview');
  const [resumeMarkdown, setResumeMarkdown] = useState('');
  const [resumeHtml, setResumeHtml] = useState('');

  // Form states
  const [formData, setFormData] = useState({
    name: '',
    city: '',
    email: '',
    phone: '',
    links: '',
    summary: '',
    skills: ''
  });

  useEffect(() => {
    fetchTemplateData();
  }, []);

  const fetchTemplateData = async () => {
    try {
      setLoading(true);
      
      // Fetch template data
      const templateData = await resumeTemplateService.getTemplate();
      if (templateData) {
        setTemplate(templateData);
        setFormData({
          name: templateData.name || '',
          city: templateData.city || '',
          email: templateData.email || '',
          phone: templateData.phone || '',
          links: templateData.links || '',
          summary: templateData.summary || '',
          skills: templateData.skills || ''
        });
      }

      // Fetch related data
      const [experiencesData, projectsData, educationsData] = await Promise.all([
        resumeTemplateService.getExperiences(),
        resumeTemplateService.getProjects(),
        resumeTemplateService.getEducations()
      ]);

      setExperiences(experiencesData || []);
      setProjects(projectsData || []);
      setEducations(educationsData || []);
    } catch (error) {
      console.error('Error fetching template data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSaveTemplate = async () => {
    try {
      setSaving(true);
      
      if (template) {
        await resumeTemplateService.updateTemplate(formData);
      } else {
        await resumeTemplateService.createTemplate(formData);
      }
      
      await fetchTemplateData();
      alert('Resume template saved successfully!');
    } catch (error) {
      console.error('Error saving template:', error);
      alert('Error saving template: ' + error.message);
    } finally {
      setSaving(false);
    }
  };

  const generateResume = async () => {
    try {
      const response = await resumeTemplateService.generateResume();
      setResumeMarkdown(response.markdown);
      
      // Convert Markdown to HTML
      const html = marked(response.markdown, { breaks: true });
      setResumeHtml(html);
    } catch (error) {
      console.error('Error generating resume:', error);
      alert('Error generating resume: ' + error.message);
    }
  };

  const handleAddExperience = () => {
    const newExperience = {
      company: '',
      position: '',
      location: '',
      start_date: '',
      end_date: '',
      is_current: false,
      description: '',
      order: experiences.length
    };
    setExperiences([...experiences, newExperience]);
  };

  const handleUpdateExperience = (index, field, value) => {
    const updated = [...experiences];
    updated[index] = { ...updated[index], [field]: value };
    setExperiences(updated);
  };

  const handleSaveExperience = async (experience, index) => {
    try {
      // Prepare experience data - remove end_date if is_current is true
      const experienceData = { ...experience };
      if (experienceData.is_current) {
        experienceData.end_date = null; // Set to null instead of empty string
      }

      if (experience.id) {
        await resumeTemplateService.updateExperience(experience.id, experienceData);
      } else {
        await resumeTemplateService.createExperience(experienceData);
      }
      await fetchTemplateData();
    } catch (error) {
      console.error('Error saving experience:', error);
      alert('Error saving experience: ' + error.message);
    }
  };

  const handleDeleteExperience = async (id) => {
    if (window.confirm('Are you sure you want to delete this experience?')) {
      try {
        await resumeTemplateService.deleteExperience(id);
        await fetchTemplateData();
      } catch (error) {
        console.error('Error deleting experience:', error);
        alert('Error deleting experience: ' + error.message);
      }
    }
  };

  const handleAddProject = () => {
    const newProject = {
      name: '',
      description: '',
      technologies: '',
      url: '',
      start_date: '',
      end_date: '',
      is_ongoing: false,
      order: projects.length
    };
    setProjects([...projects, newProject]);
  };

  const handleUpdateProject = (index, field, value) => {
    const updated = [...projects];
    updated[index] = { ...updated[index], [field]: value };
    setProjects(updated);
  };

  const handleSaveProject = async (project, index) => {
    try {
      // Prepare project data - remove end_date if is_ongoing is true
      const projectData = { ...project };
      if (projectData.is_ongoing) {
        projectData.end_date = null; // Set to null instead of empty string
      }

      if (project.id) {
        await resumeTemplateService.updateProject(project.id, projectData);
      } else {
        await resumeTemplateService.createProject(projectData);
      }
      await fetchTemplateData();
    } catch (error) {
      console.error('Error saving project:', error);
      alert('Error saving project: ' + error.message);
    }
  };

  const handleDeleteProject = async (id) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await resumeTemplateService.deleteProject(id);
        await fetchTemplateData();
      } catch (error) {
        console.error('Error deleting project:', error);
        alert('Error deleting project: ' + error.message);
      }
    }
  };

  const handleAddEducation = () => {
    const newEducation = {
      institution: '',
      degree: '',
      field_of_study: '',
      location: '',
      start_date: '',
      end_date: '',
      is_current: false,
      gpa: '',
      order: educations.length
    };
    setEducations([...educations, newEducation]);
  };

  const handleUpdateEducation = (index, field, value) => {
    const updated = [...educations];
    updated[index] = { ...updated[index], [field]: value };
    setEducations(updated);
  };

  const handleSaveEducation = async (education, index) => {
    try {
      // Prepare education data - remove end_date if is_current is true
      const educationData = { ...education };
      if (educationData.is_current) {
        educationData.end_date = null; // Set to null instead of empty string
      }

      if (education.id) {
        await resumeTemplateService.updateEducation(education.id, educationData);
      } else {
        await resumeTemplateService.createEducation(educationData);
      }
      await fetchTemplateData();
    } catch (error) {
      console.error('Error saving education:', error);
      alert('Error saving education: ' + error.message);
    }
  };

  const handleDeleteEducation = async (id) => {
    if (window.confirm('Are you sure you want to delete this education?')) {
      try {
        await resumeTemplateService.deleteEducation(id);
        await fetchTemplateData();
      } catch (error) {
        console.error('Error deleting education:', error);
        alert('Error deleting education: ' + error.message);
      }
    }
  };

  if (loading) {
    return (
      <div className="text-center">
        <h2>Resume Template</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h2>Resume Template</h2>
        <button 
          className="btn btn-primary" 
          onClick={handleSaveTemplate}
          disabled={saving}
        >
          {saving ? 'Saving...' : 'Save Template'}
        </button>
      </div>

      {/* Tab Navigation */}
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', borderBottom: '1px solid #ddd' }}>
          {['resume-preview', 'personal', 'experience', 'projects', 'education'].map(tab => (
            <button
              key={tab}
              className={`btn ${activeTab === tab ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveTab(tab)}
              style={{ 
                marginRight: '8px', 
                borderRadius: '4px 4px 0 0',
                borderBottom: activeTab === tab ? 'none' : '1px solid #ddd'
              }}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Resume Preview Tab */}
      {activeTab === 'resume-preview' && (
        <div className="card">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h3>Resume Preview</h3>
            <button 
              className="btn btn-primary"
              onClick={generateResume}
            >
              Generate Resume
            </button>
          </div>
          
          {resumeHtml ? (
            <div 
              className="resume-content"
              dangerouslySetInnerHTML={{ __html: resumeHtml }}
              style={{
                border: '1px solid #ddd',
                padding: '20px',
                backgroundColor: 'white',
                fontFamily: 'Arial, sans-serif',
                lineHeight: '1.6',
                maxWidth: '800px',
                margin: '0 auto'
              }}
            />
          ) : (
            <div className="text-center text-muted">
              <p>Click "Generate Resume" to create your resume preview</p>
            </div>
          )}
        </div>
      )}

      {/* Personal Information Tab */}
      {activeTab === 'personal' && (
        <div className="card">
          <h3>Personal Information</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
            <div>
              <label>Full Name *</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                className="form-control"
                required
              />
            </div>
            <div>
              <label>City *</label>
              <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleInputChange}
                className="form-control"
                required
              />
            </div>
            <div>
              <label>Email *</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className="form-control"
                required
              />
            </div>
            <div>
              <label>Phone *</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleInputChange}
                className="form-control"
                required
              />
            </div>
          </div>
          <div style={{ marginBottom: '16px' }}>
            <label>Links (one per line)</label>
            <textarea
              name="links"
              value={formData.links}
              onChange={handleInputChange}
              className="form-control"
              rows="3"
              placeholder="GitHub: https://github.com/username&#10;LinkedIn: https://linkedin.com/in/username"
            />
          </div>
          <div style={{ marginBottom: '16px' }}>
            <label>Professional Summary</label>
            <textarea
              name="summary"
              value={formData.summary}
              onChange={handleInputChange}
              className="form-control"
              rows="4"
              placeholder="Brief summary of your professional background and career objectives..."
            />
          </div>
          <div>
            <label>Skills (one per line or comma-separated)</label>
            <textarea
              name="skills"
              value={formData.skills}
              onChange={handleInputChange}
              className="form-control"
              rows="3"
              placeholder="JavaScript, React, Python, Django&#10;Project Management, Team Leadership"
            />
          </div>
        </div>
      )}

      {/* Experience Tab */}
      {activeTab === 'experience' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3>Work Experience</h3>
            <button className="btn btn-primary" onClick={handleAddExperience}>
              Add Experience
            </button>
          </div>
          {(experiences || []).map((exp, index) => (
            <div key={index} className="card" style={{ marginBottom: '16px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
                <div>
                  <label>Company *</label>
                  <input
                    type="text"
                    value={exp.company}
                    onChange={(e) => handleUpdateExperience(index, 'company', e.target.value)}
                    className="form-control"
                  />
                </div>
                <div>
                  <label>Position *</label>
                  <input
                    type="text"
                    value={exp.position}
                    onChange={(e) => handleUpdateExperience(index, 'position', e.target.value)}
                    className="form-control"
                  />
                </div>
                <div>
                  <label>Location</label>
                  <input
                    type="text"
                    value={exp.location}
                    onChange={(e) => handleUpdateExperience(index, 'location', e.target.value)}
                    className="form-control"
                  />
                </div>
                <div>
                  <label>Start Date *</label>
                  <input
                    type="date"
                    value={exp.start_date}
                    onChange={(e) => handleUpdateExperience(index, 'start_date', e.target.value)}
                    className="form-control"
                  />
                </div>
                <div>
                  <label>End Date</label>
                  <input
                    type="date"
                    value={exp.end_date}
                    onChange={(e) => handleUpdateExperience(index, 'end_date', e.target.value)}
                    className="form-control"
                    disabled={exp.is_current}
                  />
                </div>
                <div style={{ display: 'flex', alignItems: 'center', marginTop: '24px' }}>
                  <input
                    type="checkbox"
                    checked={exp.is_current}
                    onChange={(e) => handleUpdateExperience(index, 'is_current', e.target.checked)}
                    style={{ marginRight: '8px' }}
                  />
                  <label style={{ margin: 0 }}>Current Position</label>
                </div>
              </div>
              <div style={{ marginBottom: '16px' }}>
                <label>Description *</label>
                <textarea
                  value={exp.description}
                  onChange={(e) => handleUpdateExperience(index, 'description', e.target.value)}
                  className="form-control"
                  rows="3"
                  placeholder="Describe your responsibilities and achievements..."
                />
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button 
                  className="btn btn-success" 
                  onClick={() => handleSaveExperience(exp, index)}
                >
                  {exp.id ? 'Update' : 'Save'}
                </button>
                {exp.id && (
                  <button 
                    className="btn btn-danger" 
                    onClick={() => handleDeleteExperience(exp.id)}
                  >
                    Delete
                  </button>
                )}
              </div>
            </div>
          ))}
          {experiences.length === 0 && (
            <div className="card text-center">
              <p>No work experience added yet. Click "Add Experience" to get started!</p>
            </div>
          )}
        </div>
      )}

      {/* Projects Tab */}
      {activeTab === 'projects' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3>Projects</h3>
            <button className="btn btn-primary" onClick={handleAddProject}>
              Add Project
            </button>
          </div>
          {(projects || []).map((project, index) => (
            <div key={index} className="card" style={{ marginBottom: '16px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
                <div>
                  <label>Project Name *</label>
                  <input
                    type="text"
                    value={project.name}
                    onChange={(e) => handleUpdateProject(index, 'name', e.target.value)}
                    className="form-control"
                  />
                </div>
                <div>
                  <label>Technologies</label>
                  <input
                    type="text"
                    value={project.technologies}
                    onChange={(e) => handleUpdateProject(index, 'technologies', e.target.value)}
                    className="form-control"
                    placeholder="React, Node.js, MongoDB"
                  />
                </div>
                <div>
                  <label>Start Date *</label>
                  <input
                    type="date"
                    value={project.start_date}
                    onChange={(e) => handleUpdateProject(index, 'start_date', e.target.value)}
                    className="form-control"
                  />
                </div>
                <div>
                  <label>End Date</label>
                  <input
                    type="date"
                    value={project.end_date}
                    onChange={(e) => handleUpdateProject(index, 'end_date', e.target.value)}
                    className="form-control"
                    disabled={project.is_ongoing}
                  />
                </div>
                <div>
                  <label>Project URL</label>
                  <input
                    type="url"
                    value={project.url}
                    onChange={(e) => handleUpdateProject(index, 'url', e.target.value)}
                    className="form-control"
                    placeholder="https://github.com/username/project"
                  />
                </div>
                <div style={{ display: 'flex', alignItems: 'center', marginTop: '24px' }}>
                  <input
                    type="checkbox"
                    checked={project.is_ongoing}
                    onChange={(e) => handleUpdateProject(index, 'is_ongoing', e.target.checked)}
                    style={{ marginRight: '8px' }}
                  />
                  <label style={{ margin: 0 }}>Ongoing Project</label>
                </div>
              </div>
              <div style={{ marginBottom: '16px' }}>
                <label>Description *</label>
                <textarea
                  value={project.description}
                  onChange={(e) => handleUpdateProject(index, 'description', e.target.value)}
                  className="form-control"
                  rows="3"
                  placeholder="Describe the project, your role, and key achievements..."
                />
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button 
                  className="btn btn-success" 
                  onClick={() => handleSaveProject(project, index)}
                >
                  {project.id ? 'Update' : 'Save'}
                </button>
                {project.id && (
                  <button 
                    className="btn btn-danger" 
                    onClick={() => handleDeleteProject(project.id)}
                  >
                    Delete
                  </button>
                )}
              </div>
            </div>
          ))}
          {projects.length === 0 && (
            <div className="card text-center">
              <p>No projects added yet. Click "Add Project" to get started!</p>
            </div>
          )}
        </div>
      )}

      {/* Education Tab */}
      {activeTab === 'education' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3>Education</h3>
            <button className="btn btn-primary" onClick={handleAddEducation}>
              Add Education
            </button>
          </div>
          {(educations || []).map((edu, index) => (
            <div key={index} className="card" style={{ marginBottom: '16px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
                <div>
                  <label>Institution *</label>
                  <input
                    type="text"
                    value={edu.institution}
                    onChange={(e) => handleUpdateEducation(index, 'institution', e.target.value)}
                    className="form-control"
                  />
                </div>
                <div>
                  <label>Degree *</label>
                  <input
                    type="text"
                    value={edu.degree}
                    onChange={(e) => handleUpdateEducation(index, 'degree', e.target.value)}
                    className="form-control"
                  />
                </div>
                <div>
                  <label>Field of Study</label>
                  <input
                    type="text"
                    value={edu.field_of_study}
                    onChange={(e) => handleUpdateEducation(index, 'field_of_study', e.target.value)}
                    className="form-control"
                  />
                </div>
                <div>
                  <label>Location</label>
                  <input
                    type="text"
                    value={edu.location}
                    onChange={(e) => handleUpdateEducation(index, 'location', e.target.value)}
                    className="form-control"
                  />
                </div>
                <div>
                  <label>Start Date *</label>
                  <input
                    type="date"
                    value={edu.start_date}
                    onChange={(e) => handleUpdateEducation(index, 'start_date', e.target.value)}
                    className="form-control"
                  />
                </div>
                <div>
                  <label>End Date</label>
                  <input
                    type="date"
                    value={edu.end_date}
                    onChange={(e) => handleUpdateEducation(index, 'end_date', e.target.value)}
                    className="form-control"
                    disabled={edu.is_current}
                  />
                </div>
                <div>
                  <label>GPA</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    max="4"
                    value={edu.gpa}
                    onChange={(e) => handleUpdateEducation(index, 'gpa', e.target.value)}
                    className="form-control"
                  />
                </div>
                <div style={{ display: 'flex', alignItems: 'center', marginTop: '24px' }}>
                  <input
                    type="checkbox"
                    checked={edu.is_current}
                    onChange={(e) => handleUpdateEducation(index, 'is_current', e.target.checked)}
                    style={{ marginRight: '8px' }}
                  />
                  <label style={{ margin: 0 }}>Currently Enrolled</label>
                </div>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button 
                  className="btn btn-success" 
                  onClick={() => handleSaveEducation(edu, index)}
                >
                  {edu.id ? 'Update' : 'Save'}
                </button>
                {edu.id && (
                  <button 
                    className="btn btn-danger" 
                    onClick={() => handleDeleteEducation(edu.id)}
                  >
                    Delete
                  </button>
                )}
              </div>
            </div>
          ))}
          {educations.length === 0 && (
            <div className="card text-center">
              <p>No education added yet. Click "Add Education" to get started!</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ResumeTemplate;
