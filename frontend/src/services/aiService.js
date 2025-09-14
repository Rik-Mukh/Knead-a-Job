/**
 * AI Service for Content Generation
 * 
 * This service handles API calls to the backend AI endpoints for generating
 * project descriptions, experience summaries, and personal summaries.
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class AIService {
  /**
   * Generate a project description using AI
   * @param {Object} data - Project data
   * @param {string} data.project_name - Name of the project
   * @param {string} data.technologies - Technologies used (optional)
   * @param {string} data.existing_description - Existing description (optional)
   * @returns {Promise<string>} Generated description
   */
  async generateProjectDescription(data) {
    try {
      const response = await fetch(`${API_BASE_URL}/ai/generate-project-description/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate project description');
      }

      const result = await response.json();
      return result.generated_description;
    } catch (error) {
      console.error('Error generating project description:', error);
      throw error;
    }
  }

  /**
   * Generate an experience summary using AI
   * @param {Object} data - Experience data
   * @param {string} data.company - Company name
   * @param {string} data.position - Job position
   * @param {string} data.existing_description - Existing description (must be at least 500 chars)
   * @returns {Promise<string>} Generated description
   */
  async generateExperienceSummary(data) {
    try {
      const response = await fetch(`${API_BASE_URL}/ai/generate-experience-summary/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate experience summary');
      }

      const result = await response.json();
      return result.generated_description;
    } catch (error) {
      console.error('Error generating experience summary:', error);
      throw error;
    }
  }

  /**
   * Generate a personal summary using AI
   * @param {Object} data - Personal data
   * @param {string} data.existing_summary - Existing summary (optional)
   * @param {string} data.name - User's name (optional)
   * @param {string} data.skills - User's skills (optional)
   * @returns {Promise<string>} Generated summary
   */
  async generatePersonalSummary(data) {
    try {
      const response = await fetch(`${API_BASE_URL}/ai/generate-personal-summary/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate personal summary');
      }

      const result = await response.json();
      return result.generated_summary;
    } catch (error) {
      console.error('Error generating personal summary:', error);
      throw error;
    }
  }
}

// Create and export a singleton instance
export const aiService = new AIService();
