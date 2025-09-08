#!/bin/bash

# EU Grants Monitor - GitHub Deployment Script
# Run this after creating your GitHub repository

echo "🚀 EU Grants Monitor - GitHub Deployment"
echo "=========================================="

# Check if repository URL is provided
if [ -z "$1" ]; then
    echo "❌ Please provide your GitHub repository URL"
    echo "Usage: ./deploy.sh https://github.com/yourusername/eu-grants-monitor.git"
    echo ""
    echo "Steps to get your repository URL:"
    echo "1. Go to https://github.com/new"
    echo "2. Create repository: 'eu-grants-monitor'"
    echo "3. Copy the repository URL (https://github.com/yourusername/eu-grants-monitor.git)"
    echo "4. Run: ./deploy.sh https://github.com/yourusername/eu-grants-monitor.git"
    exit 1
fi

REPO_URL=$1

echo "📦 Adding GitHub remote..."
git remote add origin $REPO_URL

echo "🔄 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Code successfully pushed to GitHub!"
echo "🔗 Repository: $REPO_URL"
echo ""
echo "🎯 Next Steps:"
echo "1. Deploy Backend to Railway: https://railway.app"
echo "2. Deploy Frontend to Vercel: https://vercel.com"
echo "3. Configure environment variables"
echo ""
