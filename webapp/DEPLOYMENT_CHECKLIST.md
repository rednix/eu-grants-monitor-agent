# 🚀 EU Grants Monitor - Cloud Deployment Checklist

## Pre-Deployment Checklist ✅

- [x] Code committed to local Git repository
- [x] Environment files excluded from Git (.gitignore)
- [x] Production environment templates created
- [x] Deployment documentation prepared

## Step-by-Step Deployment

### 1. 📦 GitHub Repository Setup

**What to do:**
1. Go to https://github.com/new
2. Create repository: `eu-grants-monitor`
3. Keep it public or private (your choice)
4. Don't initialize with README (we already have files)
5. Copy the repository URL

**Then run:**
```bash
cd /Users/nico/projects/eu-grants-monitor-agent/webapp
./deploy.sh https://github.com/YOURUSERNAME/eu-grants-monitor.git
```

**Expected result:** ✅ Code pushed to GitHub

### 2. 🚂 Railway Backend Deployment

**What to do:**
1. Go to https://railway.app
2. Sign up with GitHub
3. New Project → Deploy from GitHub
4. Select your `eu-grants-monitor` repository  
5. Set root directory to `backend`

**Environment Variables to add:**
```bash
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=generate-a-new-secure-key-here
SUPABASE_DATABASE_URL=postgresql://postgres:kfm-fmw!jcb.BGN8grx@iabempablugdcjhrylkv.supabase.co:5432/postgres
SUPABASE_URL=https://iabempablugdcjhrylkv.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlhYmVtcGFibHVnZGNqaHJ5bGt2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwOTk3MTksImV4cCI6MjA3MjY3NTcxOX0.b7Ag3n63kX6e5b6kWGykvjndFd5ZvWD-61LCbNg3eOY
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlhYmVtcGFibHVnZGNqaHJ5bGt2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NzA5OTcxOSwiZXhwIjoyMDcyNjc1NzE5fQ.jGwb8cQGqTSENN3vH6Yp63ojbvhtL9DOQ6I5qYY0_80
```

**Test endpoints:**
- https://your-app.up.railway.app/api/health
- https://your-app.up.railway.app/api/docs

**Expected result:** ✅ Backend API live in cloud

### 3. ▲ Vercel Frontend Deployment

**What to do:**
1. Go to https://vercel.com  
2. Sign up with GitHub
3. New Project → Import from GitHub
4. Select your `eu-grants-monitor` repository
5. Set root directory to `frontend`
6. Framework should auto-detect as Next.js

**Environment Variables to add:**
```bash
NEXT_PUBLIC_API_URL=https://your-railway-app.up.railway.app
```

**Test frontend:**
- Homepage loads
- Grants page shows data from your Supabase database

**Expected result:** ✅ Frontend live in cloud

### 4. 🔗 Connect Frontend & Backend

**Update Railway backend variables:**
```bash
FRONTEND_URL=https://your-vercel-app.vercel.app
BACKEND_URL=https://your-railway-app.up.railway.app
```

**Expected result:** ✅ Full-stack application working

## Verification Checklist

### Backend Verification ✅
- [ ] Health endpoint responds: `/api/health`
- [ ] API docs load: `/api/docs`
- [ ] Grants endpoint works: `/api/grants` (returns data from Supabase)
- [ ] Database connection working (check logs)

### Frontend Verification ✅  
- [ ] Homepage loads with grants data
- [ ] Navigation works
- [ ] API calls successful (check browser network tab)
- [ ] Responsive design works on mobile

### Integration Verification ✅
- [ ] Frontend can fetch grants from backend
- [ ] CORS configured correctly
- [ ] Environment URLs match deployed domains

## Post-Deployment

### Optional Enhancements
- [ ] **Custom Domain**: Add your own domain (e.g., grants-monitor.com)
- [ ] **OAuth Setup**: Configure Google/Microsoft login for production URLs
- [ ] **Email Alerts**: Set up email notifications for new grants  
- [ ] **Monitoring**: Set up error tracking (Sentry, LogRocket)

### Maintenance
- [ ] **Database Backups**: Supabase handles this automatically
- [ ] **Uptime Monitoring**: Both Railway and Vercel have built-in monitoring
- [ ] **Analytics**: Add Google Analytics or similar

## Cost Summary

**Monthly costs:**
- Railway (Backend): ~$5-10/month
- Vercel (Frontend): FREE (hobby plan)
- Supabase: FREE (current usage)
- **Total**: ~$5-10/month + domain (~$10/year)

## Support & Documentation

- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **Supabase Docs**: https://supabase.com/docs
- **Your API Docs**: https://your-backend.up.railway.app/api/docs
