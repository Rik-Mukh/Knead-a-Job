/**
 * Notification Service
 * 
 * This module provides API functions for managing notifications.
 * It handles all HTTP requests to the Django backend for notification data.
 */

import axios from 'axios';

// Base URL for notification API endpoints
const API_BASE_URL = 'http://127.0.0.1:8000/api/notifications/';

/**
 * Notification Service
 * 
 * Object containing methods for all notification API operations.
 * Each method handles HTTP requests to the Django backend.
 */
export const notificationService = {
  /**
   * Get all notifications for the current user
   * 
   * @returns {Promise<Array>} Array of notification objects
   */
  async getAll() {
    try {
      console.log('DEBUG: Fetching notifications from:', API_BASE_URL);
      const response = await axios.get(API_BASE_URL);
      console.log('DEBUG: API response status:', response.status);
      console.log('DEBUG: API response data:', response.data);
      return response.data;
    } catch (error) {
      console.error("Error fetching notifications:", error);
      console.error("Error details:", error.response?.data);
      throw error;
    }
  },

  /**
   * Get a specific notification by ID
   * 
   * @param {number} id - The ID of the notification
   * @returns {Promise<Object>} Notification object
   */
  async getById(id) {
    const response = await axios.get(`${API_BASE_URL}${id}/`);
    return response.data;
  },

  /**
   * Create a new notification
   * 
   * @param {Object} data - Notification data
   * @returns {Promise<Object>} Created notification object
   */
  async create(data) {
    const response = await axios.post(API_BASE_URL, data);
    return response.data;
  },

  /**
   * Mark a notification as read
   * 
   * @param {number} id - The ID of the notification to mark as read
   * @returns {Promise<Object>} Response object
   */
  async markAsRead(id) {
    const response = await axios.post(`${API_BASE_URL}${id}/mark_read/`);
    return response.data;
  },

  /**
   * Get count of unread notifications
   * 
   * @returns {Promise<Object>} Object containing unread count
   */
  async getUnreadCount() {
    const response = await axios.get(`${API_BASE_URL}unread_count/`);
    return response.data;
  },

  /**
   * Delete a notification
   * 
   * @param {number} id - The ID of the notification to delete
   * @returns {Promise<void>}
   */
  async delete(id) {
    await axios.delete(`${API_BASE_URL}${id}/`);
  },
};