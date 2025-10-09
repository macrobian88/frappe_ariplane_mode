#!/bin/bash

# Comprehensive fix script for JavaScript MIME type and asset issues
# Run this script when you encounter MIME type errors or 404s

echo "🔧 Comprehensive Asset and MIME Type Fix for Airplane Mode..."
echo "============================================================="

# Check if we're in a Frappe bench directory
if [ ! -f "sites/common_site_config.json" ]; then
    echo "❌ Error: Please run this script from your frappe-bench directory"
    exit 1
fi

echo "📋 Step 1: Checking and creating missing assets..."

# Check if assets exist in the app directory
if [ ! -f "apps/airplane_mode/airplane_mode/public/css/web.css" ]; then
    echo "⚠️  Missing web.css - this should have been created in the repository"
    echo "   Please pull latest changes from the repository"
fi

if [ ! -f "apps/airplane_mode/airplane_mode/public/images/favicon.svg" ]; then
    echo "⚠️  Missing favicon.svg - this should have been created in the repository"
    echo "   Please pull latest changes from the repository"
fi

echo "🧹 Step 2: Clearing caches..."
bench clear-cache
bench clear-website-cache

echo "🔨 Step 3: Building assets for airplane_mode..."
bench build --app airplane_mode --force

echo "🔄 Step 4: Restarting services..."
bench restart

echo "✅ Step 5: Verifying assets..."

# Check built assets
CSS_FILE="sites/assets/airplane_mode/css/web.css"
JS_FILE="sites/assets/airplane_mode/js/airplane_mode.js"
FAVICON_FILE="sites/assets/airplane_mode/images/favicon.svg"

echo "🔍 Checking built assets:"

if [ -f "$CSS_FILE" ]; then
    echo "✅ web.css exists and is accessible"
    echo "📏 File size: $(du -h "$CSS_FILE" | cut -f1)"
else
    echo "❌ web.css not found in built assets!"
    echo "🔍 Available CSS files:"
    ls -la sites/assets/airplane_mode/css/ 2>/dev/null || echo "   CSS directory not found"
fi

if [ -f "$JS_FILE" ]; then
    echo "✅ airplane_mode.js exists and is accessible"
    echo "📏 File size: $(du -h "$JS_FILE" | cut -f1)"
else
    echo "❌ airplane_mode.js not found in built assets!"
    echo "🔍 Available JS files:"
    ls -la sites/assets/airplane_mode/js/ 2>/dev/null || echo "   JS directory not found"
fi

if [ -f "$FAVICON_FILE" ]; then
    echo "✅ favicon.svg exists and is accessible"
    echo "📏 File size: $(du -h "$FAVICON_FILE" | cut -f1)"
else
    echo "❌ favicon.svg not found in built assets!"
    echo "🔍 Available image files:"
    ls -la sites/assets/airplane_mode/images/ 2>/dev/null || echo "   Images directory not found"
fi

echo ""
echo "🎯 Step 6: Testing HTTP responses..."

