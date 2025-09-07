# Project Structure

This document describes the organization and structure of the EU Grants Monitor Agent project.

## 🏗 Directory Structure

```
eu-grants-monitor-agent/
├── README.md                           # Main project documentation
├── WARP.md                             # WARP AI assistant guidance  
├── pyproject.toml                      # Python project configuration
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git ignore rules
│
├── config/                             # Configuration files
│   ├── config.template.yaml            # Main configuration template
│   ├── business_profile.template.yaml  # Business profile template
│   ├── masumi_config.template.yaml     # Masumi integration template
│   ├── config.yaml                     # Main configuration (gitignored)
│   ├── business_profile.yaml           # Business profile (gitignored)
│   └── masumi_config.yaml              # Masumi configuration (gitignored)
│
├── docs/                               # Documentation
│   ├── MASUMI_INTEGRATION.md           # Masumi integration guide
│   └── PROJECT_STRUCTURE.md            # This file
│
├── scripts/                            # Utility scripts
│   └── register_masumi_agent.py        # Masumi registration script
│
├── data/                               # Data files
│   └── guidance_*.json                 # Example guidance files
│
└── src/                                # Source code
    └── grants_monitor/                 # Main package
        ├── __init__.py                 # Package initialization
        ├── __main__.py                 # CLI entry point
        ├── main.py                     # Main agent class and CLI
        ├── api.py                      # FastAPI endpoints
        ├── masumi_agent.py             # Masumi integration
        │
        ├── analyzers/                  # Grant analysis components
        │   ├── __init__.py
        │   └── opportunity_analyzer.py
        │
        ├── assistants/                 # Application assistance
        │   ├── __init__.py
        │   └── application_assistant.py
        │
        ├── data/                       # Data models and mock data
        │   ├── __init__.py
        │   ├── models.py               # Pydantic data models
        │   └── mock_grants.py          # Test data
        │
        ├── matchers/                   # Profile matching logic
        │   ├── __init__.py
        │   └── profile_matcher.py
        │
        ├── notifiers/                  # Alert and notification systems
        │   ├── __init__.py
        │   └── email_notifier.py
        │
        ├── scrapers/                   # Web scrapers
        │   ├── __init__.py
        │   └── horizon_scraper.py
        │
        ├── services/                   # Core services
        │   ├── __init__.py
        │   ├── document_analyzer.py    # Document analysis service
        │   ├── document_generator.py   # Document generation service
        │   ├── form_prefiller.py       # Form pre-filling service
        │   ├── user_prompter.py        # Interactive user prompts
        │   └── web_researcher.py       # Web research service
        │
        └── utils/                      # Utilities and helpers
            ├── __init__.py
            ├── config.py               # Configuration management
            └── logger.py               # Logging setup
```

## 📦 Package Organization

### Core Components

- **`main.py`**: Primary agent class and CLI interface
- **`api.py`**: FastAPI endpoints for Masumi integration
- **`masumi_agent.py`**: Masumi framework integration wrapper

### Functional Modules

#### Analyzers (`analyzers/`)
- Grant opportunity analysis
- Complexity assessment
- Relevance scoring

#### Assistants (`assistants/`)
- Application guidance generation
- Complete application workflow orchestration

#### Data (`data/`)
- Pydantic models for all data structures
- Mock data for development and testing

#### Matchers (`matchers/`)
- Business profile matching algorithms
- Scoring and ranking logic

#### Notifiers (`notifiers/`)
- Email notification system
- Extensible for Slack, Discord, etc.

#### Scrapers (`scrapers/`)
- Web scraping for EU funding portals
- Currently supports Horizon Europe
- Extensible for additional sources

#### Services (`services/`)
- **Document Analyzer**: PDF/webpage analysis
- **Document Generator**: Application form generation  
- **Form Prefiller**: Intelligent form pre-filling
- **User Prompter**: Interactive data collection
- **Web Researcher**: Company information gathering

#### Utils (`utils/`)
- Configuration management
- Logging setup and utilities

## 🔧 Configuration System

### Template Files
All configuration uses template files that users copy and customize:

- `config.template.yaml` → `config.yaml`
- `business_profile.template.yaml` → `business_profile.yaml`  
- `masumi_config.template.yaml` → `masumi_config.yaml`

### Configuration Hierarchy

1. **Main Configuration** (`config.yaml`)
   - Scraper settings
   - Analysis parameters
   - Notification preferences
   - Database settings

2. **Business Profile** (`business_profile.yaml`)
   - Company information
   - AI expertise areas
   - Industry preferences
   - Funding requirements

3. **Masumi Configuration** (`masumi_config.yaml`)
   - Payment API keys
   - Agent registration details
   - Pricing configuration
   - Legal information

## 🚀 Entry Points

### CLI Commands
- `python -m grants_monitor` - Main CLI interface
- Available commands: `list`, `show`, `assist`, `generate`, `run`, `serve-api`, `register-masumi`

### API Server
- `python -m grants_monitor serve-api` - Start FastAPI server
- Endpoints available at `/docs` for interactive documentation

### Scripts
- `scripts/register_masumi_agent.py` - Direct registration with Masumi

## 📊 Data Flow

### Monitoring Workflow
1. **Scrapers** → Extract opportunities from EU portals
2. **Analyzers** → Assess complexity and relevance  
3. **Matchers** → Score against business profile
4. **Notifiers** → Send alerts for high-priority matches

### Application Assistance Workflow
1. **Document Analyzer** → Download and parse grant documents
2. **Web Researcher** → Gather company information
3. **Form Prefiller** → Pre-fill application forms
4. **User Prompter** → Collect missing information
5. **Document Generator** → Generate final application package

### Masumi Integration Workflow  
1. **API Endpoints** → Receive paid requests
2. **Core Services** → Process requests using full capabilities
3. **Response Delivery** → Return structured results

## 🧪 Development Guidelines

### Adding New Components

#### New Scraper
1. Create file in `scrapers/` directory
2. Inherit from base scraper interface  
3. Register in `main.py` `_init_scrapers()` method
4. Add configuration in `config.template.yaml`

#### New Service
1. Create file in `services/` directory
2. Follow existing patterns for async operations
3. Add to `application_assistant.py` if part of main workflow
4. Update API endpoints in `api.py` if needed

#### New Notifier
1. Create file in `notifiers/` directory
2. Implement common notification interface
3. Add configuration options
4. Register in main agent initialization

### Testing
- Import tests: `python -c "import src.grants_monitor.main"`
- CLI tests: `python -m grants_monitor --help`
- API tests: Start server and check `/health` endpoint
- Configuration validation: YAML syntax checking

### Code Style
- Follow existing import organization
- Use type hints throughout
- Implement proper error handling with logging
- Document all public methods and classes

## 🔒 Security Considerations

### Configuration Security
- All sensitive configuration is gitignored
- Template files provide safe defaults
- Environment variable support for production

### API Security  
- Input validation with Pydantic models
- Error handling prevents information leakage
- CORS configuration for production use

### Data Privacy
- No permanent storage of sensitive user data
- Business profiles used only for request processing
- Compliance with EU data protection regulations

## 📈 Extensibility

The project is designed for easy extension:

- **New EU Programs**: Add scrapers for additional funding sources
- **New Analysis Methods**: Extend analyzers with additional scoring algorithms  
- **New Output Formats**: Add document generators for different formats
- **New Notification Channels**: Implement additional notifiers
- **New Payment Systems**: Extend beyond Masumi integration

Each component follows clear interfaces and patterns, making the system highly modular and maintainable.
