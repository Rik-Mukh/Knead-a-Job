import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

// Configure axios for CSRF token handling and cookies
axios.defaults.withCredentials = true;

const gmailService = {
  // Get recent emails
  async fetchMessages() {
    try {
      // First get CSRF token
      const csrfResponse = await axios.get(`${API_URL}/api/auth/csrf-token/`);
      const csrfToken = csrfResponse.data.csrfToken;
      
      // Set the token in the headers
      const response = await axios.get(`${API_URL}/api/gmail/messages/`, {
        headers: {
          'X-CSRFToken': csrfToken
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('Failed to fetch recent emails:', error);
      throw error;
    }
  }
};

export default gmailService;