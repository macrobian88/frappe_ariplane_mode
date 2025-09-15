import frappe
from frappe import _


def get_context(context):
    """
    Get context for shop availability page
    """
    context.title = _("Available Shops")
    context.description = _("Browse available retail spaces at the airport")
    
    # Get filter parameters
    shop_type_filter = frappe.form_dict.get('shop_type')
    min_area = frappe.form_dict.get('min_area')
    max_rent = frappe.form_dict.get('max_rent')
    
    # Build filters
    filters = {"status": "Available"}
    if shop_type_filter:
        filters["shop_type"] = shop_type_filter
    if min_area:
        filters["area"] = [">=", int(min_area)]
    
    # Get available shops
    try:
        available_shops = frappe.get_all(
            "Airport Shop",
            filters=filters,
            fields=[
                "name", "shop_name", "shop_type", "area", "location", 
                "rent_per_month", "description", "image"
            ],
            order_by="rent_per_month asc"
        )
        
        # Filter by max rent if specified
        if max_rent:
            max_rent_val = int(max_rent)
            available_shops = [shop for shop in available_shops if (shop.rent_per_month or 0) <= max_rent_val]
        
        context.available_shops = available_shops
        context.total_available = len(available_shops)
        
    except Exception as e:
        frappe.log_error(f"Shop availability error: {str(e)}")
        context.available_shops = []
        context.total_available = 0
    
    # Get shop types for filter dropdown
    try:
        context.shop_types = frappe.get_all(
            "Shop Type",
            fields=["name", "shop_type_name"],
            order_by="shop_type_name"
        )
    except Exception:
        context.shop_types = []
    
    # Get statistics
    try:
        context.stats = {
            "total_shops": frappe.db.count("Airport Shop"),
            "available_count": frappe.db.count("Airport Shop", {"status": "Available"}),
            "occupied_count": frappe.db.count("Airport Shop", {"status": "Occupied"}),
            "avg_rent": frappe.db.sql("""
                SELECT AVG(rent_per_month) as avg_rent 
                FROM `tabAirport Shop` 
                WHERE status = 'Available' AND rent_per_month > 0
            """, as_dict=True)[0].avg_rent or 0
        }
    except Exception:
        context.stats = {
            "total_shops": 0,
            "available_count": 0,
            "occupied_count": 0,
            "avg_rent": 0
        }
    
    # Current filters for display
    context.current_filters = {
        "shop_type": shop_type_filter,
        "min_area": min_area,
        "max_rent": max_rent
    }
    
    return context
