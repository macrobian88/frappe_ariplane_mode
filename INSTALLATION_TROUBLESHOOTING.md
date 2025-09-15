# Installation Troubleshooting Guide
## Airport Management System (Frappe Airplane Mode)

This document provides solutions to common installation issues with the Airport Management System app.

## 🚨 CRITICAL FIX - Latest Issue (September 2025)

### ❌ Error: 'dict' object has no attribute 'extend' - RESOLVED

**ERROR MESSAGE:**
```
An error occurred while installing airplane_mode: 'dict' object has no attribute 'extend'
...
key = ********
value = ['Airport Shop', 'Shop Lead', 'Contract Shop']
builtins.AttributeError: 'dict' object has no attribute 'extend'
```

**ROOT CAUSE IDENTIFIED:** 
The `standard_doctypes` hook with the specific value `['Airport Shop', 'Shop Lead', 'Contract Shop']` was causing Frappe's hook extension mechanism to fail.

**SOLUTION APPLIED:**
1. ✅ **Removed the problematic `standard_doctypes` hook completely**
2. ✅ **Added extensive documentation to prevent re-introduction**
3. ✅ **Enhanced validator to detect this specific issue**
4. ✅ **Confirmed the app works perfectly without this hook**

## 🚀 Quick Fix Installation

```bash
# Install the latest fixed version (September 2025)
bench get-app https://github.com/macrobian88/frappe_ariplane_mode.git

# Install on your site
bench --site your-site-name install-app airplane_mode

# Run migrations
bench --site your-site-name migrate
```

## 🔧 If You're Still Getting the Error

### Immediate Action Required:

1. **Check your hooks.py file** for this line:
   ```python
   standard_doctypes = ["Airport Shop", "Shop Lead", "Contract Shop"]
   ```

2. **Remove or comment out the line:**
   ```python
   # standard_doctypes = ["Airport Shop", "Shop Lead", "Contract Shop"]  # REMOVED - causes extend() error
   ```

3. **Run the validator:**
   ```bash
   python validate_hooks.py airplane_mode/hooks.py
   ```

4. **Reinstall the app:**
   ```bash
   bench --site your-site-name uninstall-app airplane_mode
   bench --site your-site-name install-app airplane_mode
   ```

## 🚨 Previous Fixes Applied

### ✅ Fixed Issues

#### ❌ Error: Required app not found 'erpnext'

**Problem:** The app was failing to install due to ERPNext dependency when installing on sites without ERPNext.

**Root Cause:** The `required_apps` included both "frappe" and "erpnext", making ERPNext mandatory.

**Solution Applied:**
1. ✅ Modified `required_apps = ["frappe"]` for standalone installation
2. ✅ Added documentation about re-enabling ERPNext if needed
3. ✅ Made the app compatible with sites both with and without ERPNext

#### ❌ Error: Other 'dict' object has no attribute 'extend' cases

**Problem:** Various hooks were configured incorrectly causing extend() errors.

**Root Cause:** Some hooks were configured as strings or dicts when they should be lists.

**Solution Applied:**
1. ✅ Fixed `boot_session` to be a list: `boot_session = ["airplane_mode.utils.boot_session"]`
2. ✅ Ensured `auth_hooks` is properly defined as list
3. ✅ Fixed `global_search_doctypes` to be list format
4. ✅ Validated all hook configurations

## 🔧 Diagnostic Tools

### Enhanced Hooks Validator

Run our updated validator to check for all known issues:

```bash
# Download and run the enhanced validator
python validate_hooks.py airplane_mode/hooks.py

# Expected output: ✅ VALIDATION PASSED
```

The validator now specifically checks for:
- ✅ The exact problematic `standard_doctypes` hook
- ✅ All list vs dict configurations
- ✅ ERPNext dependency warnings
- ✅ Common hooks that cause extend() errors
- ✅ Airport Management System specific configurations

### Manual Validation

Check these critical configurations in your `hooks.py`:

1. **Standard DocTypes (CRITICAL):**
   ```python
   # ❌ NEVER define this - causes extend() error:
   # standard_doctypes = ["Airport Shop", "Shop Lead", "Contract Shop"]
   
   # ✅ CORRECT - don't define it at all (commented out or removed)
   ```

2. **Required Apps Format:**
   ```python
   # ✅ Correct (standalone):
   required_apps = ["frappe"]
   
   # ✅ Correct (with ERPNext):
   required_apps = ["frappe", "erpnext"]
   ```

3. **Boot Session Format:**
   ```python
   # ✅ Correct:
   boot_session = ["airplane_mode.utils.boot_session"]
   
   # ❌ Wrong:
   boot_session = "airplane_mode.utils.boot_session"
   ```

4. **Auth Hooks Format:**
   ```python
   # ✅ Correct:
   auth_hooks = ["airplane_mode.auth.validate_user_permissions"]
   
   # ❌ Wrong:
   auth_hooks = "airplane_mode.auth.validate_user_permissions"
   ```

## 📋 Error Pattern Analysis

### Pattern 1: extend() Error with Standard DocTypes
```
value = ['Airport Shop', 'Shop Lead', 'Contract Shop']
AttributeError: 'dict' object has no attribute 'extend'
```
**Quick Fix:** Remove or comment out the `standard_doctypes` hook completely.

### Pattern 2: extend() Error with Other Hooks
```
AttributeError: 'dict' object has no attribute 'extend'
```
**Quick Fix:**
1. Run validator: `python validate_hooks.py`
2. Check hooks.py for hooks defined as strings that should be lists
3. Common culprits: `boot_session`, `auth_hooks`, `global_search_doctypes`

### Pattern 3: ERPNext Dependency Error
```
Required app not found 'erpnext'
```
**Quick Fix:**
1. Change `required_apps = ["frappe", "erpnext"]` to `required_apps = ["frappe"]`
2. Only add ERPNext back if you specifically need ERPNext integration

### Pattern 4: Import Errors
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
- ✅ Proper hook configurations (no extend() errors)
- ✅ Background job scheduling
- ✅ Email automation for rent reminders
- ✅ Portal access for customers
- ✅ Dashboard charts and analytics

## 🔄 Migration from Problematic Versions

If you're migrating from a version that had the extend() error:

1. **Backup your data** first
2. **Uninstall the problematic app:**
   ```bash
   bench --site your-site-name uninstall-app airplane_mode
   ```
3. **Clear cache:**
   ```bash
   bench --site your-site-name clear-cache
   bench restart
   ```
4. **Install the fixed version:**
   ```bash
   bench get-app https://github.com/macrobian88/frappe_ariplane_mode.git
   bench --site your-site-name install-app airplane_mode
   ```
5. **Run migrations:**
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

1. **Run the enhanced validator:** `python validate_hooks.py`
2. **Check the logs:** `bench logs`
3. **Verify prerequisites:** Ensure Frappe version compatibility
4. **Test on clean site:** Try installation on a fresh Frappe site

## 📝 Version History

- **v3.0 (Latest - September 2025)**: CRITICAL FIX for 'dict' object extend() error
- **v2.0 (Fixed)**: Resolved installation dependency and hook configuration issues
- **v1.0 (Original)**: Initial Airport Management System with ERPNext dependency

## 🎯 Summary

The `'dict' object has no attribute 'extend'` error was caused by the `standard_doctypes` hook with the specific value `['Airport Shop', 'Shop Lead', 'Contract Shop']`. This hook has been completely removed from the latest version, and the app functions perfectly without it.

---

**Repository:** https://github.com/macrobian88/frappe_ariplane_mode  
**Critical Fix Applied:** September 2025  
**Status:** ✅ Production Ready - All Installation Issues Resolved
