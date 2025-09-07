# EU Grants Monitor Agent

An intelligent agent built on Masumi that monitors EU grants and tender opportunities specifically for Small and Medium Enterprises (SMEs), with a focus on AI-related business opportunities for small consultancies.

## 🎯 Project Overview

This agent automatically scans, filters, and alerts on relevant EU funding opportunities that match your business profile and capabilities. It's designed to help small AI consultancies identify and apply for grants and tenders that offer the best chances of success with minimal application complexity.

## 🚀 Key Features

- **Automated Monitoring**: Continuously scans EU funding databases and portals
- **Smart Filtering**: Uses AI to identify opportunities most suitable for SMEs
- **Business Profile Matching**: Matches opportunities to your specific consultancy capabilities
- **Complexity Assessment**: Prioritizes grants with simpler application processes
- **Real-time Alerts**: Notifies you of new opportunities and upcoming deadlines
- **Complete Application Generation**: End-to-end document generation with interactive assistance
- **Masumi Integration**: Decentralized AI agent accessible via Cardano blockchain payments
- **API Services**: FastAPI endpoints for programmatic access to all capabilities

## 📊 Data Sources

The agent monitors various EU funding sources including:

- Horizon Europe
- Digital Europe Programme
- European Regional Development Fund (ERDF)
- Erasmus+ (for training and education projects)
- COSME Programme
- EU Innovation Fund
- European Social Fund Plus (ESF+)
- Life Programme (for environmental projects)
- Connecting Europe Facility (CEF)

## 🛠 Technology Stack

- **Framework**: Masumi agent framework
- **Language**: Python 3.9+
- **Data Processing**: pandas, numpy
- **Web Scraping**: BeautifulSoup, Scrapy
- **API Integration**: requests, aiohttp
- **Database**: SQLite (for local development), PostgreSQL (for production)
- **Monitoring**: APScheduler for task scheduling
- **Notifications**: Email, Slack, Discord integrations

## 🏗 Project Structure

```
eu-grants-monitor-agent/
├── src/
│   └── grants_monitor/
│       ├── __init__.py
│       ├── main.py              # Main agent entry point
│       ├── scrapers/            # Web scrapers for different EU portals
│       ├── analyzers/           # AI-powered opportunity analysis
│       ├── matchers/            # Business profile matching logic
│       ├── notifiers/           # Alert and notification systems
│       ├── data/                # Data models and database interfaces
│       └── utils/               # Utility functions and helpers
├── tests/                       # Unit and integration tests
├── config/                      # Configuration files
├── data/                        # Data storage (grants, profiles, etc.)
├── logs/                        # Application logs
├── docs/                        # Additional documentation
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project configuration
└── README.md                    # This file
```

## 🚦 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip or poetry for package management
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd eu-grants-monitor-agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up configuration:
```bash
cp config/config.template.yaml config/config.yaml
cp config/business_profile.template.yaml config/business_profile.yaml
```

5. Configure your business profile and API keys in the config files.

### Quick Start

1. Run the initial setup:
```bash
python -m grants_monitor setup
```

2. Start monitoring:
```bash
python -m grants_monitor run
```

3. View available opportunities:
```bash
python -m grants_monitor list --filter ai --complexity simple
```

## ⚙️ Configuration

### Business Profile Setup

Edit `config/business_profile.yaml` to define:
- Your consultancy size and capabilities
- AI expertise areas (ML, NLP, Computer Vision, etc.)
- Industry focus (Healthcare, Finance, Manufacturing, etc.)
- Geographic preferences
- Funding amount ranges
- Application complexity preferences

### Monitoring Settings

Configure in `config/config.yaml`:
- Scan frequency and schedules
- Notification preferences
- Data source priorities
- Filtering criteria
- Alert thresholds

## 🤖 Agent Capabilities

### Smart Opportunity Analysis
- **Relevance Scoring**: AI-powered assessment of how well opportunities match your profile
- **Complexity Rating**: Evaluates application difficulty and requirements
- **Success Probability**: Estimates likelihood of winning based on competition and fit
- **ROI Analysis**: Calculates potential return on investment for application effort

### Automated Workflows
- **Daily Monitoring**: Scheduled scans of all configured data sources
- **Alert Generation**: Immediate notifications for high-priority opportunities
- **Deadline Tracking**: Proactive reminders for application deadlines
- **Portfolio Management**: Tracks application status and outcomes

## 📈 Usage Examples

### Finding AI-Related Grants
```bash
python -m grants_monitor search --keywords "artificial intelligence" --amount "50000-500000"
```

### Setting Up Automated Alerts
```bash
python -m grants_monitor alerts add --profile sme_ai_consultancy --notify email
```

### Generating Application Guidance
```bash
python -m grants_monitor assist --grant-id HE-2024-AI-SME-001
```

### Masumi Integration (Decentralized AI Agent)

The agent can be deployed as a Masumi-integrated service, accessible via Cardano payments:

```bash
# Start the API server for Masumi integration
python -m grants_monitor serve-api --port 8000

# Register with Masumi registry (requires API key)
python -m grants_monitor register-masumi \
  --api-key YOUR_MASUMI_API_KEY \
  --api-url https://your-domain.com \
  --environment production \
  --network Mainnet

# Check registration status
python -m grants_monitor check-masumi-status \
  --api-key YOUR_MASUMI_API_KEY \
  --wallet-vkey YOUR_WALLET_VKEY
```

See [MASUMI_INTEGRATION.md](docs/MASUMI_INTEGRATION.md) for complete integration guide.

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=grants_monitor tests/
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- Create an issue for bug reports or feature requests
- Check the [docs/](docs/) folder for detailed documentation
- Review the [FAQ](docs/FAQ.md) for common questions

## 🗺 Roadmap

- [ ] Integration with additional EU funding portals
- [ ] Advanced ML models for opportunity ranking
- [ ] Automated application draft generation
- [ ] Partnership matching with other SMEs
- [ ] Success rate analytics and reporting
- [ ] Mobile app for notifications and monitoring

## 🏢 Target Use Cases

This agent is specifically designed for:
- Small AI consultancies (2-50 employees)
- Technology startups seeking R&D funding
- Independent consultants specializing in AI/ML
- Small tech companies pivoting to AI solutions
- Research-oriented SMEs in the AI space

---

**Note**: This is an autonomous monitoring system. Always verify grant details and requirements from official EU sources before applying.
