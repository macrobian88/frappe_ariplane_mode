#!/usr/bin/env python3
"""
Frappe Hooks Validator for Airport Management System

This script validates the hooks.py file for common issues that cause installation errors,
particularly the "'dict' object has no attribute 'extend'" error.

Usage:
    python validate_hooks.py [path_to_hooks.py]

If no path is provided, it will look for airplane_mode/hooks.py in the current directory.
"""

import os
import sys
import importlib.util
import inspect


def validate_hooks(hooks_path="airplane_mode/hooks.py"):
    """Validate hooks.py file for common configuration issues."""
    
    if not os.path.exists(hooks_path):
        print(f"❌ Error: hooks.py not found at {hooks_path}")
        return False
    
    print(f"🔍 Validating hooks file: {hooks_path}")
    print("="*60)
    
    # Load the hooks module
    spec = importlib.util.spec_from_file_location("hooks", hooks_path)
    hooks_module = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(hooks_module)
    except Exception as e:
        print(f"❌ Error loading hooks.py: {e}")
        return False
    
    # Define hooks that should be lists
    list_hooks = {
        'required_apps',
        'website_generators', 
        'clear_cache',
        'boot_session',
        'before_request',
        'after_request',
        'before_job',
        'after_job',
        'auth_hooks',
        'standard_doctypes',
        'auto_cancel_exempted_doctypes',
        'ignore_links_on_delete',
        'user_data_fields',
        'global_search_doctypes',
        'add_to_apps_screen',
        'standard_email_templates',
        'auto_email_reports',
        'dashboard_charts',
        'desk_pages',
        'standard_portal_menu_items',
        'onboard_steps',
        'fixtures'
    }
    
    # Define hooks that should be dicts
    dict_hooks = {
        'doc_events',
        'scheduler_events',
        'jinja',
        'role_home_page',
        'webform_include_js',
        'webform_include_css',
        'page_js',
        'doctype_js',
        'doctype_list_js',
        'doctype_tree_js',
        'doctype_calendar_js',
        'permission_query_conditions',
        'has_permission',
        'override_doctype_class',
        'override_whitelisted_methods',
        'override_doctype_dashboards',
        'default_log_clearing_doctypes',
        'job_events',
        'website_context',
        'error_page_templates',
        'override_standard_pages'
    }
    
    # Special hooks that should be list of dicts
    list_of_dicts_hooks = {
        'website_route_rules'
    }
    
    issues_found = []
    warnings = []
    
    # Check all attributes in the hooks module
    for attr_name in dir(hooks_module):
        if attr_name.startswith('_'):
            continue
            
        attr_value = getattr(hooks_module, attr_name)
        
        # Skip functions and modules
        if inspect.isfunction(attr_value) or inspect.ismodule(attr_value):
            continue
        
        # Check list hooks
        if attr_name in list_hooks:
            if not isinstance(attr_value, list):
                issues_found.append(f"❌ {attr_name} should be a list, but is {type(attr_value).__name__}")
            else:
                print(f"✅ {attr_name} is correctly defined as list")
        
        # Check dict hooks  
        elif attr_name in dict_hooks:
            if not isinstance(attr_value, dict):
                issues_found.append(f"❌ {attr_name} should be a dict, but is {type(attr_value).__name__}")
            else:
                print(f"✅ {attr_name} is correctly defined as dict")
        
        # Check list of dicts hooks
        elif attr_name in list_of_dicts_hooks:
            if not isinstance(attr_value, list):
                issues_found.append(f"❌ {attr_name} should be a list, but is {type(attr_value).__name__}")
            elif attr_value and not all(isinstance(item, dict) for item in attr_value):
                issues_found.append(f"❌ {attr_name} should be a list of dicts")
            else:
                print(f"✅ {attr_name} is correctly defined as list of dicts")
    
    # Check for required_apps specifically
    if hasattr(hooks_module, 'required_apps'):
        if isinstance(hooks_module.required_apps, list):
            if "erpnext" in hooks_module.required_apps:
                warnings.append(f"⚠️  required_apps includes 'erpnext' - this may cause installation issues on sites without ERPNext")
            print(f"✅ required_apps is properly defined as list: {hooks_module.required_apps}")
        else:
            issues_found.append(f"❌ required_apps is not a list: {type(hooks_module.required_apps)}")
    else:
        issues_found.append("❌ required_apps is not defined (this can cause installation issues)")
    
    # Check specific Airport Management System hooks
    if hasattr(hooks_module, 'boot_session'):
        if isinstance(hooks_module.boot_session, str):
            issues_found.append(f"❌ boot_session should be a list, not string: {hooks_module.boot_session}")
        elif isinstance(hooks_module.boot_session, list):
            print(f"✅ boot_session is correctly defined as list")
    
    # Print results
    print("\n" + "="*60)
    print("🔧 AIRPORT MANAGEMENT SYSTEM - VALIDATION RESULTS")
    print("="*60)
    
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
        print()
    
    if issues_found:
        print("❌ VALIDATION FAILED")
        print("\nIssues found:")
        for issue in issues_found:
            print(f"  {issue}")
        print("\nTo fix these issues:")
        print("1. Ensure hooks expecting lists are defined as lists: []")
        print("2. Ensure hooks expecting dicts are defined as dicts: {}")
        print("3. Consider removing 'erpnext' from required_apps for standalone installation")
        print("4. Check the fixed version at: https://github.com/macrobian88/frappe_ariplane_mode")
        return False
    else:
        print("✅ VALIDATION PASSED")
        print("All hooks are properly configured!")
        if warnings:
            print("\nNote: There are some warnings above that you may want to review.")
        return True


def main():
    """Main function to run the validator."""
    hooks_path = sys.argv[1] if len(sys.argv) > 1 else "airplane_mode/hooks.py"
    
    print("🔧 Airport Management System - Hooks Validator")
    print("🛫 Frappe Airplane Mode Application")
    print("="*60)
    
    success = validate_hooks(hooks_path)
    
    if success:
        print("\n🎉 Your Airport Management System is ready for installation!")
        print("📦 Install with: bench get-app https://github.com/macrobian88/frappe_ariplane_mode.git")
    else:
        print("\n🚨 Please fix the issues above before installing the app.")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
