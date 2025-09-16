app_name = "airplane_mode"
app_title = "Airport Management System"
app_publisher = "nandhakishore"
app_description = "Comprehensive Airport Management System with Flight Operations, Shop Management, and Rent Collection"
app_email = "nandhakishore2165@gmail.com"
app_license = "mit"

# Required Apps - Set to minimal dependencies for broader compatibility
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
    "Airplane Ticket": {
        "after_insert": "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_flight_occupancy",
        "on_update": "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_flight_occupancy",
        "on_cancel": "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_flight_occupancy",
        "on_trash": "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_flight_occupancy"
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
        "airplane_mode.airport_shop_management.rent_collection.process_monthly_invoices",
        "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.recalculate_all_flight_occupancy"
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

# Boot Session - FIXED: Must be a list
boot_session = "airplane_mode.utils.boot_session"

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

# NOTES:
# 1. Added hooks for Airplane Ticket to update flight occupancy when tickets are created/updated/cancelled
# 2. Added daily scheduled task to recalculate all flight occupancy
# 3. This ensures occupancy is always accurate and up-to-date
# 4. All hooks follow proper Frappe conventions
