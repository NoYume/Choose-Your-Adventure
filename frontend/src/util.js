const API_BASE_URL = process.env.VITE_VERCEL_ENV === 'production'
  ? process.env.VITE_API_URL
  : 'http://localhost:8000/api';

export { API_BASE_URL };