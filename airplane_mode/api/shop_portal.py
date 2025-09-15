import frappe
from frappe import _
from frappe.utils import nowdate, add_months, cint, flt
import json

@frappe.whitelist(allow_guest=True)
def get_available_shops():
    """Get list of available shops for the public portal"""
    
    shops = frappe.db.sql("""
        SELECT 
            name, shop_name, shop_type, location, area_sqft, 
            rent_per_sqft, total_monthly_rent, shop_description,
            airport, terminal, floor_level
        FROM `tabAirport Shop` 
        WHERE status = 'Available' 
        AND is_active = 1
        ORDER BY shop_type, area_sqft
    """, as_dict=True)
    
    shop_types = {}
    for shop in shops:
        shop_type = shop.get('shop_type', 'Others')
        if shop_type not in shop_types:
            shop_types[shop_type] = []
        shop_types[shop_type].append(shop)
    
    return {
        "status": "success",
        "shops": shops,
        "shops_by_type": shop_types,
        "total_available": len(shops)
    }

@frappe.whitelist(allow_guest=True)
def get_shop_details(shop_id):
    """Get detailed information about a specific shop"""
    
    if not shop_id:
        frappe.throw(_("Shop ID is required"))
    
    shop = frappe.get_doc("Airport Shop", shop_id)
    
    if shop.status != "Available":
        frappe.throw(_("This shop is not available for rent"))
    
    # Get shop images if any
    images = frappe.db.get_all("File", 
        filters={
            "attached_to_doctype": "Airport Shop",
            "attached_to_name": shop_id,
            "is_private": 0
        },
        fields=["file_url", "file_name"]
    )
    
    return {
        "status": "success",
        "shop": shop.as_dict(),
        "images": images,
        "contact_info": {
            "email": frappe.db.get_single_value("System Settings", "auto_email_id"),
            "phone": "+91-80-12345678"
        }
    }

@frappe.whitelist(allow_guest=True)
def submit_shop_application(shop_id, lead_data):
    """Submit application for a shop"""
    
    if isinstance(lead_data, str):
        lead_data = json.loads(lead_data)
    
    required_fields = ['lead_name', 'email', 'phone', 'business_type']
    for field in required_fields:
        if not lead_data.get(field):
            frappe.throw(_("Field {0} is required").format(field))
    
    shop = frappe.get_doc("Airport Shop", shop_id)
    if shop.status != "Available":
        frappe.throw(_("This shop is no longer available"))
    
    # Validate email format
    if not frappe.utils.validate_email_address(lead_data.get('email')):
        frappe.throw(_("Please provide a valid email address"))
    
    # Check for duplicate applications
    existing_lead = frappe.db.exists("Shop Lead", {
        "shop": shop_id,
        "email": lead_data.get('email'),
        "status": ["in", ["New", "Contacted", "Interested"]]
    })
    
    if existing_lead:
        frappe.throw(_("You have already submitted an application for this shop. We will contact you soon."))
    
    # Create lead
    lead = frappe.get_doc({
        "doctype": "Shop Lead",
        "shop": shop_id,
        "lead_name": lead_data.get('lead_name'),
        "email": lead_data.get('email'),
        "phone": lead_data.get('phone'),
        "business_type": lead_data.get('business_type'),
        "message": lead_data.get('message', ''),
        "status": "New",
        "lead_date": nowdate(),
        "source": "Website"
    })
    
    lead.insert(ignore_permissions=True)
    
    return {
        "status": "success", 
        "lead_id": lead.name, 
        "message": _("Thank you for your interest! We will contact you within 24 hours.")
    }

@frappe.whitelist()
def get_dashboard_data():
    """Get dashboard data for airport shop management"""
    
    total_shops = frappe.db.count("Airport Shop", {"is_active": 1})
    occupied_shops = frappe.db.count("Airport Shop", {"status": "Occupied", "is_active": 1})
    available_shops = frappe.db.count("Airport Shop", {"status": "Available", "is_active": 1})
    
    monthly_revenue = frappe.db.sql("""
        SELECT SUM(monthly_rent) as revenue
        FROM `tabContract Shop`
        WHERE docstatus = 1
        AND start_date <= CURDATE()
        AND end_date >= CURDATE()
    """)[0][0] or 0
    
    pending_leads = frappe.db.count("Shop Lead", {"status": "New"})
    
    expiring_contracts = frappe.db.count("Contract Shop", {
        "docstatus": 1,
        "end_date": ["between", [nowdate(), add_months(nowdate(), 3)]]
    })
    
    return {
        "total_shops": total_shops,
        "occupied_shops": occupied_shops,
        "available_shops": available_shops,
        "occupancy_rate": round((occupied_shops / total_shops * 100), 2) if total_shops > 0 else 0,
        "monthly_revenue": monthly_revenue,
        "pending_leads": pending_leads,
        "expiring_contracts": expiring_contracts
    }

@frappe.whitelist()
def send_follow_up_email(lead_name, message_type="follow_up"):
    """Send follow-up emails to leads"""
    
    lead = frappe.get_doc("Shop Lead", lead_name)
    
    if message_type == "follow_up":
        subject = f"Following up on your interest in {lead.shop}"
        message = f"""
        <p>Dear {lead.lead_name},</p>
        
        <p>We wanted to follow up on your recent inquiry about our airport shop at {lead.shop}.</p>
        
        <p>Our team is ready to discuss the opportunity with you. Would you be available for a call this week?</p>
        
        <p>Best regards,<br>Airport Management Team</p>
        """
    elif message_type == "reminder":
        subject = f"Reminder: Your application for {lead.shop}"
        message = f"""
        <p>Dear {lead.lead_name},</p>
        
        <p>This is a gentle reminder about your application for {lead.shop}.</p>
        
        <p>If you're still interested, please let us know so we can proceed with the next steps.</p>
        
        <p>Best regards,<br>Airport Management Team</p>
        """
    
    frappe.sendmail(
        recipients=[lead.email],
        subject=subject,
        message=message
    )
    
    # Update lead status
    lead.status = "Contacted"
    lead.save()
    
    return {"status": "success", "message": "Follow-up email sent successfully"}
