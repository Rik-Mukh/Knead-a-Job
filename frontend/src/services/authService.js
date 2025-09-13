import axios from 'axios';

const API_URL = "http://localhost:8000";

// Configure axios to include credentials (cookies)
axios.defaults.withCredentials = true;

const authService = {
    getGoogleLoginURL: () => {
        return `${API_URL}/accounts/google/login/?process=login&next=${API_URL}/auth-success/`;
    },
    
    checkAuthStatus: async () => {
        try {
            const response = await axios.get(`${API_URL}/api/auth/status/`);
            return response.data;
        } catch (error) {
            console.error('Auth status check failed:', error);
            return { isAuthenticated: false };
        }
    },
    
    logout: async () => {
        try {
            await axios.get(`${API_URL}/logout/`);
            return true;
        } catch (error) {
            console.error('Logout failed:', error);
            return false;
        }
    }
};

export default authService;