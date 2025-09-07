# EU Grants Monitor Web Platform

A comprehensive web application that provides companies with AI-powered assistance for discovering and applying to EU grant opportunities.

## 🌟 Features

### Free Features
- **Grant Discovery**: Browse and search thousands of EU grant opportunities
- **Advanced Filtering**: Filter by program, country, funding amount, technology area, etc.
- **Grant Details**: View comprehensive information about each grant opportunity
- **Company Registration**: Create company profiles with Google/Microsoft SSO login
- **Basic Dashboard**: Track viewed grants and basic application status

### Premium AI Assistant Features (Paid)
- **AI-Powered Grant Analysis**: Get intelligent relevance scoring and recommendations
- **Smart Form Pre-filling**: Automatically populate application forms with company data
- **Application Guidance**: Step-by-step guidance through the application process
- **Document Generation**: Generate completed application documents
- **Success Probability Assessment**: AI-powered evaluation of application chances

## 🏗 Architecture

### Backend (FastAPI)
- **Authentication**: Google/Microsoft OAuth integration
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Payments**: Stripe integration for AI Assistant subscriptions
- **AI Integration**: Connects to existing EU Grants Monitor Agent
- **Background Tasks**: Automated grant data synchronization

### Frontend (Next.js + React)
- **Responsive Design**: Works on all devices
- **Modern UI**: Built with Tailwind CSS and Headless UI
- **Real-time Updates**: React Query for data management
- **Payment Flow**: Stripe Elements integration
- **Type Safety**: Full TypeScript implementation

### Database Schema
- **Users**: Authentication and subscription management
- **Companies**: Company profiles and preferences
- **Grants**: Comprehensive grant opportunity database
- **Applications**: Application tracking and management
- **Payments**: Transaction history and billing

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- Redis (optional, for caching)

### Backend Setup

1. **Environment Setup**
```bash
cd webapp/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Database Setup**
```bash
# Create PostgreSQL database
createdb eu_grants_monitor

# Set environment variables
cp .env.example .env
# Edit .env with your database credentials and API keys
```

3. **Database Migration**
```bash
# Create tables and seed data
python -c "from app.database import reset_db; reset_db()"
```

4. **Start Backend**
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Install Dependencies**
```bash
cd webapp/frontend
npm install
```

2. **Environment Configuration**
```bash
cp .env.local.example .env.local
# Edit .env.local with API endpoints and keys
```

3. **Start Frontend**
```bash
npm run dev
```

The web application will be available at `http://localhost:3000`

## 🔧 Configuration

### Backend Environment Variables (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/eu_grants_monitor

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256

# OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
MICROSOFT_CLIENT_ID=your-microsoft-client-id
MICROSOFT_CLIENT_SECRET=your-microsoft-client-secret

# Stripe Payment Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email Configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# AI Assistant Integration
AI_ASSISTANT_ENDPOINT=http://localhost:8001
```

### Frontend Environment Variables (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
NEXT_PUBLIC_MICROSOFT_CLIENT_ID=your-microsoft-client-id
```

## 💳 Payment Integration

The platform uses Stripe for payment processing with three subscription models:

### Pricing Structure
- **Monthly Subscription**: €49/month - Unlimited AI assistance
- **Yearly Subscription**: €499/year - Unlimited AI assistance (2 months free)
- **Pay-per-Application**: €19 per application - Perfect for occasional users

### Payment Flow
1. User selects subscription type
2. Frontend creates payment intent via backend API
3. Stripe handles secure payment processing
4. Webhook confirms payment success
5. User subscription is activated automatically

## 🔐 Authentication

### OAuth Integration

**Google OAuth Setup:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs

**Microsoft OAuth Setup:**
1. Go to [Azure Portal](https://portal.azure.com/)
2. Register new application
3. Configure authentication settings
4. Add redirect URIs
5. Generate client secret

### Security Features
- JWT token authentication
- Secure password hashing
- CORS protection
- Rate limiting
- HTTPS enforcement (production)

## 📊 Database Schema

### Key Models

**User Model:**
- Authentication data (Google/Microsoft IDs)
- Subscription information
- AI Assistant usage tracking

**Company Model:**
- Company profile and details
- AI expertise and preferences
- Funding requirements

**Grant Model:**
- Comprehensive grant information
- Eligibility criteria
- Application deadlines
- AI analysis results

**Application Model:**
- Application tracking
- Form data storage
- AI assistance usage
- Submission status

## 🤖 AI Integration

The web platform integrates with the existing EU Grants Monitor Agent to provide:

### AI Services
- **Grant Analysis**: Relevance scoring and recommendations
- **Form Pre-filling**: Intelligent form completion
- **Document Generation**: Automated application document creation
- **Success Prediction**: AI-powered application success probability

### Integration Points
- Backend communicates with agent via HTTP API
- Real-time analysis results
- Asynchronous document generation
- Usage tracking and billing

## 🚀 Deployment

### Production Deployment

**Backend Deployment (Docker):**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Deployment (Vercel/Netlify):**
```bash
npm run build
npm run start
```

### Environment Configuration

**Production Environment Variables:**
- Use strong SECRET_KEY
- Configure production database
- Set up production Stripe keys
- Configure proper CORS origins
- Enable HTTPS redirects

### Database Migration
```bash
# Production database setup
alembic upgrade head
python -c "from app.database import init_db; init_db()"
```

## 📈 Monitoring and Analytics

### Application Monitoring
- Health check endpoints
- Database connection monitoring  
- API response time tracking
- Error logging and alerting

### Business Analytics
- User registration metrics
- Subscription conversion rates
- Grant search patterns
- AI Assistant usage statistics

### Performance Optimization
- Database query optimization
- Frontend code splitting
- API response caching
- CDN integration for static assets

## 🧪 Testing

### Backend Testing
```bash
cd webapp/backend
pytest tests/ -v
pytest --cov=app tests/
```

### Frontend Testing
```bash
cd webapp/frontend
npm run test
npm run test:e2e
```

### API Testing
Use the interactive API documentation at `/docs` to test all endpoints.

## 📝 Development Workflow

### Adding New Features

1. **Backend Changes:**
   - Update models in `app/models.py`
   - Create/update API endpoints
   - Add database migrations if needed
   - Update tests

2. **Frontend Changes:**
   - Create new React components
   - Update API client
   - Add new routes
   - Update UI components

3. **Database Changes:**
   - Create Alembic migrations
   - Update model definitions
   - Test migrations

### Code Quality
- Use Black for Python formatting
- Use Prettier for frontend formatting
- Follow TypeScript strict mode
- Write comprehensive tests
- Document all API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request
5. Ensure all checks pass

## 📞 Support

For technical support or questions:
- Create GitHub issues for bugs
- Check the API documentation at `/docs`
- Review existing issues and discussions

---

## 🎯 Next Steps

To complete the web platform:

1. **Frontend Development**: Build React components for all major features
2. **OAuth Integration**: Set up Google/Microsoft developer accounts
3. **Stripe Integration**: Configure payment processing
4. **Database Setup**: Configure PostgreSQL and run migrations  
5. **AI Integration**: Connect to existing grants monitor agent
6. **Testing**: Comprehensive testing of all features
7. **Deployment**: Set up production infrastructure

The foundation is complete - now ready for full implementation!
