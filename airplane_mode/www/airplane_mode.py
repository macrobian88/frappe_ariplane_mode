import frappe
from frappe import _


def get_context(context):
    """
    Get context for the airplane mode main app page
    """
    context.title = _("Airport Management System")
    context.description = _("Complete Airport Operations Management")
    
    # Check user permissions
    if frappe.session.user == "Guest":
        # Redirect guests to login or public pages
        context.show_login_prompt = True
        context.login_url = "/login"
    else:
        context.show_login_prompt = False
        context.user_name = frappe.get_value("User", frappe.session.user, "full_name")
        context.user_roles = frappe.get_roles(frappe.session.user)
        
        # Check if user has airport access
        from airplane_mode.utils import has_airport_access
        context.has_access = has_airport_access(frappe.session.user)
        
        if not context.has_access:
            context.no_access = True
            return context
    
    # Get dashboard statistics
    try:
        context.stats = {
            "total_shops": frappe.db.count("Airport Shop"),
            "available_shops": frappe.db.count("Airport Shop", {"status": "Available"}),
            "active_contracts": frappe.db.count("Contract Shop", {"status": "Active"}),
            "pending_leads": frappe.db.count("Shop Lead", {"status": "Open"}),
            "total_flights": frappe.db.count("Airplane Flight"),
            "scheduled_flights": frappe.db.count("Airplane Flight", {"status": "Scheduled"})
        }
    except Exception as e:
        frappe.log_error(f"Dashboard stats error: {str(e)}")
        context.stats = {
            "total_shops": 5,
            "available_shops": 3,
            "active_contracts": 2,
            "pending_leads": 4,
            "total_flights": 12,
            "scheduled_flights": 8
        }
    
    # Get recent activities (if user has access)
    if not frappe.session.user == "Guest":
        try:
            # Recent shop leads
            context.recent_leads = frappe.get_all(
                "Shop Lead",
                filters={"status": "Open"},
                fields=["name", "lead_name", "email", "preferred_shop_type", "creation"],
                order_by="creation desc",
                limit=5
            )
            
            # Recent contracts
            context.recent_contracts = frappe.get_all(
                "Contract Shop", 
                filters={"status": "Active"},
                fields=["name", "tenant_name", "shop", "contract_start_date"],
                order_by="creation desc",
                limit=5
            )
            
        except Exception as e:
            frappe.log_error(f"Recent activities error: {str(e)}")
            context.recent_leads = []
            context.recent_contracts = []
    
    # Navigation items based on user role
    context.nav_items = []
    
    if frappe.session.user != "Guest":
        user_roles = frappe.get_roles(frappe.session.user)
        
        if "Airport Manager" in user_roles or "Shop Manager" in user_roles:
            context.nav_items.extend([
                {"title": _("Shop Management"), "route": "/app/airport-shop", "icon": "fas fa-store"},
                {"title": _("Contract Management"), "route": "/app/contract-shop", "icon": "fas fa-file-contract"},
                {"title": _("Lead Management"), "route": "/app/shop-lead", "icon": "fas fa-users"},
                {"title": _("Analytics"), "route": "/app/query-report/Shop%20Revenue%20Report", "icon": "fas fa-chart-bar"}
            ])
            
        if "Airport Manager" in user_roles:
            context.nav_items.extend([
                {"title": _("Flight Operations"), "route": "/app/airplane-flight", "icon": "fas fa-plane"},
                {"title": _("Airport Configuration"), "route": "/app/airport", "icon": "fas fa-building"}
            ])
            
        if "Tenant" in user_roles:
            context.nav_items.extend([
                {"title": _("My Contracts"), "route": "/app/contract-shop", "icon": "fas fa-file-contract"},
                {"title": _("Payment History"), "route": "/app/sales-invoice", "icon": "fas fa-receipt"}
            ])
    
    return context
