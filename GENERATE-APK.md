# Generate APK for JOURNEY App

## Method 1: Using PWABuilder (Easiest - Online Tool)

1. **Visit PWABuilder**: https://www.pwabuilder.com/
2. **Enter your app URL**: 
   - Your GitHub Pages URL: `https://simsonpeter.github.io/Readingplan/`
   - Or your deployed URL
3. **Click "Start"** - PWABuilder will analyze your PWA
4. **Click "Build My PWA"**
5. **Select Android** → **Generate Package**
6. **Download the APK** when ready

## Method 2: Using Bubblewrap (Command Line - More Control)

### Prerequisites:
- Node.js (v14 or higher)
- Java JDK 11 or higher
- Android SDK (via Android Studio)

### Setup:

```bash
# Install Bubblewrap CLI
npm install -g @bubblewrap/cli

# Initialize the project
bubblewrap init --manifest=https://simsonpeter.github.io/Readingplan/manifest.json

# Build APK
bubblewrap build
```

The APK will be generated in the `output/` directory.

## Method 3: Using TWA (Trusted Web Activity) - Manual Android Studio

1. **Install Android Studio**
2. **Create new project** → **Add No Activity**
3. **Add TWA dependency** to `build.gradle`:
   ```gradle
   dependencies {
       implementation 'com.google.androidbrowserhelper:androidbrowserhelper:2.5.0'
   }
   ```
4. **Configure AndroidManifest.xml** with your PWA URL
5. **Build APK** → Build → Build Bundle(s) / APK(s)

## Method 4: Using Capacitor (Cross-platform)

```bash
npm install -g @capacitor/cli
npx cap init "JOURNEY" "com.jayathasoft.journey"
npx cap add android
npx cap sync
npx cap open android
```

Then build APK from Android Studio.

## Recommended: PWABuilder

**Easiest method**: Use PWABuilder online tool at https://www.pwabuilder.com/

Just enter your GitHub Pages URL and it will generate the APK for you automatically!

## Notes:

- Make sure your app is deployed and accessible online (GitHub Pages is fine)
- The manifest.json and service worker must be working
- Icons (icon-192.png and icon-512.png) must be accessible
- APK will be signed and ready for installation

