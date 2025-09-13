import axios from 'axios';

const API_BASE_URL = '/api/applications/';

export const applicationService = {
  async getAll() {
    const response = await axios.get(API_BASE_URL);
    return response.data;
  },

  async getById(id) {
    const response = await axios.get(`${API_BASE_URL}${id}/`);
    return response.data;
  },

  async create(data) {
    const response = await axios.post(API_BASE_URL, data);
    return response.data;
  },

  async update(id, data) {
    const response = await axios.put(`${API_BASE_URL}${id}/`, data);
    return response.data;
  },

  async delete(id) {
    await axios.delete(`${API_BASE_URL}${id}/`);
  },

  async getStats() {
    const response = await axios.get(`${API_BASE_URL}stats/`);
    return response.data;
  },
};
