# Masumi Integration for EU Grants Monitor Agent

This document explains how to use the EU Grants Monitor Agent with the Masumi framework for payment-based AI agent services via the Cardano blockchain.

## 🌟 Overview

The EU Grants Monitor Agent is now fully integrated with Masumi, making it available as a decentralized AI agent that can be accessed through paid requests on the Cardano network. This integration provides:

- **Payment-based Access**: Users pay in ADA (Cardano's native token) to access the agent's services
- **Decentralized Registry**: The agent is registered in the Masumi agent registry for discoverability
- **API-based Services**: FastAPI endpoints provide structured access to all agent capabilities
- **Blockchain Verification**: All transactions are recorded on the Cardano blockchain

## 🏗 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Masumi User   │    │  Masumi Agent   │    │ EU Grants API   │
│                 │    │   Registry      │    │                 │
│ - Pays in ADA   │◄──►│ - Discovery     │◄──►│ - Monitoring    │
│ - Gets Results  │    │ - Verification  │    │ - Analysis      │
│ - Via Wallet    │    │ - Payment Flow  │    │ - Generation    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. Installation

The agent already includes all necessary dependencies for Masumi integration:

```bash
# Clone and setup the repository
git clone <repository-url>
cd eu-grants-monitor-agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure the Agent

Copy and edit the configuration files:

```bash
# Basic agent configuration
cp config/config.template.yaml config/config.yaml
cp config/business_profile.template.yaml config/business_profile.yaml

# Masumi-specific configuration
cp config/masumi_config.template.yaml config/masumi_config.yaml
```

Edit `config/masumi_config.yaml` with your Masumi API key and settings.

### 3. Start the API Server

```bash
# Start the API server (required for Masumi integration)
python -m grants_monitor serve-api --port 8000 --host 0.0.0.0
```

The API will be available at `http://localhost:8000` with automatic API documentation at `http://localhost:8000/docs`.

### 4. Register with Masumi

```bash
# Register the agent (development environment)
python -m grants_monitor register-masumi \
  --api-key YOUR_MASUMI_API_KEY \
  --api-url http://your-domain.com:8000 \
  --environment development \
  --network Preprod

# Check registration status
python -m grants_monitor check-masumi-status \
  --api-key YOUR_MASUMI_API_KEY \
  --wallet-vkey YOUR_WALLET_VKEY \
  --network Preprod
```

## 📊 API Endpoints

The agent exposes the following endpoints for Masumi integration:

### Core Services

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/monitor` | POST | Start intelligent EU grants monitoring |
| `/grants/list` | POST | List grants with filtering |
| `/grants/{grant_id}/assist` | POST | Get application assistance |
| `/grants/{grant_id}` | GET | Get grant details |

### Management

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/health` | GET | Health check |
| `/status` | GET | Agent status and capabilities |

### Example Usage

```bash
# List grants with filters
curl -X POST "http://localhost:8000/grants/list" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["ai", "healthcare"],
    "min_amount": 100000,
    "max_amount": 500000,
    "complexity_max": 60
  }'

# Get application assistance
curl -X POST "http://localhost:8000/grants/HE-2024-AI-001/assist" \
  -H "Content-Type: application/json" \
  -d '{
    "grant_id": "HE-2024-AI-001",
    "assistance_type": "analyze",
    "business_profile": {
      "company_name": "AI Startup Ltd",
      "company_size": "small",
      "ai_expertise": ["machine_learning", "nlp"]
    }
  }'
```

## 💰 Pricing and Payments

### Pricing Tiers

- **Development**: 1 ADA per request
- **Staging**: 1.5 ADA per request  
- **Production**: 2 ADA per request

### Payment Flow

1. **Discovery**: Users find the agent in the Masumi registry
2. **Selection**: Users choose the service they need
3. **Payment**: Users pay the required ADA amount via their Cardano wallet
4. **Verification**: Masumi verifies the payment on-chain
5. **Execution**: The agent processes the request and returns results
6. **Delivery**: Results are delivered to the user

## 🔧 Configuration

### Environment Variables

```bash
# Required for Masumi integration
export MASUMI_API_KEY="your_masumi_api_key"
export CARDANO_NETWORK="Preprod"  # or "Mainnet"
export AGENT_API_URL="https://your-agent-domain.com"

# Optional
export AGENT_PORT=8000
export LOG_LEVEL="INFO"
```

### Configuration Files

#### `config/masumi_config.yaml`

```yaml
masumi:
  payment_api_key: "your_masumi_api_key_here"
  payment_service_url: "https://api.masumi.io"
  network: "Preprod"

agent:
  name: "eu-grants-monitor"
  api_base_url: "https://api.eu-grants-monitor.com"
  pricing:
    unit: "lovelace"
    quantity: "2000000"  # 2 ADA

author:
  name: "EU Grants Monitor Team"
  contact: "contact@eu-grants-monitor.com"
```

## 🎯 Service Capabilities

### 1. EU Grants Monitoring (`/monitor`)

**Input:**
- Business profile (company size, expertise, industries)
- Filtering preferences
- Alert settings

**Output:**
- List of relevant grants
- Relevance scores
- Priority rankings
- Alert notifications

### 2. Grant Analysis (`/grants/list`)

**Input:**
- Search keywords
- Amount ranges
- Complexity limits
- Deadline constraints

**Output:**
- Filtered grant opportunities
- Scoring metrics
- Detailed grant information

### 3. Application Assistance (`/grants/{id}/assist`)

**Input:**
- Grant ID
- Business profile
- Assistance type (analyze/guidance/generate)

**Output:**
- Eligibility assessment
- Application strategy
- Pre-filled forms
- Success recommendations

## 🚀 Deployment

### Local Development

```bash
# Start local API server
python -m grants_monitor serve-api --port 8000

# Register with Masumi Preprod
python -m grants_monitor register-masumi \
  --api-key $MASUMI_API_KEY \
  --api-url http://localhost:8000 \
  --environment development
```

### Production Deployment

```bash
# Use a proper domain with HTTPS
python -m grants_monitor register-masumi \
  --api-key $MASUMI_API_KEY \
  --api-url https://api.eu-grants-monitor.com \
  --environment production \
  --network Mainnet
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "-m", "grants_monitor", "serve-api", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔒 Security Considerations

### API Security
- All endpoints validate input data using Pydantic models
- Error handling prevents information leakage
- CORS is configurable for production environments

### Masumi Integration
- Payment verification is handled by Masumi infrastructure
- API keys should be stored securely (environment variables/secrets)
- Network selection (Preprod vs Mainnet) affects payment requirements

### Data Privacy
- No sensitive user data is permanently stored
- Business profiles are used only for request processing
- All data handling complies with EU privacy regulations

## 🧪 Testing

### API Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test status endpoint
curl http://localhost:8000/status

# Test with sample data
curl -X POST http://localhost:8000/grants/list \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["ai"]}'
```

### Masumi Integration Testing

```bash
# Dry run registration
python -m grants_monitor register-masumi \
  --api-key test \
  --api-url http://localhost:8000 \
  --dry-run

# Check configuration
python -m grants_monitor register-masumi --help
```

## 🆘 Troubleshooting

### Common Issues

**1. Registration Fails**
- Check API key validity
- Verify network settings (Preprod vs Mainnet)
- Ensure API URL is publicly accessible

**2. API Server Won't Start**
- Check port availability
- Verify all dependencies are installed
- Review configuration files

**3. Payment Issues**
- Confirm wallet has sufficient ADA
- Check network connectivity
- Verify Masumi service status

### Debug Commands

```bash
# Check agent status
python -m grants_monitor --help

# Validate configuration
python -m grants_monitor register-masumi --dry-run --api-key test --api-url http://localhost:8000

# Test API locally
curl http://localhost:8000/docs
```

## 📚 Resources

- [Masumi Documentation](https://masumi.io/docs)
- [Cardano Developer Resources](https://developers.cardano.org)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [EU Funding Portal](https://ec.europa.eu/info/funding-tenders)

## 🤝 Support

For support with the EU Grants Monitor Agent:
- Create an issue in the repository
- Contact: contact@eu-grants-monitor.com
- Documentation: [Project README](../README.md)

For Masumi-specific issues:
- Masumi Support: [https://masumi.io/support](https://masumi.io/support)
- Masumi Documentation: [https://masumi.io/docs](https://masumi.io/docs)
