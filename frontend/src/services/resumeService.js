import axios from 'axios';

const API_BASE_URL = '/api/resumes/';

export const resumeService = {
  async getAll() {
    const response = await axios.get(API_BASE_URL);
    return response.data;
  },

  async getById(id) {
    const response = await axios.get(`${API_BASE_URL}${id}/`);
    return response.data;
  },

  async create(data) {
    const response = await axios.post(API_BASE_URL, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async update(id, data) {
    const response = await axios.put(`${API_BASE_URL}${id}/`, data);
    return response.data;
  },

  async delete(id) {
    await axios.delete(`${API_BASE_URL}${id}/`);
  },

  async setDefault(id) {
    const response = await axios.post(`${API_BASE_URL}${id}/set_default/`);
    return response.data;
  },

  async getDefault() {
    const response = await axios.get(`${API_BASE_URL}default/`);
    return response.data;
  },
};
