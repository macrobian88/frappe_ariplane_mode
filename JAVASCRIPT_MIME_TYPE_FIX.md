# JavaScript MIME Type Error Fix

## Problem
You may encounter this error in the browser console:
```
Refused to execute script from 'https://airplane-mode.m.frappe.cloud/assets/airplane_mode/js/airplane_mode.js' because its MIME type ('text/html') is not executable, and strict MIME type checking is enabled.
```

## Root Cause
This error occurs when JavaScript files are being served with incorrect MIME type (`text/html` instead of `application/javascript`). This typically happens due to:

1. **Missing or incorrect web server configuration**
2. **File not found (404 error served as HTML)**
3. **Asset build issues**
4. **CDN or proxy misconfiguration**

## Solutions

### 1. Immediate Fix - Clear Assets and Rebuild

```bash
# Navigate to your frappe-bench directory
cd /path/to/frappe-bench

# Clear existing assets
bench clear-cache
bench clear-website-cache

# Rebuild assets
bench build --app airplane_mode

# Restart services
bench restart
```

### 2. For Apache Servers (.htaccess)
The repository now includes `/airplane_mode/public/.htaccess` file that:
- Forces correct MIME type for `.js` files
- Sets proper Content-Type headers
- Enables compression and caching

### 3. For Nginx Servers
Use the configuration in `/airplane_mode/config/nginx.conf`:

```nginx
# Add to your nginx site configuration
location /assets/airplane_mode/ {
    alias /path/to/frappe-bench/sites/assets/airplane_mode/;
    
    location ~* \.js$ {
        add_header Content-Type "application/javascript; charset=utf-8";
        expires 1M;
        add_header Cache-Control "public, immutable";
    }
    
    location ~* \.css$ {
        add_header Content-Type "text/css; charset=utf-8";
        expires 1M;
        add_header Cache-Control "public, immutable";
    }
}
```

### 4. Frappe Cloud Solution
If you're using Frappe Cloud:

1. **Contact Support**: Create a support ticket mentioning the MIME type issue
2. **Temporary Workaround**: 
   ```bash
   # In your app's hooks.py, ensure JavaScript files are properly listed
   app_include_js = [
       "/assets/airplane_mode/js/airplane_mode.js",
       "/assets/airplane_mode/js/airplane_dashboard.js"
   ]
   ```

### 5. Manual File Check
Verify the JavaScript file exists and is accessible:

```bash
# Check if file exists in assets
ls -la sites/assets/airplane_mode/js/

# If missing, rebuild assets
bench build --app airplane_mode --force
```

### 6. Development Environment Fix
For local development:

```bash
# Enable developer mode
bench set-config developer_mode 1

# Force rebuild
bench build --app airplane_mode --force

# Clear all caches
bench clear-cache
bench clear-website-cache

# Restart
bench restart
```

### 7. Custom App Build Hook
Add to your `airplane_mode/hooks.py`:

```python
# Build configuration
build_include_js = [
    "airplane_mode/public/js/airplane_mode.js",
    "airplane_mode/public/js/airplane_dashboard.js"
]

# Ensure proper asset serving
app_include_js = [
    "/assets/airplane_mode/js/airplane_mode.js",
    "/assets/airplane_mode/js/airplane_dashboard.js"
]
```

## Verification Steps

### 1. Check Browser Network Tab
1. Open Developer Tools → Network tab
2. Reload the page
3. Look for the JavaScript file request
4. Check the Response Headers for `Content-Type`

### 2. Direct File Access
Test direct access to the JavaScript file:
```
https://your-site.com/assets/airplane_mode/js/airplane_mode.js
```

The response should have:
- Status: `200 OK`
- Content-Type: `application/javascript` or `text/javascript`

### 3. Command Line Test
```bash
curl -I https://your-site.com/assets/airplane_mode/js/airplane_mode.js
```

Look for: `Content-Type: application/javascript`

## Prevention

### 1. Proper Asset Management
- Always run `bench build` after JavaScript changes
- Use `bench build --force` for complete rebuild
- Clear caches regularly in development

### 2. Server Configuration
- Maintain proper MIME type configurations
- Regular server configuration updates
- Monitor asset serving logs

### 3. Development Best Practices
```bash
# Development workflow
bench build --app airplane_mode
bench clear-cache
bench restart
```

## Common Mistakes to Avoid

1. **Skipping asset build** after JavaScript changes
2. **Cache issues** - not clearing caches properly
3. **File permissions** - incorrect permissions on static files
4. **Path issues** - incorrect paths in hooks.py
5. **Server misconfiguration** - missing MIME type settings

## Emergency Workaround

If the issue persists, temporarily inline the JavaScript in your templates:

```html
<!-- In your template file -->
<script type="text/javascript">
// Include the JavaScript code directly here
// This is a temporary solution only
</script>
```

## Getting Help

If none of these solutions work:

1. **Check Frappe logs**: `bench logs`
2. **Browser console**: Look for additional error messages  
3. **Network tab**: Analyze the failed request details
4. **Contact support**: Provide error logs and configuration details

## File Structure Reference
```
airplane_mode/
├── public/
│   ├── .htaccess          # Apache MIME type fix
│   ├── js/
│   │   ├── airplane_mode.js      # Main JavaScript file
│   │   └── airplane_dashboard.js # Dashboard JavaScript
│   └── css/
└── config/
    └── nginx.conf         # Nginx configuration
```

This fix ensures that JavaScript files are served with the correct MIME type, resolving the browser security error and allowing your app to function properly.
