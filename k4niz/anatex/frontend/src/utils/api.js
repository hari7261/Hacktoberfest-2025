// Axios client for backend calls
import axios from 'axios';
export const api = axios.create({ baseURL: '/api' });
