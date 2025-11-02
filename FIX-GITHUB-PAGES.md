# Fix GitHub Pages Showing Old Version

## Quick Fix Steps:

### Option 1: Update GitHub Pages Settings (Recommended)

1. **Go to your GitHub repository**: https://github.com/simsonpeter/Readingplan
2. **Click "Settings"** tab
3. **Scroll down to "Pages"** (left sidebar)
4. **Under "Source"**, select:
   - **Branch**: `main`
   - **Folder**: `/ (root)`
5. **Click "Save"**
6. **Wait 1-2 minutes** for GitHub Pages to rebuild

### Option 2: Manual Clear Cache

If the page still shows old version after updating settings:

1. **Hard refresh your browser**:
   - Chrome/Edge: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
   - Firefox: `Ctrl + F5` or `Cmd + Shift + R`
   - Safari: `Cmd + Option + R`

2. **Clear browser cache** or use Incognito/Private mode

3. **Add cache busting**: Visit `https://simsonpeter.github.io/Readingplan/?v=2` (add `?v=2` to force reload)

### Option 3: Trigger Pages Rebuild

1. **Make a small change** (add a space or comment) to any file
2. **Commit and push**:
   ```bash
   git commit --allow-empty -m "Trigger GitHub Pages rebuild"
   git push
   ```

### Option 4: Check GitHub Pages Status

1. **Go to**: https://github.com/simsonpeter/Readingplan/actions
2. **Check if "pages build and deployment"** workflow is running
3. **If it shows errors**, check the logs

### Option 5: Use GitHub Actions (Already Added)

I've added a GitHub Actions workflow (`.github/workflows/deploy.yml`) that will automatically deploy on every push to `main`.

**To activate it:**
1. Go to repository Settings → Pages
2. Under "Source", select **"GitHub Actions"** instead of "Deploy from a branch"
3. Save

This will use the workflow I created for automatic deployment.

## Verify It's Working:

1. **Check the live site**: https://simsonpeter.github.io/Readingplan/
2. **View page source** (Ctrl+U) and check:
   - Title should show "JOURNEY — Bible Reading Plan"
   - Manifest should show "JOURNEY"
   - Splash screen should be present

## Common Issues:

- **Still showing old version**: Wait 2-3 minutes, GitHub Pages can take time to update
- **404 error**: Make sure Pages is enabled and source is set to `main` branch
- **Wrong folder**: Make sure root folder `/` is selected, not `/docs`
- **Service worker cache**: Clear site data in browser settings

## Current Status:

✅ All changes pushed to `main` branch  
✅ GitHub Actions workflow added  
✅ Ready for deployment  

**Next step**: Update GitHub Pages settings to use `main` branch or GitHub Actions.

