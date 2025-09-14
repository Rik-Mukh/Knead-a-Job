/**
 * Resume Template Service
 * 
 * This service handles API calls for resume template management.
 * It provides methods for CRUD operations on resume templates and related data.
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class ResumeTemplateService {
  constructor() {
    this.csrfToken = null;
  }

  /**
   * Get CSRF token from Django
   * @returns {Promise<string>} The CSRF token
   */
  async getCsrfToken() {
    if (this.csrfToken) {
      return this.csrfToken;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/csrf-token/`, {
        method: 'GET',
        credentials: 'include',
      });

      if (response.ok) {
        const data = await response.json();
        this.csrfToken = data.csrfToken;
        return this.csrfToken;
      }
    } catch (error) {
      console.warn('Could not fetch CSRF token:', error);
    }

    return null;
  }

  /**
   * Get headers with CSRF token for requests
   * @returns {Promise<Object>} Headers object with CSRF token
   */
  async getHeaders() {
    const csrfToken = await this.getCsrfToken();
    const headers = {
      'Content-Type': 'application/json',
    };

    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken;
    }

    return headers;
  }
  /**
   * Get the current user's resume template
   * @returns {Promise<Object>} The resume template data
   */
  async getTemplate() {
    const response = await fetch(`${API_BASE_URL}/resume-template/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      if (response.status === 404) {
        return null; // No template found
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Create a new resume template
   * @param {Object} templateData - The template data to create
   * @returns {Promise<Object>} The created template data
   */
  async createTemplate(templateData) {
    const headers = await this.getHeaders();
    const response = await fetch(`${API_BASE_URL}/resume-template/`, {
      method: 'POST',
      headers,
      credentials: 'include',
      body: JSON.stringify(templateData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Update the current user's resume template
   * @param {Object} templateData - The updated template data
   * @returns {Promise<Object>} The updated template data
   */
  async updateTemplate(templateData) {
    console.log('updateTemplate called with:', templateData);
    
    const headers = await this.getHeaders();
    const response = await fetch(`${API_BASE_URL}/resume-template/update/`, {
      method: 'PUT',
      headers,
      credentials: 'include',
      body: JSON.stringify(templateData),
    });

    console.log('updateTemplate response status:', response.status);

    if (!response.ok) {
      const errorData = await response.json();
      console.error('updateTemplate error:', errorData);
      throw new Error(errorData.detail || errorData.error || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Delete the current user's resume template
   * @returns {Promise<void>}
   */
  async deleteTemplate() {
    const headers = await this.getHeaders();
    const response = await fetch(`${API_BASE_URL}/resume-template/`, {
      method: 'DELETE',
      headers,
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
  }

  // Experience methods
  async getExperiences() {
    try {
      const response = await fetch(`${API_BASE_URL}/experiences/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });

      if (!response.ok) {
        console.error(`Experiences API error: ${response.status}`);
        return []; // Return empty array on error
      }

      const data = await response.json();
      return Array.isArray(data) ? data : (data.results || []);
    } catch (error) {
      console.error('Error fetching experiences:', error);
      return []; // Return empty array on error
    }
  }

  async createExperience(experienceData) {
    const headers = await this.getHeaders();
    const res = await fetch(`${API_BASE_URL}/experiences/`, {
      method: 'POST',
      headers,
      credentials: 'include',
      body: JSON.stringify(experienceData),
    });
  
    if (!res.ok) {
      let detail;
      try { detail = await res.json(); } catch { detail = await res.text(); }
      throw new Error(`HTTP ${res.status}: ${typeof detail === 'string' ? detail : JSON.stringify(detail)}`);
    }
    return await res.json();
  }

  async updateExperience(id, experienceData) {
    const headers = await this.getHeaders();
    const response = await fetch(`${API_BASE_URL}/experiences/${id}/`, {
      method: 'PUT',
      headers,
      credentials: 'include',
      body: JSON.stringify(experienceData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  async deleteExperience(id) {
    const headers = await this.getHeaders();
    const response = await fetch(`${API_BASE_URL}/experiences/${id}/`, {
      method: 'DELETE',
      headers,
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
  }

  // Project methods
  async getProjects() {
    try {
      const response = await fetch(`${API_BASE_URL}/projects/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });

      if (!response.ok) {
        console.error(`Projects API error: ${response.status}`);
        return []; // Return empty array on error
      }

      const data = await response.json();
      return Array.isArray(data) ? data : (data.results || []);
    } catch (error) {
      console.error('Error fetching projects:', error);
      return []; // Return empty array on error
    }
  }

  async createProject(projectData) {
    const headers = await this.getHeaders();
    const response = await fetch(`${API_BASE_URL}/projects/`, {
      method: 'POST',
      headers,
      credentials: 'include',
      body: JSON.stringify(projectData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  async updateProject(id, projectData) {
    const headers = await this.getHeaders();
    const response = await fetch(`${API_BASE_URL}/projects/${id}/`, {
      method: 'PUT',
      headers,
      credentials: 'include',
      body: JSON.stringify(projectData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  async deleteProject(id) {
    const headers = await this.getHeaders();
    const response = await fetch(`${API_BASE_URL}/projects/${id}/`, {
      method: 'DELETE',
      headers,
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
  }

  // Education methods
  async getEducations() {
    try {
      const response = await fetch(`${API_BASE_URL}/educations/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });

      if (!response.ok) {
        console.error(`Educations API error: ${response.status}`);
        return []; // Return empty array on error
      }

      const data = await response.json();
      return Array.isArray(data) ? data : (data.results || []);
    } catch (error) {
      console.error('Error fetching educations:', error);
      return []; // Return empty array on error
    }
  }

  async createEducation(educationData) {
    const headers = await this.getHeaders();
    const response = await fetch(`${API_BASE_URL}/educations/`, {
      method: 'POST',
      headers,
      credentials: 'include',
      body: JSON.stringify(educationData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  async updateEducation(id, educationData) {
    const headers = await this.getHeaders();
    const response = await fetch(`${API_BASE_URL}/educations/${id}/`, {
      method: 'PUT',
      headers,
      credentials: 'include',
      body: JSON.stringify(educationData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  async deleteEducation(id) {
    const headers = await this.getHeaders();
    const response = await fetch(`${API_BASE_URL}/educations/${id}/`, {
      method: 'DELETE',
      headers,
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
  }

  // Resume generation methods
  async generateResume() {
    const response = await fetch(`${API_BASE_URL}/resume-template/generate/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  async generateFreshResume() {
    const response = await fetch(`${API_BASE_URL}/resume-template/generate_fresh/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }
}

export const resumeTemplateService = new ResumeTemplateService();