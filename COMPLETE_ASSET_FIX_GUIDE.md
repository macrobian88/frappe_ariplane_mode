# 🚨 Complete Asset and Route Fix Guide

## Problem Summary
You're experiencing multiple 404 and MIME type errors:

```
GET https://airplane-mode.m.frappe.cloud/shop-availability 404 (Not Found)
GET https://airplane-mode.m.frappe.cloud/assets/airplane_mode/css/web.css 404 (Not Found)
GET https://airplane-mode.m.frappe.cloud/assets/airplane_mode/js/airplane_mode.js 404 (Not Found)
GET https://airplane-mode.m.frappe.cloud/assets/airplane_mode/images/favicon.ico 404 (Not Found)
```

## 🔍 Root Cause Analysis

### 1. **Asset Build Issues**
- CSS and JS files aren't being built properly
- Missing image assets (favicon, logos)
- Assets not served from correct paths

### 2. **Route Configuration Problems**
- Website routes not properly registered
- Shop-availability page not accessible

### 3. **MIME Type Issues**
- Assets served as HTML instead of proper content types
- Server configuration problems

## 🛠️ Complete Solution

### **Step 1: Run Asset Creation Script**

```bash
# Create missing image assets
chmod +x create_missing_assets.sh
./create_missing_assets.sh
```

### **Step 2: Fix Assets and Build**

```bash
# Navigate to your frappe-bench directory
cd /path/to/frappe-bench

# Clear all caches
bench clear-cache
bench clear-website-cache

# Force rebuild assets
bench build --app airplane_mode --force

# Restart all services
bench restart

# If still issues, try:
bench --site your-site-name migrate
bench --site your-site-name reload-doctype "Workspace"
```

### **Step 3: Verify Assets Exist**

```bash
# Check if assets were built properly
ls -la sites/assets/airplane_mode/css/
ls -la sites/assets/airplane_mode/js/
ls -la sites/assets/airplane_mode/images/

# Expected files:
# css/airplane_mode.css
# css/web.css
# js/airplane_mode.js
# js/airplane_dashboard.js
# images/favicon.svg
# images/logo.svg
# images/splash.svg
```

### **Step 4: Run MIME Type Fix**

```bash
# Run the MIME type fix script
chmod +x fix_mime_types.sh
./fix_mime_types.sh
```

### **Step 5: Test Website Routes**

```bash
# Test if routes are working
curl -I https://your-site.com/shop-availability
curl -I https://your-site.com/assets/airplane_mode/css/web.css
```

## 🔧 Manual Asset Fix (If Scripts Fail)

### **Create Missing Files Manually**

1. **Web CSS** - Create `airplane_mode/public/css/web.css`:
```css
/* Basic website styles */
body { font-family: 'Inter', sans-serif; }
.hero-section { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
/* Full CSS content is already in the repository */
```

2. **Images Directory** - Create `airplane_mode/public/images/`:
```bash
mkdir -p airplane_mode/public/images
# SVG files are already created in the repository
```

3. **Manual Build**:
```bash
# Force asset collection
bench build --app airplane_mode --hard-link

# Alternative method
rm -rf sites/assets/airplane_mode
bench build --app airplane_mode --force
```

## 🌐 Frappe Cloud Specific Fixes

### **For Frappe Cloud Users:**

1. **Check App Installation**:
```bash
# Verify app is properly installed
bench --site your-site list-apps
```

2. **Force Asset Rebuild on Cloud**:
```bash
# In your Frappe Cloud console
bench build --app airplane_mode --force
bench migrate
bench restart
```

3. **Contact Frappe Cloud Support** if assets still don't serve:
   - Mention MIME type issues
   - Request asset server configuration check
   - Reference specific 404 errors

## 📋 Verification Checklist

### ✅ **Assets Check**
- [ ] `web.css` exists and loads
- [ ] `airplane_mode.js` exists and loads  
- [ ] `favicon.svg` exists and loads
- [ ] No MIME type errors in console

