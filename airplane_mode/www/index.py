import frappe
from frappe import _


def get_context(context):
    """
    Get context for the main index page
    """
    # Basic site information
    context.title = _("Airport Management System")
    context.description = _("Comprehensive Airport Management with Shop Operations and Flight Management")
    
    # Add navigation items
    context.nav_items = [
        {"label": _("Flights"), "route": "/flights", "active": False},
        {"label": _("Shop Portal"), "route": "/shop-portal", "active": False},
        {"label": _("Available Shops"), "route": "/shop-availability", "active": False},
        {"label": _("Apply for Shop"), "route": "/apply-shop", "active": False}
    ]
    
    # Get public statistics for homepage
    try:
        context.stats = {
            "total_shops": frappe.db.count("Airport Shop"),
            "available_shops": frappe.db.count("Airport Shop", {"status": "Available"}),
            "active_flights": frappe.db.count("Airplane Flight", {"status": "Scheduled"}),
            "shop_types": frappe.db.count("Shop Type")
        }
    except Exception:
        context.stats = {
            "total_shops": 0,
            "available_shops": 0, 
            "active_flights": 0,
            "shop_types": 0
        }
    
    # Get featured shop types
    try:
        context.shop_types = frappe.get_all(
            "Shop Type",
            fields=["shop_type_name", "description"],
            limit=6
        )
    except Exception:
        context.shop_types = []
    
    # Get recent available shops
    try:
        context.featured_shops = frappe.get_all(
            "Airport Shop",
            filters={"status": "Available"},
            fields=["shop_name", "area", "rent_per_month", "shop_type", "name"],
            order_by="creation desc",
            limit=4
        )
    except Exception:
        context.featured_shops = []
    
    # User information if logged in
    if frappe.session.user != "Guest":
        context.user_name = frappe.get_value("User", frappe.session.user, "full_name")
        context.user_roles = frappe.get_roles(frappe.session.user)
    
    return context
