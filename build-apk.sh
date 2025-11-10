#!/bin/bash
# Build APK script with proper input handling

cd "$(dirname "$0")"

echo "🚀 Building APK with Bubblewrap..."

# Remove existing android directory if it exists
if [ -d "android" ]; then
    echo "⚠️  Removing existing android directory..."
    rm -rf android
fi

# Initialize Bubblewrap with proper inputs
echo "📦 Initializing Bubblewrap..."
printf "readingplan.vercel.app\n/\n" | bubblewrap init \
    --manifest https://readingplan.vercel.app/manifest.json \
    --packageId "com.jayathasoft.journey" \
    --name "JOURNEY" \
    --applicationId "journey" \
    --url "https://readingplan.vercel.app/" \
    --launcherName "JOURNEY" \
    --enableNotifications false \
    --enableSplashScreen true \
    --webManifestUrl "https://readingplan.vercel.app/manifest.json" \
    --shortcuts "[]" \
    --generatorVersion 1.21.0 \
    --skipManifestValidation

if [ $? -ne 0 ]; then
    echo "❌ Bubblewrap initialization failed"
    exit 1
fi

# Copy keystore to android directory
if [ -f "jayathasoft.keystore" ]; then
    echo "📝 Copying keystore..."
    cp jayathasoft.keystore android/app/jayathasoft.keystore
else
    echo "⚠️  Keystore not found! Building without signing..."
fi

# Build APK
echo "🔨 Building APK..."
cd android

# Check if keystore exists
if [ -f "app/jayathasoft.keystore" ]; then
    echo "📝 Using existing keystore: jayathasoft.keystore"
    echo "💡 You'll be prompted for keystore password and key alias password"
    echo "💡 Key alias is likely 'jayathasoft'"
    bubblewrap build --keystorePath app/jayathasoft.keystore --keystoreAlias jayathasoft
else
    echo "⚠️  No keystore found, building debug APK..."
    bubblewrap build
fi

if [ $? -eq 0 ]; then
    echo "✅ APK build completed!"
    if [ -f "app/build/outputs/apk/release/app-release.apk" ]; then
        echo "📦 APK location: android/app/build/outputs/apk/release/app-release.apk"
        echo "📱 APK size: $(du -h app/build/outputs/apk/release/app-release.apk | cut -f1)"
    elif [ -f "app/build/outputs/apk/release/app-release-unsigned.apk" ]; then
        echo "📦 APK location: android/app/build/outputs/apk/release/app-release-unsigned.apk"
        echo "📱 APK size: $(du -h app/build/outputs/apk/release/app-release-unsigned.apk | cut -f1)"
    fi
else
    echo "❌ APK build failed"
    exit 1
fi

