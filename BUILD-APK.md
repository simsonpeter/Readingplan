# Building APK with Bubblewrap

## Prerequisites
- Keystore: `jayathasoft.keystore` (already copied to project root)
- Keystore alias: `jayathasoft` (typical)

## Step 1: Initialize Bubblewrap (One-time setup)

Run this command and answer the prompts:

```bash
bubblewrap init --manifest https://readingplan.vercel.app/manifest.json
```

**Answers to prompts:**
1. **Domain**: `readingplan.vercel.app`
2. **URL path**: `/` (just press Enter)
3. **Application name**: `JOURNEY`
4. **Short name**: `journey` (or `JOURNEY`)
5. **Display mode**: `standalone` (default)
6. **Theme color**: `#2c5a8c` (or default)
7. **Background color**: `#667eea` (or default)
8. **Enable notifications**: `n` (no)
9. **Splash screen**: `y` (yes)
10. **Maskable icon**: `y` (yes)
11. **Monochrome icon**: `n` (no)
12. **Shortcuts**: `[]` (empty array)
13. **Signing key**: When asked, choose to use existing key

## Step 2: Configure Signing Key

After initialization, copy the keystore to the android directory:

```bash
cp jayathasoft.keystore android/app/jayathasoft.keystore
```

## Step 3: Update Signing Configuration

Edit `android/app/build.gradle` and ensure signing config uses the keystore:

```gradle
signingConfigs {
    release {
        storeFile file('jayathasoft.keystore')
        storePassword 'YOUR_KEYSTORE_PASSWORD'
        keyAlias 'jayathasoft'
        keyPassword 'YOUR_KEY_PASSWORD'
    }
}
```

## Step 4: Build APK

```bash
cd android
bubblewrap build
```

Or directly:
```bash
cd android
./gradlew assembleRelease
```

The signed APK will be at:
`android/app/build/outputs/apk/release/app-release.apk`

## Alternative: Quick Build Script

If you've already initialized, you can use:

```bash
./build-apk-auto.sh
```

This script will:
1. Initialize Bubblewrap (if needed)
2. Copy the keystore
3. Build the signed APK

## Notes

- You'll be prompted for keystore password and key password during build
- The keystore alias is likely `jayathasoft`
- If you forget passwords, check the tcradios repo documentation

