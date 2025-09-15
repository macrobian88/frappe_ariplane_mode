import frappe
from frappe import _


@frappe.whitelist()
def has_app_permission(user=None):
    """
    Check if user has permission to access Airport Management System
    Called by hooks.py in add_to_apps_screen configuration
    """
    if not user:
        user = frappe.session.user
    
    # Administrator always has access
    if user == "Administrator":
        return True
    
    # Check if user has any of the airport management roles
    user_roles = frappe.get_roles(user)
    airport_roles = [
        "Airport Manager", 
        "Shop Manager", 
        "Ground Staff", 
        "Tenant",
        "System Manager"
    ]
    
    # Check if user has any airport-related role
    has_role = any(role in user_roles for role in airport_roles)
    
    if has_role:
        return True
    
    # Check if user has any airport-related documents
    has_documents = (
        frappe.db.exists("Shop Lead", {"owner": user}) or
        frappe.db.exists("Contract Shop", {"tenant_email": user}) or
        frappe.db.exists("Airport Shop", {"owner": user})
    )
    
    return has_documents


@frappe.whitelist()
def get_user_permissions(doctype=None, user=None):
    """
    Get user permissions for specific doctype
    """
    if not user:
        user = frappe.session.user
        
    if user == "Administrator":
        return {"read": True, "write": True, "create": True, "delete": True}
    
    user_roles = frappe.get_roles(user)
    
    # Default permissions
    permissions = {"read": False, "write": False, "create": False, "delete": False}
    
    # Airport Manager has full access
    if "Airport Manager" in user_roles:
        permissions = {"read": True, "write": True, "create": True, "delete": True}
    
    # Shop Manager permissions
    elif "Shop Manager" in user_roles:
        if doctype in ["Airport Shop", "Shop Lead", "Contract Shop"]:
            permissions = {"read": True, "write": True, "create": True, "delete": False}
        else:
            permissions = {"read": True, "write": False, "create": False, "delete": False}
    
    # Tenant permissions  
    elif "Tenant" in user_roles:
        if doctype == "Contract Shop":
            permissions = {"read": True, "write": False, "create": False, "delete": False}
        elif doctype == "Shop Lead":
            permissions = {"read": True, "write": True, "create": True, "delete": False}
        else:
            permissions = {"read": True, "write": False, "create": False, "delete": False}
    
    # Ground Staff permissions
    elif "Ground Staff" in user_roles:
        permissions = {"read": True, "write": False, "create": False, "delete": False}
    
    return permissions


@frappe.whitelist()
def check_doctype_access(doctype, user=None):
    """
    Check if user can access a specific doctype
    """
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return True
    
    # Get user permissions for the doctype
    perms = get_user_permissions(doctype, user)
    
    # User has access if they can at least read
    return perms.get("read", False)


@frappe.whitelist() 
def validate_shop_access(shop_name, user=None):
    """
    Validate if user can access a specific shop
    """
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    # Airport Manager and Shop Manager have access to all shops
    if "Airport Manager" in user_roles or "Shop Manager" in user_roles:
        return True
    
    # Tenant can only access their contracted shops
    if "Tenant" in user_roles:
        # Check if user has active contract for this shop
        contract_exists = frappe.db.exists(
            "Contract Shop", 
            {
                "shop": shop_name,
                "tenant_email": user,
                "status": "Active"
            }
        )
        return bool(contract_exists)
    
    return False


