# ▲ Vercel Deployment Guide

## Frontend Deployment to Vercel

### Step 1: Sign Up & Import Project
1. Go to https://vercel.com
2. Sign up with GitHub account
3. Click "New Project" → Import from GitHub
4. Select your `eu-grants-monitor` repository
5. Configure project settings:

### Step 2: Project Configuration
- **Framework Preset**: Next.js (should auto-detect)
- **Root Directory**: Set to `frontend`
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `.next` (auto-detected)
- **Install Command**: `npm install` (auto-detected)

### Step 3: Environment Variables
Add these in Vercel dashboard → Project Settings → Environment Variables:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app

# Optional: Stripe (for payments)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_placeholder
```

### Step 4: Deploy & Test
1. Click "Deploy" - Vercel will build and deploy automatically
2. You'll get a URL like: `https://eu-grants-monitor.vercel.app`
3. Test the frontend:
   - Homepage loads
   - Grants page shows data
   - API integration works

### Step 5: Update Backend Environment
Update your Railway backend environment variable:
```bash
FRONTEND_URL=https://eu-grants-monitor.vercel.app
```

### Step 6: Custom Domain (Optional)
1. In Vercel dashboard → Project → Settings → Domains
2. Add your custom domain (e.g., `grants-monitor.com`)
3. Configure DNS records as instructed
4. Vercel provides automatic HTTPS

## Build Optimization
Vercel automatically optimizes your Next.js app with:
- **Edge Functions**: For API routes
- **Image Optimization**: Automatic image resizing
- **Global CDN**: Fast loading worldwide
- **Automatic HTTPS**: SSL certificates included

## Cost Estimate
- **Vercel**: FREE for hobby projects
- Includes:
  - 100GB bandwidth/month
  - 100 serverless function invocations/day
  - Automatic HTTPS
  - Global CDN
