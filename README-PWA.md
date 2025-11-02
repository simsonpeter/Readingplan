# Progressive Web App (PWA) Setup

This app is now configured as a Progressive Web App that can be installed on devices and works offline.

## Features Added

1. **Web App Manifest** (`manifest.json`)
   - App name, icons, theme colors
   - Standalone display mode
   - Installable on mobile and desktop

2. **Service Worker** (`service-worker.js`)
   - Caches all Bible files and app data for offline access
   - Automatic caching of static resources
   - Network-first strategy with cache fallback

3. **Install Prompts**
   - Automatic install button appears on supported browsers
   - Works on Chrome, Edge, Safari (iOS 11.3+), and other PWA-capable browsers

## Creating App Icons

You need to create two icon files:
- `icon-192.png` (192x192 pixels)
- `icon-512.png` (512x512 pixels)

You can:
1. Use the provided `create-icons.html` helper (open in browser and run the JavaScript in console)
2. Create your own icons with a Bible/book theme
3. Use any image editor to create PNG icons

## Installation Instructions

### For Users:

**On Android/Chrome:**
- Visit the app in Chrome
- Tap the menu (3 dots) → "Add to Home Screen" or "Install App"
- The app will install and appear on your home screen

**On iOS/Safari:**
- Visit the app in Safari
- Tap the Share button → "Add to Home Screen"
- The app will install as an icon on your home screen

**On Desktop (Chrome/Edge):**
- Visit the app in the browser
- Look for the install icon in the address bar
- Click it to install the app

## Offline Support

Once installed, the app works offline:
- All Bible translations (Tamil, English, Dutch) are cached
- Reading plan data is cached
- App interface works without internet
- New content syncs when online

## Updating the App

When a new version is available:
- The service worker automatically checks for updates
- Users will be prompted to refresh for the latest version
- Updates happen seamlessly in the background

