# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is an intelligent agent built on the Masumi framework that monitors EU grants and tender opportunities specifically for Small and Medium Enterprises (SMEs), with a focus on AI-related business opportunities. The agent automatically scans, filters, and alerts on relevant EU funding opportunities that match configured business profiles.

The project consists of two main components:
1. **Core Agent** (`src/grants_monitor/`): Python-based monitoring agent with CLI and API interfaces
2. **Web Platform** (`webapp/`): Full-stack web application with React frontend and FastAPI backend

## Common Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"
```

### Configuration Setup
```bash
# Copy and customize configuration templates
cp config/config.template.yaml config/config.yaml
cp config/business_profile.template.yaml config/business_profile.yaml

# Initialize the agent configuration
python -m grants_monitor setup
```

### Running the Application
```bash
# Run a single monitoring cycle
python -m grants_monitor run

# Run continuously with scheduled intervals
python -m grants_monitor run --continuous

# List available opportunities with filters
python -m grants_monitor list --filter ai --complexity simple --amount 50000-500000

# Generate application assistance for a grant
python -m grants_monitor assist HE-2024-AI-001
```

### Development and Testing
```bash
# Run tests (when test suite is implemented)
pytest tests/
pytest --cov=grants_monitor tests/

# Code formatting and linting
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/

# Run pre-commit hooks
pre-commit run --all-files
```

### Package Management
```bash
# Build the package
python -m build

# Install in development mode
pip install -e .
```

### Web Platform Development

#### Backend Setup (FastAPI)
```bash
# Navigate to webapp backend
cd webapp/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Start development server
uvicorn app.main:app --reload --port 8000

# API documentation available at http://localhost:8000/docs
```

#### Frontend Setup (Next.js + React)
```bash
# Navigate to webapp frontend
cd webapp/frontend

# Install dependencies
npm install

# Set up environment
cp .env.local.example .env.local
# Edit .env.local with API endpoints

# Start development server
npm run dev

# Production build
npm run build
npm start

# Type checking
npm run type-check

