# Building APK - Step by Step Guide

## Quick Build (If Android project already exists)

If the `android` directory already exists and is initialized:

```bash
cd android
cp ../jayathasoft.keystore app/jayathasoft.keystore
bubblewrap build --keystorePath app/jayathasoft.keystore --keystoreAlias jayathasoft
```

The APK will be at: `android/app/build/outputs/apk/release/app-release.apk`

## First Time Setup (Interactive)

### Step 1: Initialize Bubblewrap

Run this command:

```bash
bubblewrap init --manifest https://readingplan.vercel.app/manifest.json
```

### Step 2: Answer the Prompts

When prompted, enter the following:

1. **Domain**: `readingplan.vercel.app`
2. **URL path**: `/` (just press Enter for default)
3. **Application name**: `JOURNEY`
4. **Short name**: `journey` (or `JOURNEY`)
5. **Display mode**: `standalone` (default, just press Enter)
6. **Theme color**: `#2c5a8c` (or press Enter for default)
7. **Background color**: `#667eea` (or press Enter for default)
8. **Enable notifications**: `n` (no)
9. **Splash screen**: `y` (yes)
10. **Maskable icon**: `y` (yes)
11. **Monochrome icon**: `n` (no)
12. **Shortcuts**: `[]` (empty array, just press Enter)
13. **Signing key**: When asked about signing key, choose option to use existing key

### Step 3: Copy Keystore

After initialization, copy the keystore:

```bash
cp jayathasoft.keystore android/app/jayathasoft.keystore
```

### Step 4: Build APK

```bash
cd android
bubblewrap build --keystorePath app/jayathasoft.keystore --keystoreAlias jayathasoft
```

You'll be prompted for:
- **Keystore password**: (enter your keystore password)
- **Key alias password**: (enter your key password, usually same as keystore password)
- **Key alias**: `jayathasoft` (should be pre-filled)

### Step 5: Find Your APK

The signed APK will be at:
```
android/app/build/outputs/apk/release/app-release.apk
```

## Troubleshooting

### "Android project not initialized"
- Run `bubblewrap init` first (see Step 1 above)

### "Keystore not found"
- Make sure `jayathasoft.keystore` is in the project root
- Copy it: `cp jayathasoft.keystore android/app/jayathasoft.keystore`

### "Build failed"
- Check that Java JDK is installed: `java -version`
- Check that Android SDK is installed
- Make sure you have internet connection (for downloading dependencies)

### "Signing failed"
- Verify keystore password is correct
- Verify key alias is `jayathasoft`
- Check that keystore file is not corrupted

## Alternative: Use PWABuilder (Online - No Setup Required)

1. Visit: https://www.pwabuilder.com/
2. Enter URL: `https://readingplan.vercel.app/`
3. Click "Build My PWA"
4. Select Android → Generate Package
5. Download the APK

This is the easiest method if you don't want to set up the build environment!

