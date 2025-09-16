"""
REST API endpoints for Airplane Mode App
This file contains all the API endpoints and their configurations
"""

import frappe
from frappe import _

@frappe.whitelist(allow_guest=False, methods=["GET"])
def get_shops_list():
    """
    Get list of all shops with detailed information
    Endpoint: /api/method/airplane_mode.api.shop_api.get_shops_list
    """
    try:
        shops = frappe.db.get_list(
            "Airport Shop",
            fields=[
                "name",
                "shop_number", 
                "shop_name",
                "shop_type",
                "area_sqft",
                "rent_amount",
                "is_occupied",
                "tenant",
                "airport",
                "location_description",
                "status",
                "creation",
                "modified"
            ],
            order_by="shop_number"
        )
        
        return {
            "success": True,
            "data": shops,
            "count": len(shops)
        }
    except Exception as e:
        frappe.log_error(f"Error in get_shops_list: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist(allow_guest=False, methods=["POST"])
def create_shop(**kwargs):
    """
    Create a new shop via API
    Endpoint: /api/method/airplane_mode.api.shop_api.create_shop
    
    Required Parameters:
    - shop_number: Shop number/identifier
    - shop_name: Name of the shop
    - shop_type: Type of shop (link to Shop Type)
    - area_sqft: Area in square feet
    - airport: Airport where shop is located
    
    Optional Parameters:
    - rent_amount: Monthly rent amount
    - location_description: Description of shop location
    - tenant: Tenant information (if occupied)
    """
    try:
        # Validate required fields
        required_fields = ["shop_number", "shop_name", "shop_type", "area_sqft", "airport"]
        for field in required_fields:
            if not kwargs.get(field):
                return {
                    "success": False,
                    "error": f"Required field '{field}' is missing"
                }
        
        # Create shop document
        shop_doc = frappe.get_doc({
            "doctype": "Airport Shop",
            "shop_number": kwargs.get("shop_number"),
            "shop_name": kwargs.get("shop_name"), 
            "shop_type": kwargs.get("shop_type"),
            "area_sqft": kwargs.get("area_sqft"),
            "airport": kwargs.get("airport"),
            "rent_amount": kwargs.get("rent_amount", 0),
            "location_description": kwargs.get("location_description", ""),
            "tenant": kwargs.get("tenant", ""),
            "is_occupied": 1 if kwargs.get("tenant") else 0,
            "status": "Available" if not kwargs.get("tenant") else "Occupied"
        })
        
        shop_doc.insert()
        shop_doc.submit() if hasattr(shop_doc, 'submit') else None
        
        return {
            "success": True,
            "message": "Shop created successfully",
            "shop_id": shop_doc.name,
            "data": shop_doc.as_dict()
        }
        
    except frappe.DuplicateEntryError:
        return {
            "success": False,
            "error": f"Shop with number '{kwargs.get('shop_number')}' already exists"
        }
    except Exception as e:
        frappe.log_error(f"Error in create_shop: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist(allow_guest=False, methods=["GET"])
def get_shop_details(shop_id):
    """
    Get detailed information for a specific shop
    Endpoint: /api/method/airplane_mode.api.shop_api.get_shop_details?shop_id=SHOP-001
    """
    try:
        if not shop_id:
            return {
                "success": False,
                "error": "shop_id parameter is required"
            }
            
        shop = frappe.get_doc("Airport Shop", shop_id)
        
        # Get additional related data
        contracts = frappe.db.get_list(
            "Shop Contract",
            filters={"shop": shop_id},
            fields=["name", "start_date", "end_date", "monthly_rent", "status"]
        )
        
        return {
            "success": True,
            "data": {
                "shop_details": shop.as_dict(),
                "contracts": contracts
            }
        }
        
    except frappe.DoesNotExistError:
        return {
            "success": False,
            "error": f"Shop '{shop_id}' not found"
        }
    except Exception as e:
        frappe.log_error(f"Error in get_shop_details: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist(allow_guest=False, methods=["GET"])
def get_shop_types():
    """
    Get all enabled shop types
    Endpoint: /api/method/airplane_mode.api.shop_api.get_shop_types
    """
    try:
        shop_types = frappe.db.get_list(
            "Shop Type",
            filters={"enabled": 1},
            fields=["name", "shop_type_name", "description"],
            order_by="shop_type_name"
        )
        
        return {
            "success": True,
            "data": shop_types
        }
    except Exception as e:
        frappe.log_error(f"Error in get_shop_types: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@frappe.whitelist(allow_guest=False, methods=["GET"]) 
def get_airport_analytics(airport=None):
    """
    Get analytics for airport shops
    Endpoint: /api/method/airplane_mode.api.shop_api.get_airport_analytics
    """
    try:
        filters = {}
        if airport:
            filters["airport"] = airport
            
        total_shops = frappe.db.count("Airport Shop", filters)
        occupied_shops = frappe.db.count("Airport Shop", {**filters, "is_occupied": 1})
        available_shops = total_shops - occupied_shops
        
        occupancy_rate = (occupied_shops / total_shops * 100) if total_shops > 0 else 0
        
        # Get shop type distribution
        shop_type_data = frappe.db.sql("""
            SELECT 
                shop_type,
                COUNT(*) as count,
                SUM(CASE WHEN is_occupied = 1 THEN 1 ELSE 0 END) as occupied
            FROM `tabAirport Shop` 
            WHERE airport = %(airport)s OR %(airport)s IS NULL
            GROUP BY shop_type
        """, {"airport": airport}, as_dict=True)
        
        return {
            "success": True,
            "data": {
                "summary": {
                    "total_shops": total_shops,
                    "occupied_shops": occupied_shops, 
                    "available_shops": available_shops,
                    "occupancy_rate": round(occupancy_rate, 2)
                },
                "shop_type_distribution": shop_type_data
            }
        }
    except Exception as e:
        frappe.log_error(f"Error in get_airport_analytics: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
