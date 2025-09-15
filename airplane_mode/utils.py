import frappe
from frappe import _
from frappe.utils import get_site_url, get_datetime, getdate, format_datetime
from frappe.utils.password import get_decrypted_password


def boot_session(bootinfo):
    """
    Boot session data for Airport Management System
    Called when user logs in to add custom data to the boot info
    """
    user = frappe.session.user
    
    # Add user-specific airport management data
    bootinfo.airport_data = {
        "user_roles": frappe.get_roles(user),
        "site_url": get_site_url(),
        "user_email": user,
        "has_airport_access": has_airport_access(user)
    }
    
    # Add quick stats for dashboard
    if has_airport_access(user):
        bootinfo.airport_stats = get_quick_stats()
    
    # Add notification preferences
    bootinfo.notification_settings = get_user_notification_settings(user)


def has_airport_access(user=None):
    """
    Check if user has access to airport management features
    """
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return True
        
    user_roles = frappe.get_roles(user)
    airport_roles = ["Airport Manager", "Shop Manager", "Ground Staff", "Tenant"]
    
    return any(role in user_roles for role in airport_roles)


def get_quick_stats():
    """
    Get quick statistics for the airport management dashboard
    """
    try:
        stats = {
            "total_shops": frappe.db.count("Airport Shop"),
            "available_shops": frappe.db.count("Airport Shop", {"status": "Available"}),
            "active_contracts": frappe.db.count("Contract Shop", {"status": "Active"}),
            "pending_leads": frappe.db.count("Shop Lead", {"status": "Open"})
        }
        return stats
    except Exception:
        return {}


def get_user_notification_settings(user):
    """
    Get user notification preferences
    """
    try:
        settings = frappe.db.get_value(
            "User", 
            user, 
            ["email", "phone", "enabled"], 
            as_dict=True
        )
        return settings or {}
    except Exception:
        return {}


# Jinja Methods
def jinja_methods():
    """
    Custom Jinja methods for templates
    """
    return {
        "get_shop_availability": get_shop_availability,
        "format_currency_custom": format_currency_custom,
        "get_contract_status": get_contract_status,
        "get_shop_image": get_shop_image,
        "is_contract_expiring": is_contract_expiring
    }


def jinja_filters():
    """
    Custom Jinja filters for templates
    """
    return {
        "currency_words": currency_words,
        "shop_status_color": shop_status_color,
        "days_until": days_until
    }


def get_shop_availability(shop_type=None):
    """
    Get available shops, optionally filtered by type
    """
    try:
        filters = {"status": "Available"}
        if shop_type:
            filters["shop_type"] = shop_type
        
        shops = frappe.get_all(
            "Airport Shop",
            filters=filters,
            fields=["name", "shop_name", "area", "rent_per_month", "shop_type"]
        )
        return shops
    except Exception:
        return []


def format_currency_custom(amount, currency="INR"):
    """
    Format currency with custom styling
    """
    try:
        if not amount:
            return "0"
        
        # Format with commas for Indian numbering system
        formatted = "{:,.2f}".format(float(amount))
        return f"{currency} {formatted}"
    except Exception:
        return str(amount)


def get_contract_status(contract_name):
    """
    Get detailed status of a contract
    """
    try:
        contract = frappe.get_doc("Contract Shop", contract_name)
        today = getdate()
        
        status_info = {
            "status": contract.status,
            "days_remaining": (getdate(contract.contract_end_date) - today).days if contract.contract_end_date else 0,
            "is_expiring": False
        }
        
        if status_info["days_remaining"] <= 30:
            status_info["is_expiring"] = True
            
        return status_info
    except Exception:
        return {"status": "Unknown", "days_remaining": 0, "is_expiring": False}


def get_shop_image(shop_name):
    """
    Get the main image for a shop
    """
    try:
        shop = frappe.get_doc("Airport Shop", shop_name)
        if hasattr(shop, 'image') and shop.image:
            return shop.image
        return "/assets/airplane_mode/images/default-shop.png"
    except Exception:
        return "/assets/airplane_mode/images/default-shop.png"


def is_contract_expiring(contract_end_date, days=30):
    """
    Check if contract is expiring within specified days
    """
    try:
        if not contract_end_date:
            return False
        
        today = getdate()
        end_date = getdate(contract_end_date)
        days_remaining = (end_date - today).days
        
        return days_remaining <= days and days_remaining >= 0
    except Exception:
        return False


# Jinja Filters
def currency_words(amount):
    """
    Convert currency amount to words
    """
    try:
        from frappe.utils import money_in_words
        return money_in_words(amount)
    except Exception:
        return str(amount)


def shop_status_color(status):
    """
    Get color code for shop status
    """
    color_map = {
        "Available": "success",
        "Occupied": "primary", 
        "Under Maintenance": "warning",
        "Reserved": "info",
        "Unavailable": "danger"
    }
    return color_map.get(status, "secondary")


def days_until(date):
    """
    Calculate days until a given date
    """
    try:
        if not date:
            return 0
        
        today = getdate()
        target_date = getdate(date)
        return (target_date - today).days
    except Exception:
        return 0


def before_job(job_name):
    """
    Execute before scheduled job
    """
    frappe.log_error(f"Starting job: {job_name}", "Job Start")


def after_job(job_name):
    """
    Execute after scheduled job
    """
    frappe.log_error(f"Completed job: {job_name}", "Job Complete")


def get_portal_menu_items(user=None):
    """
    Get custom portal menu items for airport management
    """
    if not user:
        user = frappe.session.user
        
    menu_items = []
    user_roles = frappe.get_roles(user)
    
    if "Tenant" in user_roles:
        menu_items.extend([
            {
                "title": _("My Contracts"),
                "route": "/my-contracts",
                "reference_doctype": "Contract Shop"
            },
            {
                "title": _("Payment History"),
                "route": "/payment-history", 
                "reference_doctype": "Sales Invoice"
            }
        ])
        
    if "Airport Manager" in user_roles or "Shop Manager" in user_roles:
        menu_items.extend([
            {
                "title": _("Shop Management"),
                "route": "/shop-management",
                "reference_doctype": "Airport Shop"
            },
            {
                "title": _("Lead Management"),
                "route": "/lead-management",
                "reference_doctype": "Shop Lead"
            }
        ])
    
    return menu_items


def validate_airport_permissions(user=None):
    """
    Validate user permissions for airport operations
    """
    if not user:
        user = frappe.session.user
        
    if user == "Administrator":
        return True
        
    # Check if user has any airport-related roles
    return has_airport_access(user)
