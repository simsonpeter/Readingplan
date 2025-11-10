# Offline App with Auto-Update System

This app is designed to work **completely offline** as an Android app, but can **automatically update content** without requiring APK updates.

## How It Works

### 1. **Offline-First Architecture**
- All content (Bibles, reading plans, dictionary) is cached locally
- App works 100% offline after first installation
- No internet connection required for normal usage

### 2. **Automatic Content Updates**
- When online, the app checks for new content versions
- Content files use **Network-First** strategy:
  - Tries to fetch from network first (gets latest version)
  - If network fails, uses cached version (offline mode)
  - Automatically updates cache when new content is available

### 3. **Update Detection**
- App checks for updates:
  - On startup (after 2 seconds)
  - Every 5 minutes while app is running
- When new content is detected:
  - Shows notification: "📥 New content available!"
  - Automatically reloads app with updated content
  - No user action required

## Files Involved

### `app-version.json`
Version manifest that tracks:
- Overall app version
- Last update timestamp
- Individual file versions and modification dates

### `service-worker.js`
Service Worker that:
- Caches all content for offline use
- Implements Network-First strategy for content files
- Implements Cache-First strategy for static files (HTML, CSS, JS)
- Checks for version updates

### `index.html`
Main app that:
- Registers service worker
- Checks for updates on startup
- Periodically checks for updates
- Shows update notifications

## How to Update Content

### Method 1: Automatic (Recommended)
1. Update your content files (e.g., `bibles/tamilbible.json`, `plan/njcplan.json`)
2. Update the version in `app-version.json`:
   ```bash
   node update-version.js 1.0.1
   ```
   Or manually edit `app-version.json` and increment the version number.

3. Deploy to your web server (GitHub Pages, Vercel, etc.)
4. Users will automatically get the update when they open the app (if online)

### Method 2: Manual Version Update
1. Edit `app-version.json`
2. Change the `version` field (e.g., from `"1.0.0"` to `"1.0.1"`)
3. Update `lastUpdated` timestamp
4. Optionally update individual file versions in `contentFiles`

## Update Script

Use the helper script to automatically update versions:

```bash
# Increment patch version automatically (1.0.0 -> 1.0.1)
node update-version.js

# Set specific version
node update-version.js 1.1.0
```

The script will:
- Increment version (or use provided version)
- Update `lastUpdated` timestamp
- Update file modification dates for all content files

## Content Files That Auto-Update

These files use Network-First strategy and update automatically:
- `plan/njcplan.json` - Reading plan
- `bibles/tamilbible.json` - Tamil Bible
- `bibles/englishbible.json` - English Bible
- `bibles/dutchbible.json` - Dutch Bible
- `bibles/tamilromanizedbible.json` - Tamil Romanized Bible
- `dictionary/TSVPA1975.dictionary.SQLite3` - Dictionary

## Static Files (Cache-First)

These files are cached and only update when service worker updates:
- `index.html` - Main app HTML
- `service-worker.js` - Service worker code
- `manifest.json` - PWA manifest
- External libraries (html2canvas, sql.js, etc.)

To update these, you need to:
1. Change the `CACHE_NAME` in `service-worker.js` (e.g., `v2` -> `v3`)
2. Deploy the new service worker
3. Users will be prompted to refresh

## Testing Updates

1. **Test locally:**
   - Make changes to a Bible file
   - Update version in `app-version.json`
   - Serve with a local server
   - Open app, then update the file and version again
   - App should detect update and reload

2. **Test on Android:**
   - Build APK and install
   - Make sure app works offline
   - Update content on server
   - Open app (with internet)
   - Should detect update and reload

## Important Notes

- **Version Changes**: Always update `app-version.json` when changing content files
- **Cache Busting**: Service worker uses version manifest to detect changes
- **Offline Mode**: App works completely offline after first load
- **Network Required**: Updates only happen when device is online
- **Automatic Reload**: App automatically reloads when update is detected (no user action needed)

## Troubleshooting

### Updates not working?
1. Check that `app-version.json` version was incremented
2. Check browser console for service worker errors
3. Clear browser cache and reload
4. Check that service worker is registered (DevTools > Application > Service Workers)

### Content not updating?
1. Verify file was actually changed on server
2. Check network tab to see if file is being fetched
3. Check service worker cache (DevTools > Application > Cache Storage)
4. Try hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

### App not working offline?
1. Check that service worker is registered
2. Check that files are in cache (DevTools > Application > Cache Storage)
3. Verify `STATIC_CACHE_FILES` and `CONTENT_FILES` include all needed files

