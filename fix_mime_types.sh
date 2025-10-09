#!/bin/bash

# Quick fix script for JavaScript MIME type issues
# Run this script when you encounter MIME type errors

echo "🔧 Fixing JavaScript MIME type issues for Airplane Mode..."
echo "=================================================="

# Check if we're in a Frappe bench directory
if [ ! -f "sites/common_site_config.json" ]; then
    echo "❌ Error: Please run this script from your frappe-bench directory"
    exit 1
fi

echo "📋 Step 1: Clearing caches..."
bench clear-cache
bench clear-website-cache

echo "🔨 Step 2: Building assets for airplane_mode..."
bench build --app airplane_mode --force

echo "🧹 Step 3: Clearing browser caches (if possible)..."
# This will clear server-side caches, browser cache needs manual clearing

echo "🔄 Step 4: Restarting services..."
bench restart

echo "✅ Step 5: Verifying JavaScript files..."
JS_FILE="sites/assets/airplane_mode/js/airplane_mode.js"
if [ -f "$JS_FILE" ]; then
    echo "✅ airplane_mode.js exists and is accessible"
    echo "📏 File size: $(du -h "$JS_FILE" | cut -f1)"
else
    echo "❌ airplane_mode.js not found in assets!"
    echo "🔍 Available files in js directory:"
    ls -la sites/assets/airplane_mode/js/ 2>/dev/null || echo "   Directory not found"
fi

echo ""
echo "🎯 Quick verification steps:"
echo "1. Check browser console for JavaScript errors"
echo "2. Verify asset path: /assets/airplane_mode/js/airplane_mode.js"
echo "3. Check server response headers for Content-Type"
echo ""
echo "📖 For more details, see: JAVASCRIPT_MIME_TYPE_FIX.md"
echo ""

# Optional: Test if the site is responding
echo "🌐 Testing site response..."
if command -v curl &> /dev/null; then
    SITE_URL=$(bench config get host_name 2>/dev/null || echo "localhost:8000")
    echo "Testing: http://$SITE_URL/assets/airplane_mode/js/airplane_mode.js"
    
    RESPONSE=$(curl -s -I "http://$SITE_URL/assets/airplane_mode/js/airplane_mode.js" 2>/dev/null)
    if echo "$RESPONSE" | grep -q "200 OK"; then
        echo "✅ JavaScript file is accessible via HTTP"
        CONTENT_TYPE=$(echo "$RESPONSE" | grep -i "content-type" | cut -d' ' -f2-)
        echo "📝 Content-Type: $CONTENT_TYPE"
    else
        echo "❌ JavaScript file not accessible via HTTP"
        echo "🔍 Response headers:"
        echo "$RESPONSE"
    fi
else
    echo "ℹ️  Install curl to test HTTP responses"
fi

echo ""
echo "🎉 Script completed! If issues persist, check the troubleshooting guide."
