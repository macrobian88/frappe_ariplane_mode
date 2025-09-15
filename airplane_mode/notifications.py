import frappe
from frappe import _


def get_notification_config():
    """
    Get notification configuration for Airport Management System
    Returns notification settings and alerts configuration
    """
    return {
        # Email alerts configuration
        "for_doctype": {
            "Shop Lead": {"status": "Open"},
            "Contract Shop": {"status": "Active"},
            "Airport Shop": {"status": "Available"}
        },
        
        # Desktop notifications
        "notifications": {
            "Shop Lead": {
                "doctype": "Shop Lead",
                "filters": [["status", "=", "Open"]],
                "field_map": {
                    "lead_name": 1,
                    "phone": 1,
                    "email": 1
                }
            },
            "Contract Shop": {
                "doctype": "Contract Shop",
                "filters": [["status", "=", "Active"]],
                "field_map": {
                    "tenant_name": 1,
                    "shop": 1,
                    "contract_end_date": 1
                }
            },
            "Airport Shop": {
                "doctype": "Airport Shop", 
                "filters": [["status", "=", "Available"]],
                "field_map": {
                    "shop_name": 1,
                    "shop_type": 1,
                    "area": 1
                }
            }
        },
        
        # Real-time notifications
        "open_count_doctype": {
            "Shop Lead": "Airport Shop Management",
            "Contract Shop": "Airport Shop Management", 
            "Airport Shop": "Airport Shop Management"
        },
        
        # Notification indicators
        "targets": {
            "Shop Lead": {
                "color": "blue",
                "title": _("New Shop Leads"),
                "route": "/app/shop-lead"
            },
            "Contract Shop": {
                "color": "green", 
                "title": _("Active Contracts"),
                "route": "/app/contract-shop"
            },
            "Airport Shop": {
                "color": "orange",
                "title": _("Available Shops"), 
                "route": "/app/airport-shop"
            }
        }
    }


def get_permission_query_conditions(user):
    """
    Get permission query conditions for notifications
    """
    if not user:
        user = frappe.session.user

    if user == "Administrator":
        return ""

    # Standard user restrictions
    return f"""
        `tabShop Lead`.owner = '{user}' OR 
        `tabContract Shop`.owner = '{user}' OR
        `tabAirport Shop`.owner = '{user}'
    """


def has_permission(doc, ptype="read", user=None):
    """
    Check if user has permission for notification-related documents
    """
    if not user:
        user = frappe.session.user
        
    if user == "Administrator":
        return True
        
    # Check if user is the owner
    if doc.owner == user:
        return True
        
    # Check role-based permissions
    user_roles = frappe.get_roles(user)
    
    if "Airport Manager" in user_roles:
        return True
    elif "Shop Manager" in user_roles and doc.doctype in ["Shop Lead", "Airport Shop"]:
        return True
    elif "Tenant" in user_roles and doc.doctype == "Contract Shop":
        # Tenants can only see their own contracts
        return doc.tenant_email == frappe.session.user
        
    return False


def send_notification_email(doc, method):
    """
    Send email notifications for important events
    """
    try:
        if doc.doctype == "Shop Lead" and method == "after_insert":
            # Send welcome email to new leads
            frappe.sendmail(
                recipients=[doc.email],
                subject=_("Thank you for your interest in our Airport Shops"),
                template="shop_lead_welcome",
                args={
                    "lead_name": doc.lead_name,
                    "shop_type": doc.preferred_shop_type
                }
            )
            
        elif doc.doctype == "Contract Shop" and method == "on_submit":
            # Send contract confirmation
            frappe.sendmail(
                recipients=[doc.tenant_email],
                subject=_("Shop Contract Confirmation"),
                template="contract_confirmation", 
                args={
                    "tenant_name": doc.tenant_name,
                    "shop_name": doc.shop,
                    "contract_start_date": doc.contract_start_date,
                    "contract_end_date": doc.contract_end_date
                }
            )
            
    except Exception as e:
        frappe.log_error(f"Notification email failed: {str(e)}", "Notification Error")


def get_dashboard_data(data):
    """
    Get data for notification dashboard widgets
    """
    return {
        "fieldname": "reference_doctype",
        "non_standard_fieldnames": {
            "Shop Lead": "name",
            "Contract Shop": "name", 
            "Airport Shop": "name"
        },
        "transactions": [
            {
                "label": _("Leads & Applications"),
                "items": ["Shop Lead"]
            },
            {
                "label": _("Active Operations"), 
                "items": ["Contract Shop", "Airport Shop"]
            }
        ]
    }
