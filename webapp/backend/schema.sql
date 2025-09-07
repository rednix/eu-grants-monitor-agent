-- EU Grants Monitor Database Schema
-- Execute this in your Supabase SQL Editor to create all tables
-- Dashboard: https://iabempablugdcjhrylkv.supabase.co -> SQL Editor

-- Create custom enum types
CREATE TYPE userrole AS ENUM ('user', 'company_admin', 'system_admin');
CREATE TYPE subscriptionstatus AS ENUM ('free', 'monthly', 'yearly', 'pay_per_use', 'cancelled');
CREATE TYPE companysize AS ENUM ('micro', 'small', 'medium', 'large');
CREATE TYPE grantstatus AS ENUM ('open', 'closed', 'upcoming', 'cancelled');
CREATE TYPE applicationstatus AS ENUM ('draft', 'in_progress', 'review', 'submitted', 'accepted', 'rejected', 'withdrawn');

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    profile_picture_url VARCHAR(500),
    google_id VARCHAR(255) UNIQUE,
    microsoft_id VARCHAR(255) UNIQUE,
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    role userrole DEFAULT 'user',
    subscription_status subscriptionstatus DEFAULT 'free',
    subscription_start_date TIMESTAMPTZ,
    subscription_end_date TIMESTAMPTZ,
    stripe_customer_id VARCHAR(255) UNIQUE,
    ai_assistant_credits INTEGER DEFAULT 0,
    ai_assistant_usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    last_login TIMESTAMPTZ,
    company_id INTEGER
);

-- Create indexes for users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_google_id ON users(google_id);
CREATE INDEX idx_users_microsoft_id ON users(microsoft_id);

-- Create companies table
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    website VARCHAR(255),
    size companysize NOT NULL,
    industry VARCHAR(100),
    country VARCHAR(2) NOT NULL, -- ISO country code
    city VARCHAR(100),
    address TEXT,
    vat_number VARCHAR(50),
    registration_number VARCHAR(50),
    ai_expertise JSONB DEFAULT '[]'::jsonb,
    technology_focus JSONB DEFAULT '[]'::jsonb,
    annual_revenue INTEGER,
    funding_history JSONB DEFAULT '[]'::jsonb,
    preferred_funding_min INTEGER DEFAULT 50000,
    preferred_funding_max INTEGER DEFAULT 500000,
    max_project_duration_months INTEGER DEFAULT 24,
    profile_completed BOOLEAN DEFAULT false,
    profile_completion_percentage FLOAT DEFAULT 0.0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Create indexes for companies
CREATE INDEX idx_companies_name ON companies(name);
CREATE INDEX idx_companies_country ON companies(country);
CREATE INDEX idx_companies_size ON companies(size);

-- Create grants table
CREATE TABLE grants (
    id SERIAL PRIMARY KEY,
    grant_id VARCHAR(255) NOT NULL UNIQUE,
    title VARCHAR(500) NOT NULL,
    program VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    synopsis TEXT,
    objectives TEXT,
    total_budget INTEGER NOT NULL,
    funding_rate FLOAT DEFAULT 70.0,
    min_funding_amount INTEGER,
    max_funding_amount INTEGER,
    publication_date TIMESTAMPTZ,
    deadline TIMESTAMPTZ NOT NULL,
    project_start_date TIMESTAMPTZ,
    project_end_date TIMESTAMPTZ,
    project_duration_months INTEGER,
    eligible_countries JSONB DEFAULT '[]'::jsonb,
    target_organizations JSONB DEFAULT '[]'::jsonb,
    eligible_activities JSONB DEFAULT '[]'::jsonb,
    keywords JSONB DEFAULT '[]'::jsonb,
    topics JSONB DEFAULT '[]'::jsonb,
    technology_areas JSONB DEFAULT '[]'::jsonb,
    industry_sectors JSONB DEFAULT '[]'::jsonb,
    url VARCHAR(500),
    documents_url VARCHAR(500),
    submission_url VARCHAR(500),
    status grantstatus DEFAULT 'open',
    complexity_score FLOAT,
    ai_relevance_keywords JSONB DEFAULT '[]'::jsonb,
    estimated_success_rate FLOAT,
    source_system VARCHAR(100),
    source_url VARCHAR(500),
    last_updated TIMESTAMPTZ DEFAULT NOW(),
    search_vector TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Create indexes for grants
CREATE INDEX idx_grants_grant_id ON grants(grant_id);
CREATE INDEX idx_grants_program ON grants(program);
CREATE INDEX idx_grants_deadline ON grants(deadline);
CREATE INDEX idx_grants_status ON grants(status);
CREATE INDEX idx_grants_title ON grants USING gin(to_tsvector('english', title));
CREATE INDEX idx_grants_description ON grants USING gin(to_tsvector('english', description));
CREATE INDEX idx_grants_keywords ON grants USING gin(keywords);
CREATE INDEX idx_grants_technology_areas ON grants USING gin(technology_areas);

-- Create applications table
CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    grant_id INTEGER NOT NULL,
    project_title VARCHAR(500),
    project_summary TEXT,
    requested_amount INTEGER,
    project_duration_months INTEGER,
    status applicationstatus DEFAULT 'draft',
    submitted_at TIMESTAMPTZ,
    ai_assistant_used BOOLEAN DEFAULT false,
    ai_assistant_session_id VARCHAR(255),
    form_completion_percentage FLOAT DEFAULT 0.0,
    form_data JSONB DEFAULT '{}'::jsonb,
    generated_documents JSONB DEFAULT '[]'::jsonb,
    external_reference VARCHAR(255),
    submission_confirmation VARCHAR(255),
    evaluation_score FLOAT,
    feedback_received TEXT,
    outcome_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    
    -- Unique constraint to prevent duplicate applications
    CONSTRAINT unique_company_grant_application UNIQUE (company_id, grant_id)
);

