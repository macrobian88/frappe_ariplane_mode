import frappe
from frappe import _


def get_context(context):
    """
    Get context for the shop portal page
    """
    context.title = _("Airport Shop Portal")
    context.description = _("Discover premium retail opportunities at our world-class airport")
    
    # Check if user is logged in and get user info
    if frappe.session.user != "Guest":
        context.user_name = frappe.get_value("User", frappe.session.user, "full_name")
        context.user_roles = frappe.get_roles(frappe.session.user)
    else:
        context.user_name = None
        context.user_roles = []
    
    # Get basic statistics for display
    try:
        context.stats = {
            "total_shops": frappe.db.count("Airport Shop"),
            "available_shops": frappe.db.count("Airport Shop", {"status": "Available"}),
            "occupied_shops": frappe.db.count("Airport Shop", {"status": "Occupied"}),
            "total_applications": frappe.db.count("Shop Lead")
        }
    except Exception as e:
        frappe.log_error(f"Shop portal stats error: {str(e)}")
        context.stats = {
            "total_shops": 0,
            "available_shops": 0,
            "occupied_shops": 0,
            "total_applications": 0
        }
    
    # Get shop types for filters
    try:
        context.shop_types = frappe.get_all(
            "Shop Type",
            fields=["name", "shop_type_name"],
            order_by="shop_type_name"
        )
    except Exception as e:
        frappe.log_error(f"Shop types error: {str(e)}")
        context.shop_types = []
    
    return context
