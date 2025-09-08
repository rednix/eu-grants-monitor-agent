import axios from 'axios';
import { Grant, User, GrantFilters, PaginatedResponse, ApiResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://grant-monitor-production.up.railway.app';

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
    try {
      const params = new URLSearchParams();
      
      // Map frontend filters to simple API parameters
      if (filters.search) {
        params.append('query', filters.search);
      }
      if (filters.program) {
        params.append('program', filters.program);
      }
      if (filters.min_amount) {
        params.append('min_amount', filters.min_amount.toString());
      }
      if (filters.max_amount) {
        params.append('max_amount', filters.max_amount.toString());
      }
      if (filters.technology_areas && filters.technology_areas.length > 0) {
        params.append('technology_areas', filters.technology_areas.join(','));
      }
      
      params.append('page', page.toString());
      params.append('limit', perPage.toString());
      
      const response = await api.get(`/api/grants/simple?${params.toString()}`);
      
      // Transform simple API response to match frontend expectations
      return {
        data: response.data.grants,
        total: response.data.total_count,
        page: response.data.page,
        per_page: response.data.limit,
        total_pages: response.data.total_pages
      };
    } catch (error) {
      // Fallback to local grants data when backend is unavailable
      console.warn('Backend unavailable, using fallback grants data:', error);
      
      try {
        const fallbackResponse = await fetch('/grants.json');
        const fallbackData = await fallbackResponse.json();
        
        // Apply basic filtering to fallback data
        let filteredGrants = fallbackData.grants;
        
        if (filters.search) {
          const searchTerm = filters.search.toLowerCase();
          filteredGrants = filteredGrants.filter((grant: any) => 
            grant.title.toLowerCase().includes(searchTerm) ||
            grant.description.toLowerCase().includes(searchTerm) ||
            grant.synopsis?.toLowerCase().includes(searchTerm)
          );
        }
        
        if (filters.program) {
          filteredGrants = filteredGrants.filter((grant: any) => 
            grant.program.toLowerCase().includes(filters.program!.toLowerCase())
          );
        }
        
        if (filters.min_amount) {
          filteredGrants = filteredGrants.filter((grant: any) => 
            (grant.min_funding_amount || 0) >= filters.min_amount!
          );
        }
        
        if (filters.max_amount) {
          filteredGrants = filteredGrants.filter((grant: any) => 
            (grant.max_funding_amount || Infinity) <= filters.max_amount!
          );
        }
        
        if (filters.technology_areas && filters.technology_areas.length > 0) {
          filteredGrants = filteredGrants.filter((grant: any) => 
            filters.technology_areas!.some(area => 
              grant.technology_areas.some((grantArea: string) => 
                grantArea.toLowerCase().includes(area.toLowerCase())
              )
            )
          );
        }
        
        // Apply pagination
        const startIndex = (page - 1) * perPage;
        const endIndex = startIndex + perPage;
        const paginatedGrants = filteredGrants.slice(startIndex, endIndex);
        const totalPages = Math.ceil(filteredGrants.length / perPage);
        
        return {
          data: paginatedGrants,
          total: filteredGrants.length,
          page: page,
          per_page: perPage,
          total_pages: totalPages
        };
      } catch (fallbackError) {
        console.error('Fallback data also failed:', fallbackError);
        throw new Error('Both backend and fallback data are unavailable');
      }
    }
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