### ✅ **Routes Check**
- [ ] `/shop-availability` loads without 404
- [ ] `/shop-portal` loads properly
- [ ] `/apply-shop` loads properly
- [ ] Website navigation works

### ✅ **Console Check**
- [ ] No JavaScript errors
- [ ] No CSS loading errors
- [ ] No 404s in Network tab
- [ ] Proper Content-Type headers

## 🚨 Emergency Workarounds

### **If Assets Still Don't Load:**

1. **Inline Critical CSS** (temporary):
```html
<!-- Add to base template -->
<style>
body { font-family: 'Inter', sans-serif; }
/* Add critical styles inline */
</style>
```

2. **CDN Fallback** (temporary):
```html
<!-- Use external CDN for similar styles -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
```

3. **Disable Asset Dependencies** (last resort):
```python
# In hooks.py, comment out problematic assets temporarily
# app_include_css = "/assets/airplane_mode/css/airplane_mode.css"
# web_include_css = "/assets/airplane_mode/css/web.css"
```

## 🔄 Testing Different Scenarios

### **Test 1: Direct Asset Access**
```bash
# Test direct file access
wget https://your-site.com/assets/airplane_mode/css/web.css
wget https://your-site.com/assets/airplane_mode/js/airplane_mode.js
```

### **Test 2: Browser Console**
1. Open Developer Tools → Network tab
2. Clear cache and hard reload (Ctrl+Shift+R)
3. Check each asset's status code and Content-Type
4. Look for proper `200 OK` responses

### **Test 3: Route Testing**
```bash
# Test each website route
curl -L https://your-site.com/shop-availability
curl -L https://your-site.com/shop-portal
curl -L https://your-site.com/apply-shop
```

## 📞 Getting Help

### **If Issues Persist:**

1. **Check Logs**:
```bash
bench logs
tail -f sites/your-site/logs/web.log
```

2. **Debug Mode**:
```bash
# Enable debug mode
bench set-config developer_mode 1 --site your-site
bench restart
```

3. **Create Support Ticket** with:
   - Complete error messages
   - Browser console screenshots
   - Network tab screenshots
   - Output of `bench build --app airplane_mode --verbose`

## 🎯 Prevention

### **Regular Maintenance:**
```bash
# Weekly asset maintenance
bench clear-cache
bench build --app airplane_mode
bench restart

# Monthly checks
bench --site your-site console
```

```python
# In console - verify assets
import frappe
print("App installed:", "airplane_mode" in frappe.get_installed_apps())
```

## 📝 File Structure Reference

```
airplane_mode/
├── public/
│   ├── .htaccess              # Apache MIME fix
│   ├── css/
│   │   ├── airplane_mode.css  # App styles
│   │   └── web.css           # Website styles ✅ FIXED
│   ├── js/
│   │   ├── airplane_mode.js   # Main JavaScript ✅ EXISTS
│   │   └── airplane_dashboard.js
│   └── images/               # ✅ CREATED
│       ├── favicon.svg       # ✅ ADDED
│       ├── logo.svg          # ✅ ADDED
│       └── splash.svg        # ✅ ADDED
├── www/
│   ├── shop-availability.html # ✅ EXISTS
│   ├── shop-availability.py   # ✅ EXISTS
│   └── [other web pages]
└── config/
    └── nginx.conf            # Nginx MIME fix
```

## 🎉 Success Indicators

Your installation is working correctly when:

1. **No 404 errors** in browser console
2. **Proper MIME types**: 
   - CSS files: `text/css`
   - JS files: `application/javascript`
   - SVG files: `image/svg+xml`
3. **All routes accessible** without errors
4. **Website styling** loads properly
5. **JavaScript functionality** works

---

**Quick Fix Command Summary:**
```bash
chmod +x create_missing_assets.sh fix_mime_types.sh
./create_missing_assets.sh
bench clear-cache && bench build --app airplane_mode --force && bench restart
./fix_mime_types.sh
```

This comprehensive fix addresses all asset loading, MIME type, and routing issues in your Airplane Mode application.
