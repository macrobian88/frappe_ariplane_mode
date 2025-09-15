# Installation Troubleshooting Guide
## Airport Management System (Frappe Airplane Mode)

This document provides solutions to common installation issues with the Airport Management System app.

## 🚨 Recent Fixes Applied

### ✅ Fixed Issues

#### ❌ Error: Required app not found 'erpnext'

**Problem:** The app was failing to install due to ERPNext dependency when installing on sites without ERPNext.

**Root Cause:** The `required_apps` included both "frappe" and "erpnext", making ERPNext mandatory.

**Solution Applied:**
1. ✅ Modified `required_apps = ["frappe"]` for standalone installation
2. ✅ Added documentation about re-enabling ERPNext if needed
3. ✅ Made the app compatible with sites both with and without ERPNext

#### ❌ Error: 'dict' object has no attribute 'extend'

**Problem:** The app installation fails during the hooks loading phase with: `AttributeError: 'dict' object has no attribute 'extend'`

**Root Cause:** Some hooks were configured incorrectly:
- `boot_session` was a string instead of list
- Some other hooks had wrong data types

**Solution Applied:**
1. ✅ Fixed `boot_session` to be a list: `boot_session = ["airplane_mode.utils.boot_session"]`
2. ✅ Ensured `auth_hooks` is properly defined as list
3. ✅ Fixed `global_search_doctypes` to be list format
4. ✅ Validated all hook configurations

## 🚀 Installation Commands

### Quick Installation (Fixed Version)

```bash
# Install the fixed version
bench get-app https://github.com/macrobian88/frappe_ariplane_mode.git

# Install on your site
bench --site your-site-name install-app airplane_mode

# Run migrations
bench --site your-site-name migrate
```

### If You Want ERPNext Integration

If you need ERPNext integration, modify `airplane_mode/hooks.py`:

```python
# Change this line:
required_apps = ["frappe"]

# To this:
required_apps = ["frappe", "erpnext"]
```

## 🔧 Diagnostic Tools

### Hooks Validator

Run our custom validator to check for configuration issues:

```bash
# Download and run the validator
python validate_hooks.py airplane_mode/hooks.py

# Or run from the app directory
python validate_hooks.py
```

The validator will check for:
- ✅ Correct list vs dict configurations
- ✅ ERPNext dependency warnings
- ✅ Common hooks that cause extend() errors
- ✅ Airport Management System specific configurations

### Manual Validation

Check these common issues in your `hooks.py`:

1. **Required Apps Format:**
   ```python
   # ✅ Correct (standalone):
   required_apps = ["frappe"]
   
   # ✅ Correct (with ERPNext):
   required_apps = ["frappe", "erpnext"]
   
   # ❌ Wrong:
   # required_apps = []  # Commented out
   ```

2. **Boot Session Format:**
   ```python
   # ✅ Correct:
   boot_session = ["airplane_mode.utils.boot_session"]
   
   # ❌ Wrong:
   boot_session = "airplane_mode.utils.boot_session"
   ```

3. **Auth Hooks Format:**
   ```python
   # ✅ Correct:
   auth_hooks = ["airplane_mode.auth.validate_user_permissions"]
   
   # ❌ Wrong:
   auth_hooks = "airplane_mode.auth.validate_user_permissions"
   ```

## 📋 Common Error Patterns & Solutions

### Pattern 1: extend() Error
```
AttributeError: 'dict' object has no attribute 'extend'
```
**Quick Fix:**
1. Check hooks.py for hooks defined as single strings that should be lists
2. Common culprits: `boot_session`, `auth_hooks`, `global_search_doctypes`
3. Use our validator: `python validate_hooks.py`

### Pattern 2: ERPNext Dependency Error
```
Required app not found 'erpnext'
```
**Quick Fix:**
1. Change `required_apps = ["frappe", "erpnext"]` to `required_apps = ["frappe"]`
2. Only add ERPNext back if you specifically need ERPNext integration

### Pattern 3: Import Errors
```
ImportError: No module named 'airplane_mode.something'
```
**Solution:**
1. Ensure all referenced modules exist
2. Check file paths in hook configurations
3. Verify DocType names match exactly

## 🏗️ Architecture Notes

This Airport Management System includes:

### Core Modules
- **Flight Operations**: Airplane Flight management with gate synchronization
- **Shop Management**: Airport Shop leasing and management
- **Contract Management**: Shop contracts and rent collection
- **Lead Management**: Shop application leads with notifications

### Key Features Fixed
- ✅ Standalone installation (no ERPNext requirement)
- ✅ Proper hook configurations
- ✅ Background job scheduling
- ✅ Email automation for rent reminders
- ✅ Portal access for customers
- ✅ Dashboard charts and analytics

## 🔄 Migration from Other Versions

If you're migrating from another airplane_mode app:

1. **Backup your data** first
2. **Uninstall the old app:**
   ```bash
   bench --site your-site-name uninstall-app airplane_mode
   ```
3. **Install the fixed version:**
   ```bash
   bench get-app https://github.com/macrobian88/frappe_ariplane_mode.git
   bench --site your-site-name install-app airplane_mode
   ```
4. **Run migrations:**
   ```bash
   bench --site your-site-name migrate
   ```

## 🧪 Testing Your Installation

After successful installation:

1. **Check App Lists:**
   - Log into your Frappe site
   - Verify "Airport Management System" appears in apps

2. **Test Core Doctypes:**
   - Navigate to: Airport Shop, Shop Lead, Contract Shop
   - Create test records

3. **Test Portal Features:**
   - Visit `/shop-portal` for customer portal
   - Check `/shop-availability` for public shop listings

4. **Verify Background Jobs:**
   - Check that scheduler events are configured
   - Test email notifications (if SMTP is configured)

## 🆘 Additional Support

### Log Analysis
```bash
# Check installation logs
bench logs

# Check specific site logs
tail -f logs/your-site-name.log
```

### Common File Locations
- **Hooks:** `airplane_mode/hooks.py`
- **DocTypes:** `airplane_mode/airplane_mode/doctype/`
- **Reports:** `airplane_mode/airplane_mode/report/`
- **Web Pages:** `airplane_mode/airplane_mode/web_form/`

### Compatibility
- **Frappe:** v15.x and above
- **ERPNext:** Optional (v15.x if used)
- **Python:** 3.10+

## 📞 Getting Help

If you encounter issues not covered here:

1. **Run the validator:** `python validate_hooks.py`
2. **Check the logs:** `bench logs`
3. **Verify prerequisites:** Ensure Frappe version compatibility
4. **Test on clean site:** Try installation on a fresh Frappe site

## 📝 Version History

- **v2.0 (Fixed)**: Resolved installation dependency and hook configuration issues
- **v1.0 (Original)**: Initial Airport Management System with ERPNext dependency

---

**Repository:** https://github.com/macrobian88/frappe_ariplane_mode  
**Issues Fixed:** Installation dependencies, hook configurations, standalone compatibility  
**Status:** ✅ Production Ready