# Linting
npm run lint
```

## Code Architecture

### Overall System Architecture

The EU Grants Monitor consists of two main applications that work together:

#### 1. Core Agent (Python/CLI)
The monitoring and analysis engine that can run standalone or serve API endpoints.

#### 2. Web Platform (Full-Stack)
User-facing web application providing UI for grant discovery and AI-assisted applications.

### Core Agent Architecture

The core agent follows a modular architecture with clear separation of concerns:

1. **Agent Core (`main.py`)**: The `GrantsMonitorAgent` class orchestrates the entire monitoring workflow, managing scrapers, analyzers, matchers, and notifiers. Entry points:
   - CLI interface via `python -m grants_monitor`
   - API server via `uvicorn app.main:app`

2. **Data Layer (`data/models.py`)**: Comprehensive Pydantic models define the data structures:
   - `Grant`: Core grant opportunity model with financial, timing, eligibility, and scoring fields
   - `BusinessProfile`: Company profile for matching (expertise, industries, funding preferences)
   - `Application`: Tracks application status and outcomes
   - `Alert`: Notification model for high-priority opportunities

3. **Scrapers (`scrapers/`)**: Web scraping modules for different EU funding portals
   - Currently implements Horizon Europe scraper
   - Designed for easy extension to additional funding sources (Digital Europe, ERDF, etc.)

4. **Analysis Pipeline**: Two-stage analysis system:
   - **Analyzers (`analyzers/`)**: AI-powered opportunity analysis (complexity assessment, ROI analysis)
   - **Matchers (`matchers/`)**: Business profile matching logic with weighted scoring

5. **Services (`services/`)**: Core application services:
   - **Document Analyzer**: PDF/webpage analysis and parsing
   - **Document Generator**: Application form generation and completion
   - **Form Prefiller**: Intelligent form pre-filling with company data
   - **User Prompter**: Interactive data collection workflows
   - **Web Researcher**: Company information gathering and validation

6. **Notification System (`notifiers/`)**: Multi-channel alert system supporting email, Slack, and Discord integrations

7. **Configuration Management (`utils/config.py`)**: YAML-based configuration with template system and default value handling

### Web Platform Architecture

#### Frontend (Next.js + TypeScript)
- **Framework**: Next.js 14 with React 18 and TypeScript
- **Styling**: Tailwind CSS with Headless UI components
- **State Management**: React Query for server state, React Context for client state
- **Authentication**: OAuth integration (Google/Microsoft) via backend APIs
- **Payment Processing**: Stripe integration for subscription management
- **Type Safety**: Full TypeScript implementation with strict mode

#### Backend (FastAPI + PostgreSQL)
- **Framework**: FastAPI with async/await support
- **Database**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **Authentication**: JWT tokens with OAuth provider integration
- **Payment Processing**: Stripe webhooks and subscription management
- **AI Integration**: HTTP client connecting to core agent API endpoints
- **Real-time Features**: Background task processing for data synchronization

### Key Architectural Patterns

- **Async/Await Pattern**: The agent uses async programming for concurrent scraping and API calls
- **Plugin Architecture**: Scrapers and notifiers are designed as pluggable components
- **Scoring System**: Multi-weighted scoring algorithm combining relevance, complexity, amount, and deadline factors
- **Template-Based Config**: Separate template files ensure easy setup while keeping sensitive data secure

### Data Flow

1. **Monitoring Cycle**: `run_monitoring_cycle()` orchestrates: scan → analyze → alert → store
2. **Scoring Pipeline**: Grants flow through relevance calculation → complexity assessment → priority scoring
3. **Alert System**: High-priority grants (configurable threshold) trigger immediate notifications

### Extension Points

- **New Scrapers**: Add to `scrapers/` directory and register in `_init_scrapers()`
- **Analysis Algorithms**: Extend `OpportunityAnalyzer` for additional scoring criteria
- **Notification Channels**: Add new notifiers following the email notifier pattern
- **Data Sources**: The system is designed to handle multiple EU funding portals

## Configuration System

### Main Configuration (`config/config.yaml`)
- Scraper settings (rate limits, enabled sources)
- Analysis parameters (keyword weights, matching criteria)
- Scoring weights and alert thresholds
- Notification channels and database settings

### Business Profile (`config/business_profile.yaml`)
- Company information and size classification
- AI expertise and technology focus areas
- Target industries and business sectors
- Funding preferences and complexity tolerance
- Geographic and keyword preferences

## Technology Stack

- **Framework**: Masumi agent framework
- **Language**: Python 3.9+
- **Data Processing**: pandas, numpy, pydantic
- **Web Scraping**: BeautifulSoup, Scrapy, aiohttp
- **Database**: SQLite (dev), PostgreSQL (prod) with SQLAlchemy/Alembic
- **Scheduling**: APScheduler for automated monitoring
- **CLI**: Click framework with Rich for formatting
- **Logging**: Loguru for structured logging

## Development Guidelines

### Module Import Structure
The codebase uses relative imports within the package. When adding new modules, follow the existing pattern of importing from utils, data, and component directories.

### Async Programming
Most core operations are async. New scrapers and analyzers should follow the async pattern for consistency and performance.

### Configuration Management
All configurable parameters should be externalized to YAML files. Use the ConfigManager for accessing settings and provide sensible defaults.

### Error Handling
The system includes comprehensive error handling with logging. Failed scrapers don't break the entire monitoring cycle.

### Data Validation
All data models use Pydantic for validation. New models should include proper field validation and type hints.

## Development Workflows

### Working with Both Applications

The project contains two applications that can be developed independently or together:

1. **Core Agent Development**: Work in the root directory and `src/grants_monitor/`
2. **Web Platform Development**: Work in the `webapp/` directory
3. **Integrated Development**: Run both applications simultaneously for full-stack development

### Integrated Development Setup

```bash
# Terminal 1: Core Agent API
python -m grants_monitor serve-api --port 8001

# Terminal 2: Web Platform Backend
cd webapp/backend
uvicorn app.main:app --reload --port 8000

