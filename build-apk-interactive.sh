#!/bin/bash
# Interactive APK build script
# Run this and follow the prompts

cd "$(dirname "$0")"

echo "🚀 Building APK with Bubblewrap..."
echo ""
echo "This script will guide you through building the APK."
echo ""

# Check if android directory exists and is properly initialized
if [ -d "android" ] && [ -f "android/twa-manifest.json" ]; then
    echo "✅ Android project already initialized"
    echo "📦 Proceeding to build..."
    cd android
    
    if [ -f "app/jayathasoft.keystore" ]; then
        echo "📝 Using keystore: jayathasoft.keystore"
        echo "💡 You'll be prompted for keystore password and key alias password"
        echo "💡 Key alias is likely 'jayathasoft'"
        bubblewrap build --keystorePath app/jayathasoft.keystore --keystoreAlias jayathasoft
    else
        echo "⚠️  No keystore found, building debug APK..."
        bubblewrap build
    fi
else
    echo "📦 Need to initialize Bubblewrap first..."
    echo ""
    echo "Please run this command manually and answer the prompts:"
    echo ""
    echo "  bubblewrap init --manifest https://readingplan.vercel.app/manifest.json"
    echo ""
    echo "When prompted, enter:"
    echo "  Domain: readingplan.vercel.app"
    echo "  URL path: / (just press Enter)"
    echo "  Application name: JOURNEY"
    echo "  Short name: journey (or JOURNEY)"
    echo "  Display mode: standalone (default, just press Enter)"
    echo "  Theme color: #2c5a8c (or default)"
    echo "  Background color: #667eea (or default)"
    echo "  Enable notifications: n"
    echo "  Splash screen: y"
    echo "  Maskable icon: y"
    echo "  Monochrome icon: n"
    echo "  Shortcuts: [] (empty array)"
    echo "  Signing key: Choose to use existing key when asked"
    echo ""
    echo "After initialization, run this script again to build the APK."
    exit 1
fi

if [ $? -eq 0 ]; then
    echo ""
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

