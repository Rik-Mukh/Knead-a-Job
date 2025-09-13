/**
 * Resume Service
 * 
 * This module provides API functions for managing resume files.
 * It handles all HTTP requests to the Django backend for resume data.
 */

import axios from 'axios';

// Base URL for resume API endpoints
const API_BASE_URL = '/api/resumes/';

/**
 * Resume Service
 * 
 * Object containing methods for all resume API operations.
 * Each method handles HTTP requests to the Django backend.
 */
export const resumeService = {
  /**
   * Get all resumes for the current user
   * 
   * @returns {Promise<Array>} Array of resume objects
   */
  async getAll() {
    const response = await axios.get(API_BASE_URL);
    return response.data;
  },

  /**
   * Get a specific resume by ID
   * 
   * @param {number} id - The ID of the resume
   * @returns {Promise<Object>} Resume object
   */
  async getById(id) {
    const response = await axios.get(`${API_BASE_URL}${id}/`);
    return response.data;
  },

  /**
   * Upload a new resume file
   * 
   * @param {FormData} data - FormData containing resume file and metadata
   * @returns {Promise<Object>} Created resume object
   */
  async create(data) {
    const response = await axios.post(API_BASE_URL, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Update an existing resume
   * 
   * @param {number} id - The ID of the resume to update
   * @param {Object} data - Updated resume data
   * @returns {Promise<Object>} Updated resume object
   */
  async update(id, data) {
    const response = await axios.put(`${API_BASE_URL}${id}/`, data);
    return response.data;
  },

  /**
   * Delete a resume
   * 
   * @param {number} id - The ID of the resume to delete
   * @returns {Promise<void>}
   */
  async delete(id) {
    await axios.delete(`${API_BASE_URL}${id}/`);
  },

  /**
   * Set a resume as the default resume for the current user
   * 
   * @param {number} id - The ID of the resume to set as default
   * @returns {Promise<Object>} Response object
   */
  async setDefault(id) {
    const response = await axios.post(`${API_BASE_URL}${id}/set_default/`);
    return response.data;
  },

  /**
   * Get the default resume for the current user
   * 
   * @returns {Promise<Object>} Default resume object
   */
  async getDefault() {
    const response = await axios.get(`${API_BASE_URL}default/`);
    return response.data;
  },
};
