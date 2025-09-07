import axios from 'axios';
import { Grant, User, GrantFilters, PaginatedResponse, ApiResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const grantsApi = {
  // Get grants with optional filters
  getGrants: async (filters: GrantFilters = {}, page = 1, perPage = 20): Promise<PaginatedResponse<Grant>> => {
    const params = new URLSearchParams();
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        if (Array.isArray(value)) {
          params.append(key, value.join(','));
        } else {
          params.append(key, value.toString());
        }
      }
    });
    
    params.append('page', page.toString());
    params.append('per_page', perPage.toString());
    
    const response = await api.get(`/api/grants?${params.toString()}`);
    return response.data;
  },

  // Get single grant by ID
  getGrant: async (grantId: string): Promise<ApiResponse<Grant>> => {
    const response = await api.get(`/api/grants/${grantId}`);
    return response.data;
  },

  // Search grants
  searchGrants: async (query: string): Promise<ApiResponse<Grant[]>> => {
    const response = await api.get(`/api/grants/search?q=${encodeURIComponent(query)}`);
    return response.data;
  }
};

export const authApi = {
  // Google OAuth login
  loginWithGoogle: () => {
    window.location.href = `${API_BASE_URL}/api/auth/google`;
  },

  // Microsoft OAuth login
  loginWithMicrosoft: () => {
    window.location.href = `${API_BASE_URL}/api/auth/microsoft`;
  },

  // Get current user
  getCurrentUser: async (): Promise<ApiResponse<User>> => {
    const response = await api.get('/api/me');
    return response.data;
  },

  // Logout
  logout: async (): Promise<void> => {
    try {
      await api.post('/api/auth/logout');
    } finally {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token');
        window.location.href = '/';
      }
    }
  }
};

export const userApi = {
  // Update user profile
  updateProfile: async (userData: Partial<User>): Promise<ApiResponse<User>> => {
    const response = await api.put('/api/users/profile', userData);
    return response.data;
  },

  // Update company profile
  updateCompany: async (companyData: any): Promise<ApiResponse<any>> => {
    const response = await api.put('/api/users/company', companyData);
    return response.data;
  }
};

export const paymentsApi = {
  // Create subscription checkout session
  createCheckoutSession: async (planType: 'monthly' | 'yearly'): Promise<ApiResponse<{ checkout_url: string }>> => {
    const response = await api.post('/api/payments/create-checkout-session', { plan_type: planType });
    return response.data;
  },

  // Get subscription status
  getSubscriptionStatus: async (): Promise<ApiResponse<any>> => {
    const response = await api.get('/api/payments/subscription-status');
    return response.data;
  }
};

export const aiApi = {
  // Get AI assistance for grant application
  getAssistance: async (grantId: string, questionType: string): Promise<ApiResponse<any>> => {
    const response = await api.post('/api/ai-assistant/assistance', {
      grant_id: grantId,
      question_type: questionType
    });
    return response.data;
  },

  // Generate application draft
  generateApplication: async (grantId: string, companyInfo: any): Promise<ApiResponse<any>> => {
    const response = await api.post('/api/ai-assistant/generate-application', {
      grant_id: grantId,
      company_info: companyInfo
    });
    return response.data;
  }
};

export default api;
