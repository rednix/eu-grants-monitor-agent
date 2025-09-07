# 🚀 EU Grants Monitor - Deployment Guide

This guide will help you deploy the EU Grants Monitor to production in under 30 minutes.

## 📋 Prerequisites

- ✅ Backend working locally (we already have this)
- ✅ Frontend working locally (we already have this) 
- ✅ Supabase database set up (we already have this)
- 📝 Domain name (you'll need to purchase this)
- 📝 GitHub repository (for deployments)

## 🎯 Deployment Strategy

**Frontend**: Vercel (free tier, perfect for Next.js)
**Backend**: Railway (affordable, Python-friendly)
**Database**: Supabase (already set up)
**Domain**: Namecheap/Cloudflare (your choice)

## 🏗️ Step-by-Step Deployment

### 1. 📂 Create GitHub Repository

```bash
# Initialize git in the webapp directory
cd /Users/nico/projects/eu-grants-monitor-agent/webapp
git init
git add .
git commit -m "Initial commit - EU Grants Monitor"

# Create repository on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/eu-grants-monitor.git
git branch -M main
git push -u origin main
```

### 2. 🔧 Deploy Backend to Railway

1. **Sign up to Railway**: https://railway.app
2. **Create new project** → Import from GitHub
3. **Select your repository** → Choose `webapp/backend` folder
4. **Environment Variables**: Add these in Railway dashboard:

```bash
# Required Environment Variables for Railway
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-super-secure-secret-key-here

# Supabase (use your existing values from .env)
SUPABASE_DATABASE_URL=postgresql://postgres:your-password@your-project.supabase.co:5432/postgres
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# OAuth (you'll need to set these up)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
MICROSOFT_CLIENT_ID=your-microsoft-client-id
MICROSOFT_CLIENT_SECRET=your-microsoft-client-secret

# Stripe (optional for now)
STRIPE_PUBLISHABLE_KEY=pk_test_placeholder
STRIPE_SECRET_KEY=sk_test_placeholder

# URLs (update after deployment)
FRONTEND_URL=https://your-domain.com
BACKEND_URL=https://your-backend.up.railway.app
```

5. **Deploy**: Railway will automatically deploy. You'll get a URL like `https://your-app.up.railway.app`

### 3. 🌐 Deploy Frontend to Vercel

1. **Sign up to Vercel**: https://vercel.com
2. **Import from GitHub** → Select your repository
3. **Framework**: Next.js (auto-detected)
4. **Root Directory**: Set to `webapp/frontend`
5. **Environment Variables**: Add these in Vercel dashboard:

```bash
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_placeholder
```

6. **Deploy**: Vercel will build and deploy. You'll get a URL like `https://your-app.vercel.app`

### 4. 🔗 Set Up Custom Domain

#### Option A: Use Vercel's Domain
1. Go to your Vercel project settings
2. Add custom domain (e.g., `eugrants-monitor.com`)
3. Update DNS records as instructed

#### Option B: Use Railway's Domain
1. In Railway, go to your service settings
2. Add custom domain for the backend API
3. Update DNS records

### 5. 🔐 Configure OAuth Providers

#### Google OAuth:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `https://your-domain.com/api/auth/google/callback`
   - `https://your-backend-domain.com/api/auth/google/callback`

#### Microsoft OAuth:
1. Go to [Azure Portal](https://portal.azure.com)
2. Register new application
3. Add redirect URIs:
   - `https://your-domain.com/api/auth/microsoft/callback`
   - `https://your-backend-domain.com/api/auth/microsoft/callback`

### 6. 🔄 Update Environment Variables

After deployment, update these in both Railway and Vercel:

**Railway Backend**:
```bash
FRONTEND_URL=https://your-domain.com
BACKEND_URL=https://your-backend-domain.com
GOOGLE_REDIRECT_URI=https://your-backend-domain.com/api/auth/google/callback
MICROSOFT_REDIRECT_URI=https://your-backend-domain.com/api/auth/microsoft/callback
```

**Vercel Frontend**:
```bash
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
```

### 7. ✅ Test Deployment

1. **Backend Health Check**:
   ```bash
   curl https://your-backend-domain.com/api/health
   ```

2. **Frontend Access**:
   - Visit `https://your-domain.com`
   - Test grant browsing
   - Test authentication flow

3. **API Integration**:
   - Check if grants load on homepage
   - Test search functionality

## 🎯 Quick Start Commands

Here's everything in one go:

```bash
# 1. Prepare for deployment
cd /Users/nico/projects/eu-grants-monitor-agent/webapp
git init
git add .
git commit -m "Ready for deployment"

# 2. Push to GitHub (create repo first)
git remote add origin https://github.com/YOUR_USERNAME/eu-grants-monitor.git
git push -u origin main

# 3. Deploy to Railway (backend)
# - Import from GitHub
# - Add environment variables from .env.production.template
# - Note the deployment URL

# 4. Deploy to Vercel (frontend)
# - Import from GitHub  
# - Set root directory to webapp/frontend
# - Add NEXT_PUBLIC_API_URL with Railway URL

# 5. Set up custom domain
# - Add domain to Vercel/Railway
# - Update DNS records
# - Update environment variables with final URLs
```

## 💰 Cost Breakdown

- **Railway**: $5-10/month for backend hosting
- **Vercel**: Free for frontend (hobby plan)
- **Domain**: $10-15/year
- **Supabase**: Free tier (already using)

**Total**: ~$10-15/month + domain cost

## 🚨 Important Security Notes

1. **Never commit secrets** to GitHub
2. **Use strong SECRET_KEY** for production
3. **Enable HTTPS only** in production
4. **Set proper CORS origins**
5. **Use environment variables** for all secrets

## 🔧 Post-Deployment Checklist

- [ ] Backend health check passes
- [ ] Frontend loads correctly  
- [ ] Grants data displays
- [ ] OAuth login works
- [ ] Search functionality works
- [ ] Mobile responsive
- [ ] SSL certificate active
- [ ] Analytics set up (optional)
- [ ] Error monitoring set up (optional)

## 🆘 Troubleshooting

### Backend Issues:
- Check Railway logs
- Verify environment variables
- Test database connectivity

### Frontend Issues:
- Check Vercel build logs
- Verify API URL configuration
- Test API endpoints directly

### Domain Issues:
- DNS propagation can take 24-48 hours
- Use DNS checker tools
- Verify SSL certificate

## 🎉 You're Live!

Once deployed, your EU Grants Monitor will be accessible at your custom domain, with:
- ✅ Professional landing page
- ✅ Grant search and browsing
- ✅ User authentication
- ✅ Responsive design
- ✅ Production-ready backend API

**Estimated deployment time**: 20-30 minutes (excluding DNS propagation)

---

Need help? The deployment is straightforward, but let me know if you run into any issues!