-- Create indexes for applications
CREATE INDEX idx_applications_user_id ON applications(user_id);
CREATE INDEX idx_applications_company_id ON applications(company_id);
CREATE INDEX idx_applications_grant_id ON applications(grant_id);
CREATE INDEX idx_applications_status ON applications(status);

-- Create payment_transactions table
CREATE TABLE payment_transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    stripe_payment_intent_id VARCHAR(255) NOT NULL UNIQUE,
    stripe_session_id VARCHAR(255) UNIQUE,
    amount INTEGER NOT NULL, -- in cents
    currency VARCHAR(3) DEFAULT 'EUR',
    description VARCHAR(500),
    status VARCHAR(50) DEFAULT 'pending',
    product_type VARCHAR(50),
    credits_added INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Create indexes for payment_transactions
CREATE INDEX idx_payment_transactions_user_id ON payment_transactions(user_id);
CREATE INDEX idx_payment_transactions_status ON payment_transactions(status);

-- Add foreign key constraints
ALTER TABLE users ADD CONSTRAINT fk_users_company FOREIGN KEY (company_id) REFERENCES companies(id);
ALTER TABLE applications ADD CONSTRAINT fk_applications_user FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE applications ADD CONSTRAINT fk_applications_company FOREIGN KEY (company_id) REFERENCES companies(id);
ALTER TABLE applications ADD CONSTRAINT fk_applications_grant FOREIGN KEY (grant_id) REFERENCES grants(id);
ALTER TABLE payment_transactions ADD CONSTRAINT fk_payment_transactions_user FOREIGN KEY (user_id) REFERENCES users(id);

-- Enable Row Level Security (RLS) for security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE payment_transactions ENABLE ROW LEVEL SECURITY;

-- Create RLS policies

-- Users can see and modify their own data
CREATE POLICY users_own_data ON users
    FOR ALL USING (auth.uid()::text = id::text);

-- Companies can be seen by their members
CREATE POLICY company_members ON companies
    FOR ALL USING (
        id IN (
            SELECT company_id FROM users 
            WHERE auth.uid()::text = users.id::text 
            AND company_id IS NOT NULL
        )
    );

-- Grants are publicly readable
CREATE POLICY grants_public_read ON grants
    FOR SELECT USING (true);

-- Applications are private to users and their company
CREATE POLICY applications_own_company ON applications
    FOR ALL USING (
        user_id IN (
            SELECT id FROM users 
            WHERE auth.uid()::text = users.id::text
        )
        OR
        company_id IN (
            SELECT company_id FROM users 
            WHERE auth.uid()::text = users.id::text 
            AND company_id IS NOT NULL
        )
    );

-- Payment transactions are private to the user
CREATE POLICY payment_transactions_own ON payment_transactions
    FOR ALL USING (
        user_id IN (
            SELECT id FROM users 
            WHERE auth.uid()::text = users.id::text
        )
    );

