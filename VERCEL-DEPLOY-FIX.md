# Fix Vercel Deployment Sync Issue

## Problem
Changes are pushed to GitHub but not automatically deploying to Vercel.

## Solution Steps

### Option 1: Manual Redeploy from Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Log in to your account

2. **Find Your Project**
   - Look for `Readingplan` or `readingplan` project
   - Click on the project name

3. **Check Deployment Status**
   - Go to the **"Deployments"** tab
   - Check if there are any failed deployments (red status)
   - Look for the latest deployment timestamp

4. **Manually Redeploy**
   - Click on the **"..."** (three dots) menu next to the latest deployment
   - Select **"Redeploy"**
   - Confirm the redeployment
   - Wait for the deployment to complete (usually 1-2 minutes)

### Option 2: Trigger via GitHub Webhook

1. **Check Vercel Integration**
   - In Vercel dashboard, go to your project
   - Click **"Settings"** → **"Git"**
   - Verify that your GitHub repository is connected
   - Ensure **"Production Branch"** is set to `main`

2. **Reconnect Repository (if needed)**
   - If repository is not connected, click **"Connect Git Repository"**
   - Select your GitHub repository: `simsonpeter/Readingplan`
   - Authorize Vercel if prompted

3. **Check Auto-Deploy Settings**
   - In Settings → Git
   - Ensure **"Automatic deployments from Git"** is enabled
   - For **Production Branch**: should be `main`

### Option 3: Force Redeploy via Git Push

If you want to trigger a new deployment:

```bash
# Create an empty commit to trigger deployment
git commit --allow-empty -m "Trigger Vercel deployment"
git push origin main
```

### Option 4: Use Vercel CLI (if installed)

```bash
# Install Vercel CLI (if not installed)
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
cd /home/simsonpeter/github/readingplan/Readingplan
vercel --prod
```

## Verify Deployment

1. **Check Deployment URL**
   - Your app should be at: `https://readingplan.vercel.app/`
   - Or check your custom domain if configured

2. **Verify Changes**
   - Open the deployed URL
   - Check if the calendar timezone fix is working (try clicking October 1st)
   - Clear browser cache if you see old version (Ctrl+Shift+R)

3. **Check Deployment Logs**
   - In Vercel dashboard → Deployments → Click on latest deployment
   - Check **"Build Logs"** for any errors
   - Check **"Function Logs"** if applicable

## Common Issues

### Issue: "No deployments found"
- **Solution**: You may need to connect your GitHub repository to Vercel for the first time
- Go to Vercel dashboard → Add New Project → Import Git Repository

### Issue: "Build failed"
- **Solution**: Check build logs for errors
- Common issues: missing files, incorrect build settings
- Since this is a static site, build command should be empty or simple

### Issue: "Deployment succeeded but site shows old version"
- **Solution**: 
  - Clear browser cache (Ctrl+Shift+R)
  - Clear service worker cache (see CLEAR-CACHE.md)
  - Wait a few minutes for CDN to update

## Recommended Vercel Settings for This Project

Since this is a static site:

1. **Framework Preset**: Other
2. **Build Command**: (leave empty - no build needed)
3. **Output Directory**: (leave empty - files are in root)
4. **Install Command**: (leave empty)

## Quick Fix: Empty Commit Push

Run this to trigger a fresh deployment:

```bash
cd /home/simsonpeter/github/readingplan/Readingplan
git commit --allow-empty -m "Trigger Vercel redeploy"
git push origin main
```

Then check Vercel dashboard - a new deployment should start automatically within 30 seconds.

