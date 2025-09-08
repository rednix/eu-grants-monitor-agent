# 🚂 Railway Deployment Guide

## Backend Deployment to Railway

### Step 1: Sign Up & Import Project
1. Go to https://railway.app
2. Sign up with GitHub account
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `eu-grants-monitor` repository
5. Choose "Deploy Now"

### Step 2: Configure Build Settings
Railway should auto-detect it's a Python project. If not:

1. **Root Directory**: Set to `backend`
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Environment Variables
Go to your Railway project → Variables tab and add:

```bash
# Essential Variables
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-super-secure-secret-key-generate-new-one

# Supabase (copy from your backend/.env file)
SUPABASE_DATABASE_URL=postgresql://postgres:kfm-fmw!jcb.BGN8grx@iabempablugdcjhrylkv.supabase.co:5432/postgres
SUPABASE_URL=https://iabempablugdcjhrylkv.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# URLs (update after getting Railway domain)
FRONTEND_URL=https://your-domain.vercel.app
BACKEND_URL=https://your-backend.up.railway.app
```

### Step 4: Deploy & Test
1. Railway will automatically deploy after adding variables
2. You'll get a URL like: `https://eu-grants-monitor.up.railway.app`
3. Test endpoints:
   - Health: `https://your-domain.up.railway.app/api/health`
   - Docs: `https://your-domain.up.railway.app/api/docs`

### Step 5: Update Environment Variables
Once deployed, update the BACKEND_URL variable with your actual Railway domain.

## Cost Estimate
- **Railway**: ~$5-10/month for backend hosting
- Includes 500 hours/month (enough for 24/7 operation)
- Auto-scaling included
