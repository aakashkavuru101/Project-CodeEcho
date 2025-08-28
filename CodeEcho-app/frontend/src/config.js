// Configuration for different environments
const config = {
  development: {
    API_BASE_URL: 'http://localhost:5000',
  },
  production: {
    API_BASE_URL: process.env.VITE_API_BASE_URL || window.location.origin,
  },
};

const environment = process.env.NODE_ENV || 'development';

export default config[environment];