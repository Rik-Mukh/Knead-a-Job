/**
 * Meeting Notes Service
 * 
 * This module provides API functions for managing meeting notes.
 * It handles all HTTP requests to the Django backend for meeting note data.
 */

import axios from 'axios';

// Base URL for meeting notes API endpoints
const API_BASE_URL = 'http://127.0.0.1:8000/api/';

/**
 * Meeting Notes Service
 * 
 * Object containing methods for all meeting note API operations.
 * Each method handles HTTP requests to the Django backend.
 */
export const meetingNotesService = {
  /**
   * Get all meeting notes for a specific job application
   * 
   * @param {number} applicationId - The ID of the job application
   * @returns {Promise<Array>} Array of meeting note objects
   */
  async getByApplication(applicationId) {
    try {
      const response = await axios.get(`${API_BASE_URL}meeting-notes/?job_application=${applicationId}`);
      return response.data;
    } catch (error) {
      console.error("Error fetching meeting notes:", error);
      throw error;
    }
  },

  /**
   * Create a new meeting note for a job application
   * 
   * @param {number} applicationId - The ID of the job application
   * @param {Object} data - Meeting note data
   * @returns {Promise<Object>} Created meeting note object
   */
  async create(applicationId, data) {
    try {
      const response = await axios.post(`${API_BASE_URL}meeting-notes/`, {
        ...data,
        job_application: applicationId
      });
      return response.data;
    } catch (error) {
      console.error("Error creating meeting note:", error);
      throw error;
    }
  },

  /**
   * Update an existing meeting note
   * 
   * @param {number} id - The ID of the meeting note to update
   * @param {Object} data - Updated meeting note data
   * @returns {Promise<Object>} Updated meeting note object
   */
  async update(id, data) {
    try {
      const response = await axios.put(`${API_BASE_URL}meeting-notes/${id}/`, data);
      return response.data;
    } catch (error) {
      console.error("Error updating meeting note:", error);
      throw error;
    }
  },

  /**
   * Delete a meeting note
   * 
   * @param {number} id - The ID of the meeting note to delete
   * @returns {Promise<void>}
   */
  async delete(id) {
    try {
      await axios.delete(`${API_BASE_URL}meeting-notes/${id}/`);
    } catch (error) {
      console.error("Error deleting meeting note:", error);
      throw error;
    }
  },

  /**
   * Get all meeting notes
   * 
   * @returns {Promise<Array>} Array of all meeting note objects
   */
  async getAll() {
    try {
      const response = await axios.get(`${API_BASE_URL}meeting-notes/`);
      return response.data;
    } catch (error) {
      console.error("Error fetching all meeting notes:", error);
      throw error;
    }
  },
};