# Optional: Test if the site is responding
if command -v curl &> /dev/null; then
    SITE_URL=$(bench config get host_name 2>/dev/null || echo "localhost:8000")
    echo "🌐 Testing site: http://$SITE_URL"
    
    # Test CSS file
    echo "📄 Testing CSS file..."
    CSS_RESPONSE=$(curl -s -I "http://$SITE_URL/assets/airplane_mode/css/web.css" 2>/dev/null)
    if echo "$CSS_RESPONSE" | grep -q "200 OK"; then
        echo "✅ CSS file is accessible via HTTP"
        CSS_CONTENT_TYPE=$(echo "$CSS_RESPONSE" | grep -i "content-type" | cut -d' ' -f2-)
        echo "📝 Content-Type: $CSS_CONTENT_TYPE"
        if echo "$CSS_CONTENT_TYPE" | grep -q "text/css"; then
            echo "✅ CSS has correct MIME type"
        else
            echo "⚠️  CSS MIME type may be incorrect"
        fi
    else
        echo "❌ CSS file not accessible via HTTP"
    fi
    
    # Test JS file
    echo "📄 Testing JS file..."
    JS_RESPONSE=$(curl -s -I "http://$SITE_URL/assets/airplane_mode/js/airplane_mode.js" 2>/dev/null)
    if echo "$JS_RESPONSE" | grep -q "200 OK"; then
        echo "✅ JavaScript file is accessible via HTTP"
        JS_CONTENT_TYPE=$(echo "$JS_RESPONSE" | grep -i "content-type" | cut -d' ' -f2-)
        echo "📝 Content-Type: $JS_CONTENT_TYPE"
        if echo "$JS_CONTENT_TYPE" | grep -q -E "(application/javascript|text/javascript)"; then
            echo "✅ JavaScript has correct MIME type"
        else
            echo "⚠️  JavaScript MIME type may be incorrect"
        fi
    else
        echo "❌ JavaScript file not accessible via HTTP"
    fi
    
    # Test route
    echo "📄 Testing shop-availability route..."
    ROUTE_RESPONSE=$(curl -s -I "http://$SITE_URL/shop-availability" 2>/dev/null)
    if echo "$ROUTE_RESPONSE" | grep -q "200 OK"; then
        echo "✅ shop-availability route is accessible"
    else
        echo "❌ shop-availability route not accessible"
        echo "🔍 Response:"
        echo "$ROUTE_RESPONSE"
    fi
    
else
    echo "ℹ️  Install curl to test HTTP responses"
fi

echo ""
echo "🛠️  Step 7: Additional troubleshooting..."

# Check if airplane_mode app is properly installed
echo "📦 Checking app installation..."
if bench --site "$(ls sites | grep -v assets | grep -v common_site_config.json | head -1)" list-apps | grep -q "airplane_mode"; then
    echo "✅ airplane_mode app is installed"
else
    echo "❌ airplane_mode app not found in installed apps"
    echo "🔧 Try: bench --site your-site-name install-app airplane_mode"
fi

# Check hooks.py configuration
if [ -f "apps/airplane_mode/airplane_mode/hooks.py" ]; then
    echo "✅ hooks.py exists"
    if grep -q "web_include_css.*web.css" apps/airplane_mode/airplane_mode/hooks.py; then
        echo "✅ web.css is configured in hooks.py"
    else
        echo "⚠️  web.css may not be properly configured in hooks.py"
    fi
else
    echo "❌ hooks.py not found"
fi

echo ""
echo "📋 Summary and Next Steps:"
echo "========================="

# Count issues
ISSUES=0

if [ ! -f "$CSS_FILE" ]; then
    echo "❌ CSS file missing"
    ((ISSUES++))
fi

if [ ! -f "$JS_FILE" ]; then
    echo "❌ JavaScript file missing"
    ((ISSUES++))
fi

if [ ! -f "$FAVICON_FILE" ]; then
    echo "❌ Favicon missing"
    ((ISSUES++))
fi

if [ $ISSUES -eq 0 ]; then
    echo "🎉 All assets appear to be correctly built and accessible!"
    echo ""
    echo "✅ If you're still seeing errors:"
    echo "   1. Clear your browser cache (Ctrl+Shift+R)"
    echo "   2. Check browser console for any remaining errors"
    echo "   3. Verify MIME types in Network tab"
else
    echo "⚠️  Found $ISSUES asset issues. Try these solutions:"
    echo ""
    echo "🔧 Manual fixes:"
    echo "   1. Pull latest repository changes:"
    echo "      git pull origin main"
    echo ""
    echo "   2. Force app reinstallation:"
    echo "      bench --site your-site-name uninstall-app airplane_mode"
    echo "      bench --site your-site-name install-app airplane_mode"
    echo ""
    echo "   3. Hard reset assets:"
    echo "      rm -rf sites/assets/airplane_mode"
    echo "      bench build --app airplane_mode --force"
    echo ""
    echo "   4. Check the COMPLETE_ASSET_FIX_GUIDE.md for detailed troubleshooting"
fi

echo ""
echo "📖 For detailed troubleshooting:"
echo "   - See: COMPLETE_ASSET_FIX_GUIDE.md"
echo "   - See: JAVASCRIPT_MIME_TYPE_FIX.md"
echo ""
echo "🎯 Script completed! Check the summary above for any remaining issues."
