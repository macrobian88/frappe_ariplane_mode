app_name = "airplane_mode"
app_title = "Airport Management System"
app_publisher = "nandhakishore"
app_description = "Comprehensive Airport Management System with Flight Operations, Shop Management, and Rent Collection"
app_email = "nandhakishore2165@gmail.com"
app_license = "mit"

# Required Apps - Set to minimal dependencies for broader compatibility
# Remove ERPNext dependency to allow standalone installation
# Add it back if specifically needed: required_apps = ["frappe", "erpnext"]
required_apps = ["frappe"]

# Apps - Apps screen configuration
add_to_apps_screen = [
    {
        "name": "airplane_mode",
        "logo": "/assets/airplane_mode/logo.png",
        "title": "Airport Management",
        "route": "/airplane_mode",
        "has_permission": "airplane_mode.api.permission.has_app_permission"
    }
]

# Includes in <head>
app_include_css = "/assets/airplane_mode/css/airplane_mode.css"
app_include_js = "/assets/airplane_mode/js/airplane_mode.js"
web_include_css = "/assets/airplane_mode/css/web.css"
web_include_js = "/assets/airplane_mode/js/web.js"

# include js in doctype views
doctype_js = {
    "Airplane Flight": "public/js/airplane_flight.js",
    "Airport Shop": "public/js/airport_shop.js",
    "Contract Shop": "public/js/contract_shop.js",
    "Shop Lead": "public/js/shop_lead.js"
}

# Document Events
doc_events = {
    "Airplane Flight": {
        "on_update": "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.sync_gate_to_tickets"
    },
    "Contract Shop": {
        "on_submit": "airplane_mode.airplane_mode.doctype.contract_shop.contract_shop.create_invoice",
        "validate": "airplane_mode.airplane_mode.doctype.contract_shop.contract_shop.validate_contract"
    },
    "Sales Invoice": {
        "on_update": "airplane_mode.airplane_mode.doctype.contract_shop.contract_shop.update_contract_payment_status"
    },
    "Payment Entry": {
        "on_submit": "airplane_mode.airplane_mode.doctype.contract_shop.contract_shop.update_contract_payment_status"
    },
    "Shop Lead": {
        "after_insert": "airplane_mode.airport_shop_management.lead_notifications.send_lead_notifications"
    }
}

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "airplane_mode.airport_shop_management.rent_reminder.send_rent_reminders",
        "airplane_mode.airport_shop_management.rent_collection.process_monthly_invoices"
    ],
    "weekly": [
        "airplane_mode.airplane_mode.report_automation.send_weekly_reports"
    ],
    "monthly": [
        "airplane_mode.airport_shop_management.analytics.update_monthly_metrics"
    ]
}

# Website Routes
website_route_rules = [
    {"from_route": "/shop-portal", "to_route": "Airport Shop Portal"},
    {"from_route": "/shop-availability", "to_route": "Shop Availability"},
    {"from_route": "/apply-shop", "to_route": "Shop Application"}
]

# Fixtures
fixtures = [
    {
        "dt": "Shop Type",
        "filters": [["shop_type_name", "in", ["Stall", "Walk-through", "Normal", "Food Court", "Duty Free"]]]
    },
    {
        "dt": "Airport",
        "filters": [["name", "in", ["Bangalore International Airport", "Chennai International Airport"]]]
    }
]

# Permissions
permission_query_conditions = {
    "Airport Shop": "airplane_mode.airplane_mode.doctype.airport_shop.airport_shop.get_permission_query_conditions",
    "Contract Shop": "airplane_mode.airplane_mode.doctype.contract_shop.contract_shop.get_permission_query_conditions"
}

has_permission = {
    "Airport Shop": "airplane_mode.airplane_mode.doctype.airport_shop.airport_shop.has_permission",
    "Contract Shop": "airplane_mode.airplane_mode.doctype.contract_shop.contract_shop.has_permission"
}

# Jinja Methods
jinja = {
    "methods": "airplane_mode.utils.jinja_methods",
    "filters": "airplane_mode.utils.jinja_filters"
}

# Background Jobs - FIXED: These should be lists, not single strings
job_events = {
    "before_job": ["airplane_mode.utils.before_job"],
    "after_job": ["airplane_mode.utils.after_job"]
}

# Boot Session - FIXED: Should be list, not single string
boot_session = ["airplane_mode.utils.boot_session"]

# User Data Protection
user_data_fields = [
    {
        "doctype": "Shop Lead",
        "filter_by": "email",
        "redact_fields": ["lead_name", "phone", "email"],
        "partial": 1,
    }
]

# Export Python Type Annotations
export_python_type_annotations = True

# Default Log Clearing
default_log_clearing_doctypes = {
    "Shop Lead": 90,  # 3 months
    "Contract Shop": 365  # 1 year
}

# Website Theme
website_theme_scss = "airplane_mode/public/scss/website"

# Error Pages
error_page_templates = {
    "404": "templates/pages/404.html",
    "500": "templates/pages/500.html"
}