# Terminal 3: Web Platform Frontend  
cd webapp/frontend
npm run dev

# Now you can:
# - Access web UI at http://localhost:3000
# - Access web API at http://localhost:8000/docs
# - Access core agent API at http://localhost:8001/docs
```

### Database Development

#### Core Agent (SQLite/PostgreSQL)
```bash
# Using in-memory storage (default for development)
python -m grants_monitor run

# Database migrations (when implemented)
alembic upgrade head
alembic revision --autogenerate -m "Description"
```

#### Web Platform (PostgreSQL/Supabase)
```bash
# Database setup with Supabase
cd webapp/backend
python setup_supabase.py

# Test connection
python test_connection.py

# Initialize database
python initialize_db.py
```

### Testing Strategy

#### Core Agent Testing
```bash
# Run all tests
pytest tests/ -v

# Test with coverage
pytest --cov=grants_monitor tests/

# Test specific components
pytest tests/test_scrapers.py -v
pytest tests/test_analyzers.py -v
```

#### Web Platform Testing
```bash
# Backend tests
cd webapp/backend
pytest tests/ -v

# Frontend tests
cd webapp/frontend
npm test
npm run test:e2e  # End-to-end tests (when implemented)
```

### Deployment Workflow

#### Development Deployment
```bash
# Quick local deployment
cd webapp
# Follow webapp/DEPLOYMENT.md for Railway + Vercel setup
```

#### Production Deployment
```bash
# Core agent as service
python -m grants_monitor serve-api --host 0.0.0.0 --port 8000

# Web platform (see webapp/DEPLOYMENT.md)
# Backend: Deploy to Railway/Heroku/DigitalOcean
# Frontend: Deploy to Vercel/Netlify
```

## Project Structure

```
eu-grants-monitor-agent/
├── README.md                           # Main project documentation
├── WARP.md                             # This file
├── pyproject.toml                      # Python project configuration
├── requirements.txt                    # Python dependencies
├── config/                             # Configuration templates
│   ├── config.template.yaml
│   ├── business_profile.template.yaml
│   └── masumi_config.template.yaml
├── docs/                               # Additional documentation
│   ├── PROJECT_STRUCTURE.md
│   └── MASUMI_INTEGRATION.md
├── scripts/                            # Utility scripts
│   └── register_masumi_agent.py
├── data/                               # Sample data files
│   └── guidance_*.json
├── src/grants_monitor/                 # Core agent package
│   ├── main.py                         # Main agent and CLI entry point
│   ├── api.py                          # FastAPI endpoints
│   ├── masumi_agent.py                 # Masumi integration
│   ├── data/
│   │   └── models.py                   # Pydantic data models
│   ├── scrapers/                       # Web scrapers for EU funding portals
│   ├── analyzers/                      # AI-powered opportunity analysis
│   ├── matchers/                       # Business profile matching logic
│   ├── assistants/                     # Application assistance workflows
│   ├── services/                       # Core application services
│   ├── notifiers/                      # Alert and notification systems
│   └── utils/                          # Configuration and logging utilities
└── webapp/                             # Full-stack web application
    ├── README.md                       # Web platform documentation
    ├── DEPLOYMENT.md                   # Deployment guide
    ├── backend/                        # FastAPI backend
    │   ├── app/
    │   │   ├── main.py                 # FastAPI application
    │   │   ├── models.py               # Database models
    │   │   ├── auth/                   # Authentication logic
    │   │   ├── api/                    # API route handlers
    │   │   └── services/               # Business logic services
    │   ├── requirements.txt
    │   └── .env.example
    └── frontend/                       # Next.js frontend
        ├── package.json
        ├── next.config.js
        ├── tailwind.config.js
        ├── pages/                      # Next.js pages
        ├── components/                 # React components
        ├── hooks/                      # Custom React hooks
        ├── services/                   # API client services
        ├── styles/                     # CSS and styling
        └── .env.local.example
```

The architecture supports the full grant monitoring lifecycle from discovery to application tracking, with both programmatic (CLI/API) and web-based user interfaces, focusing on SME-friendly opportunities in the AI space.
