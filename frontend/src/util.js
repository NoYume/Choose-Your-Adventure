const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? process.env.REACT_APP_API_URL || process.env.VITE_API_URL
  : 'http://localhost:8000';

export { API_BASE_URL };