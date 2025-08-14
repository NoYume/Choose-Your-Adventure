const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:8000/api';
console.log(API_BASE_URL);
console.log(process.env.VITE_API_URL);
console.log(process.env.API_URL);
export { API_BASE_URL };