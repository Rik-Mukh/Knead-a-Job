/**
 * Job Application Service
 * 
 * This module provides API functions for managing job applications.
 * It handles all HTTP requests to the Django backend for job application data.
 */

import axios from 'axios';

// Base URL for job application API endpoints
const API_BASE_URL = 'http://127.0.0.1:8000/api/applications/';


/**
 * Job Application Service
 * 
 * Object containing methods for all job application API operations.
 * Each method handles HTTP requests to the Django backend.
 */
export const applicationService = {
  /**
   * Get all job applications for the current user
   * 
   * @returns {Promise<Array>} Array of job application objects
   */
  async getAll() {
    try {
      const response = await axios.get(API_BASE_URL);
      return response.data;
    } catch (error) {
      console.error("Error fetching job applications:", error);
      throw error;
    }
  },

  /**
   * Get a specific job application by ID
   * 
   * @param {number} id - The ID of the job application
   * @returns {Promise<Object>} Job application object
   */
  async getById(id) {
    const response = await axios.get(`${API_BASE_URL}${id}/`);
    return response.data;
  },

  /**
   * Create a new job application
   * 
   * @param {Object} data - Job application data
   * @returns {Promise<Object>} Created job application object
   */
  async create(data) {
    const response = await axios.post(API_BASE_URL, data);
    return response.data;
  },

  /**
   * Update an existing job application
   * 
   * @param {number} id - The ID of the job application to update
   * @param {Object} data - Updated job application data
   * @returns {Promise<Object>} Updated job application object
   */
  async update(id, data) {
    const response = await axios.put(`${API_BASE_URL}${id}/`, data);
    return response.data;
  },

  /**
   * Delete a job application
   * 
   * @param {number} id - The ID of the job application to delete
   * @returns {Promise<void>}
   */
  async delete(id) {
    await axios.delete(`${API_BASE_URL}${id}/`);
  },

  /**
   * Get application statistics for the current user
   * 
   * @returns {Promise<Object>} Object containing application statistics
   */
  async getStats() {
    const response = await axios.get(`${API_BASE_URL}stats/`);
    return response.data;
  },
};