@frappe.whitelist()
def get_accessible_shops(user=None):
    """
    Get list of shops accessible to the user
    """
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return frappe.get_all("Airport Shop", fields=["name", "shop_name"])
    
    user_roles = frappe.get_roles(user)
    
    # Airport Manager and Shop Manager can see all shops
    if "Airport Manager" in user_roles or "Shop Manager" in user_roles:
        return frappe.get_all("Airport Shop", fields=["name", "shop_name", "status"])
    
    # Tenant can only see their contracted shops and available shops
    if "Tenant" in user_roles:
        # Get shops with active contracts
        contracted_shops = frappe.get_all(
            "Contract Shop",
            filters={"tenant_email": user, "status": "Active"},
            fields=["shop"]
        )
        
        shop_names = [shop.shop for shop in contracted_shops]
        
        # Add available shops for potential contracting
        available_shops = frappe.get_all(
            "Airport Shop",
            filters={"status": "Available"},
            fields=["name", "shop_name"]
        )
        
        # Combine contracted and available shops
        accessible_shops = frappe.get_all(
            "Airport Shop",
            filters={"name": ["in", shop_names]},
            fields=["name", "shop_name", "status"]
        )
        
        accessible_shops.extend(available_shops)
        return accessible_shops
    
    # Default: no access
    return []


@frappe.whitelist()
def check_contract_permissions(contract_name, user=None):
    """
    Check permissions for contract operations
    """
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    # Airport Manager has full access
    if "Airport Manager" in user_roles:
        return True
    
    # Shop Manager can manage contracts
    if "Shop Manager" in user_roles:
        return True
    
    # Tenant can only access their own contracts
    if "Tenant" in user_roles:
        contract = frappe.get_doc("Contract Shop", contract_name)
        return contract.tenant_email == user
    
    return False


@frappe.whitelist()
def get_dashboard_permissions(user=None):
    """
    Get dashboard access permissions for user
    """
    if not user:
        user = frappe.session.user
    
    user_roles = frappe.get_roles(user)
    
    permissions = {
        "can_view_analytics": False,
        "can_manage_shops": False,
        "can_view_financials": False,
        "can_manage_contracts": False,
        "can_view_leads": False
    }
    
    if "Administrator" in user_roles or "Airport Manager" in user_roles:
        # Full dashboard access
        permissions = {k: True for k in permissions.keys()}
    
    elif "Shop Manager" in user_roles:
        permissions.update({
            "can_view_analytics": True,
            "can_manage_shops": True,
            "can_manage_contracts": True,
            "can_view_leads": True
        })
    
    elif "Tenant" in user_roles:
        permissions.update({
            "can_view_analytics": False,  # Limited analytics
            "can_manage_shops": False,
            "can_view_financials": False,  # Own finances only
            "can_manage_contracts": False,  # View only
            "can_view_leads": False
        })
    
    return permissions


def get_permission_query_conditions_for_shop_lead(user=None):
    """
    Permission query conditions for Shop Lead doctype
    """
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return ""
    
    user_roles = frappe.get_roles(user)
    
    if "Airport Manager" in user_roles or "Shop Manager" in user_roles:
        return ""  # Can see all leads
    
    # Users can only see their own leads
    return f"`tabShop Lead`.owner = '{user}'"


def get_permission_query_conditions_for_contract_shop(user=None):
    """
    Permission query conditions for Contract Shop doctype
    """
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return ""
    
    user_roles = frappe.get_roles(user)
    
    if "Airport Manager" in user_roles or "Shop Manager" in user_roles:
        return ""  # Can see all contracts
    
    # Tenants can only see their own contracts
    if "Tenant" in user_roles:
        return f"`tabContract Shop`.tenant_email = '{user}'"
    
    # Default: no access
    return "1=0"


def get_permission_query_conditions_for_airport_shop(user=None):
    """
    Permission query conditions for Airport Shop doctype
    """
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return ""
    
    user_roles = frappe.get_roles(user)
    
    if "Airport Manager" in user_roles or "Shop Manager" in user_roles:
        return ""  # Can see all shops
    
    if "Tenant" in user_roles:
        # Tenants can see available shops and their contracted shops
        contracted_shops = frappe.get_all(
            "Contract Shop",
            filters={"tenant_email": user, "status": "Active"},
            pluck="shop"
        )
        
        if contracted_shops:
            shop_list = "', '".join(contracted_shops)
            return f"(`tabAirport Shop`.status = 'Available' OR `tabAirport Shop`.name IN ('{shop_list}'))"
        else:
            return "`tabAirport Shop`.status = 'Available'"
    
    # Default: can see available shops only
    return "`tabAirport Shop`.status = 'Available'"
