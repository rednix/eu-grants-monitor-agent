export interface Grant {
  id: string;
  grant_id: string;
  title: string;
  program: string;
  description: string;
  synopsis: string;
  total_budget: number;
  min_funding_amount: number;
  max_funding_amount: number;
  deadline: string;
  project_start_date: string;
  project_end_date: string;
  project_duration_months: number;
  eligible_countries: string[];
  target_organizations: string[];
  keywords: string[];
  technology_areas: string[];
  industry_sectors: string[];
  url: string;
  documents_url?: string;
  status: 'open' | 'closed' | 'draft';
  source_system: string;
  complexity_score: number;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  profile_image_url?: string;
  subscription_status: 'free' | 'ai_assistant_monthly' | 'ai_assistant_yearly';
  subscription_expires_at?: string;
  oauth_provider: 'google' | 'microsoft';
  oauth_provider_id: string;
  company_id?: string;
  company?: Company;
  created_at: string;
  updated_at: string;
}

export interface Company {
  id: string;
  name: string;
  description?: string;
  website?: string;
  size: 'micro' | 'small' | 'medium' | 'large';
  industry_sectors: string[];
  technology_areas: string[];
  eligible_countries: string[];
  funding_preferences: {
    min_amount?: number;
    max_amount?: number;
    preferred_programs: string[];
    max_complexity_score?: number;
  };
  created_at: string;
  updated_at: string;
}

export interface Application {
  id: string;
  user_id: string;
  grant_id: string;
  grant: Grant;
  status: 'draft' | 'in_progress' | 'submitted' | 'approved' | 'rejected';
  ai_assistance_used: boolean;
  application_data: Record<string, any>;
  notes?: string;
  submitted_at?: string;
  created_at: string;
  updated_at: string;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  loading: boolean;
}

export interface GrantFilters {
  search?: string;
  program?: string;
  min_amount?: number;
  max_amount?: number;
  deadline_from?: string;
  deadline_to?: string;
  countries?: string[];
  technology_areas?: string[];
  industry_sectors?: string[];
  max_complexity?: number;
  status?: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}
