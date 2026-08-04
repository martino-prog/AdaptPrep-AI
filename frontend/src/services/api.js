import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: Attach JWT Token if present
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('adaptprep_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Handle 401 Unauthorized
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('adaptprep_token');
      localStorage.removeItem('adaptprep_user');
      // Redirect to login if unauthenticated on protected routes
      if (!window.location.pathname.includes('/login') && !window.location.pathname.includes('/signup')) {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// --- Auth Endpoints ---
export const signupUser = async (username, email, password) => {
  const response = await api.post('/auth/signup', { username, email, password });
  return response.data;
};

export const loginUser = async (username_or_email, password) => {
  const response = await api.post('/auth/login', { username_or_email, password });
  return response.data;
};

export const fetchCurrentUser = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

// --- Questions Endpoints ---
export const fetchQuestions = async (topic = '', difficulty = '') => {
  const params = {};
  if (topic) params.topic = topic;
  if (difficulty) params.difficulty = difficulty;
  const response = await api.get('/questions', { params });
  return response.data;
};

export const fetchQuestionById = async (id) => {
  const response = await api.get(`/questions/${id}`);
  return response.data;
};

export const fetchNextQuestion = async () => {
  const response = await api.get('/questions/next-question');
  return response.data;
};

// --- Submissions & Code Execution Endpoints ---
export const submitCode = async (questionId, language, code) => {
  const response = await api.post('/submissions/submit', {
    question_id: questionId,
    language,
    code,
  });
  return response.data;
};

export const fetchSubmissionHistory = async () => {
  const response = await api.get('/submissions/history');
  return response.data;
};

// --- Analytics Endpoints ---
export const fetchDashboardData = async () => {
  const response = await api.get('/analytics/dashboard');
  return response.data;
};

export const fetchUserScores = async () => {
  const response = await api.get('/analytics/scores');
  return response.data;
};

export default api;