# Email Templates
standard_email_templates = [
    {
        "name": "Shop Lead Welcome",
        "subject": "Thank you for your interest in our Airport Shops",
        "response": "airplane_mode/templates/emails/shop_lead_welcome.html"
    },
    {
        "name": "Rent Reminder",
        "subject": "Monthly Rent Due Reminder",
        "response": "airplane_mode/templates/emails/rent_reminder.html"
    },
    {
        "name": "Contract Renewal",
        "subject": "Shop Contract Renewal Notice",
        "response": "airplane_mode/templates/emails/contract_renewal.html"
    }
]

# Website Context
website_context = {
    "favicon": "/assets/airplane_mode/images/favicon.ico",
    "splash_image": "/assets/airplane_mode/images/splash.png"
}

# Auto Email Reports
auto_email_reports = [
    {
        "report": "Shop Occupancy Report",
        "email_to": ["admin@airport.com"],
        "frequency": "Weekly",
        "format": "PDF"
    },
    {
        "report": "Revenue Analytics",
        "email_to": ["finance@airport.com"],
        "frequency": "Monthly", 
        "format": "Excel"
    }
]

# Notification Config
notification_config = "airplane_mode.notifications.get_notification_config"

# Override Standard Pages
override_standard_pages = {
    "home": "airplane_mode.www.index"
}

# Custom Authentication - FIXED: Should be list
auth_hooks = [
    "airplane_mode.auth.validate_user_permissions"
]

# Global Search - FIXED: Should be list
global_search_doctypes = ["Airport Shop", "Shop Lead", "Contract Shop"]

# Dashboard Charts
dashboard_charts = [
    {
        "chart_name": "Shop Occupancy",
        "chart_type": "donut",
        "timeseries": 0,
        "based_on": "shop_type",
        "value_based_on": "count"
    },
    {
        "chart_name": "Monthly Revenue",
        "chart_type": "line", 
        "timeseries": 1,
        "based_on": "posting_date",
        "value_based_on": "grand_total"
    }
]

# Desk Page
desk_pages = [
    {
        "module": "Airport Shop Management",
        "category": "Places",
        "label": "Shop Portal",
        "route": "/shop-portal"
    }
]

# Standard Portal Doctypes
standard_portal_menu_items = [
    {"title": "Shop Applications", "route": "/shop-applications", "reference_doctype": "Shop Lead", "role": "Customer"},
    {"title": "My Contracts", "route": "/my-contracts", "reference_doctype": "Contract Shop", "role": "Customer"},
    {"title": "Invoices", "route": "/invoices", "reference_doctype": "Sales Invoice", "role": "Customer"}
]

# OnBoard Steps
onboard_steps = [
    {
        "step": "Create Shop Types",
        "description": "Set up different categories of shops in your airport",
        "action": "Create Shop Type",
        "action_label": "Create Shop Type"
    },
    {
        "step": "Add Airport Shops", 
        "description": "Register available shops for lease",
        "action": "Create Airport Shop",
        "action_label": "Add Shop"
    },
    {
        "step": "Configure Email Settings",
        "description": "Set up email notifications for leads and contracts",
        "action": "Setup Email",
        "action_label": "Configure Email"
    }
]

# CRITICAL FIX: Explicitly prevent problematic hooks that cause extend() errors
# These hooks are often the source of 'dict' object has no attribute 'extend' errors

# Standard DocTypes - FIXED: Ensure this is never defined as dict
# The error traceback shows ['Airport Shop', 'Shop Lead', 'Contract Shop'] causing issues
# We explicitly avoid defining this hook to prevent the error

# Clear cache hooks (must be list if defined)
# clear_cache = []

# Website generators (must be list if defined)  
# website_generators = []

# Standard doctypes (CRITICAL: This hook was causing the extend() error)
# DO NOT UNCOMMENT THE FOLLOWING LINE - it causes installation failure:
# standard_doctypes = ["Airport Shop", "Shop Lead", "Contract Shop"]

# Request/Response hooks (must be lists if defined)
# before_request = []
# after_request = []

# Installation hooks (single strings, not lists)
# before_install = "airplane_mode.install.before_install"
# after_install = "airplane_mode.install.after_install"

# Website context processors (must be list if defined)
# website_context_processors = []

# Boot session data (already fixed above as list)
# Additional boot data (must be list if defined)
# boot_info = []

# Migration hooks (must be list if defined)
# before_migrate = []
# after_migrate = []

# IMPORTANT NOTES:
# 1. This hooks.py file has been specifically fixed to resolve the extend() error
# 2. The problematic hook was likely 'standard_doctypes' with value ['Airport Shop', 'Shop Lead', 'Contract Shop']
# 3. All list hooks are properly configured as lists []
# 4. All dict hooks are properly configured as dicts {}
# 5. Problematic hooks are commented out to prevent errors
# 6. Made required_apps compatible (removed erpnext dependency for standalone install)
# 7. Fixed boot_session to be a list instead of string
# 8. Ensured auth_hooks is properly defined as list
# 9. Fixed global_search_doctypes to be a list
# 10. Added extensive documentation for troubleshooting

# For debugging: If you still get extend() errors, check these common issues:
# - Ensure no hooks are defined as single strings when they should be lists
# - Check that no hooks are accidentally defined as dicts when they should be lists
# - Verify that all list hooks use [] syntax, not {} syntax
# - Look for any dynamically added hooks in other Python files
