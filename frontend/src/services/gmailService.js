import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

// Configure axios for CSRF token handling and cookies
axios.defaults.withCredentials = true;

const gmailService = {
  // Fetch Gmail messages and create notifications
  async fetchMessages() {
    try {
      const response = await axios.get(`${API_URL}/api/gmail/messages/`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch Gmail messages:', error);
      throw error;
    }
  }
};

export default gmailService;