-- Insert sample grant data
INSERT INTO grants (
    grant_id, title, program, description, synopsis, total_budget, 
    min_funding_amount, max_funding_amount, deadline, project_start_date, 
    project_end_date, project_duration_months, eligible_countries, 
    target_organizations, keywords, technology_areas, industry_sectors,
    url, status, source_system, complexity_score
) VALUES 
(
    'HE-2024-AI-001',
    'AI for Healthcare SMEs',
    'Horizon Europe',
    'This call supports Small and Medium Enterprises (SMEs) in developing artificial intelligence solutions for healthcare applications. Focus areas include machine learning for medical diagnosis, natural language processing for clinical documentation, and computer vision for medical imaging.',
    'AI solutions for healthcare: ML diagnosis, NLP clinical docs, CV medical imaging',
    10000000,
    50000,
    500000,
    NOW() + INTERVAL '45 days',
    NOW() + INTERVAL '120 days',
    NOW() + INTERVAL '850 days',
    24,
    '["DE", "FR", "IT", "ES", "NL", "BE", "AT", "SE", "DK", "FI"]'::jsonb,
    '["SME", "Small Enterprise", "Medium Enterprise"]'::jsonb,
    '["artificial intelligence", "healthcare", "machine learning", "medical diagnosis", "clinical validation"]'::jsonb,
    '["AI", "Healthcare", "Machine Learning"]'::jsonb,
    '["Healthcare", "Technology"]'::jsonb,
    'https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/HORIZON-EIC-2024-PATHFINDEROPEN-01',
    'open',
    'horizon_europe',
    65.0
),
(
    'DIGITAL-EU-2024-002',
    'Digital Innovation for Manufacturing SMEs',
    'Digital Europe',
    'Supporting digital transformation in European manufacturing through Industry 4.0 technologies. This call targets SMEs developing solutions in areas such as IoT integration, predictive maintenance using AI, automated quality control, and supply chain optimization.',
    'Industry 4.0: IoT, AI predictive maintenance, automated quality control',
    5000000,
    75000,
    300000,
    NOW() + INTERVAL '60 days',
    NOW() + INTERVAL '90 days',
    NOW() + INTERVAL '630 days',
    18,
    '["DE", "FR", "IT", "ES", "PL", "CZ", "HU", "SK"]'::jsonb,
    '["SME", "Manufacturing Company", "Technology Provider"]'::jsonb,
    '["digital transformation", "industry 40", "iot", "predictive maintenance", "automation"]'::jsonb,
    '["IoT", "AI", "Manufacturing"]'::jsonb,
    '["Manufacturing", "Technology"]'::jsonb,
    'https://digital-strategy.ec.europa.eu/en/activities/digital-programme',
    'open',
    'digital_europe',
    55.0
),
(
    'LIFE-2024-GREEN-004',
    'AI-Powered Environmental Monitoring Solutions',
    'Life',
    'Developing AI solutions for environmental monitoring and protection. Focus on satellite data analysis, IoT sensor networks, predictive environmental modeling, and automated reporting systems for environmental compliance.',
    'Green AI: Satellite analysis, IoT sensors, environmental modeling',
    3000000,
    100000,
    400000,
    NOW() + INTERVAL '75 days',
    NOW() + INTERVAL '150 days',
    NOW() + INTERVAL '870 days',
    24,
    '["DE", "FR", "IT", "ES", "NL", "BE", "AT", "SE", "DK", "FI", "PT", "GR"]'::jsonb,
    '["SME", "Environmental Company", "Technology Provider"]'::jsonb,
    '["environmental monitoring", "ai", "satellite data", "iot", "sustainability"]'::jsonb,
    '["AI", "Environmental", "Satellite"]'::jsonb,
    '["Environment", "Technology", "Sustainability"]'::jsonb,
    'https://ec.europa.eu/environment/life/',
    'open',
    'life_programme',
    70.0
),
(
    'EIC-2024-ACCELERATOR-003',
    'Deep Tech AI Startups Accelerator',
    'EIC Accelerator',
    'Supporting deep tech startups leveraging AI for breakthrough innovations. Focus on companies developing novel AI applications in robotics, autonomous systems, advanced materials, and quantum computing applications.',
    'Deep tech AI: robotics, autonomous systems, quantum computing',
    15000000,
    500000,
    2500000,
    NOW() + INTERVAL '90 days',
    NOW() + INTERVAL '180 days',
    NOW() + INTERVAL '1275 days',
    36,
    '["ALL_EU"]'::jsonb,
    '["SME", "Startup", "Deep Tech Company"]'::jsonb,
    '["deep tech", "ai", "robotics", "autonomous systems", "quantum computing", "breakthrough innovation"]'::jsonb,
    '["AI", "Robotics", "Quantum", "Deep Tech"]'::jsonb,
    '["Technology", "Research", "Innovation"]'::jsonb,
    'https://eic.ec.europa.eu/eic-funding-opportunities/eic-accelerator_en',
    'open',
    'eic_accelerator',
    85.0
),
(
    'EUREKA-2024-AI-005',
    'AI for Sustainable Energy Solutions',
    'Eureka',
    'International collaboration program supporting AI applications in renewable energy, smart grids, energy efficiency optimization, and sustainable energy storage solutions for SMEs across Europe.',
    'Sustainable AI: renewable energy, smart grids, energy efficiency',
    8000000,
    200000,
    800000,
    NOW() + INTERVAL '120 days',
    NOW() + INTERVAL '210 days',
    NOW() + INTERVAL '1122 days',
    30,
    '["DE", "FR", "IT", "ES", "NL", "BE", "AT", "SE", "DK", "FI", "NO", "CH"]'::jsonb,
    '["SME", "Energy Company", "Technology Provider", "Research Institute"]'::jsonb,
    '["sustainable energy", "ai", "renewable energy", "smart grids", "energy efficiency"]'::jsonb,
    '["AI", "Energy", "Sustainability"]'::jsonb,
    '["Energy", "Technology", "Sustainability"]'::jsonb,
    'https://www.eurekanetwork.org/',
    'open',
    'eureka',
    75.0
);

-- Grant success message
SELECT 
    'Database schema created successfully!' as message,
    COUNT(*) as grants_created 
FROM grants;
