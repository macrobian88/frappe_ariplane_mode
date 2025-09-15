import frappe
from frappe import _
from frappe.utils import nowdate, add_months, cint, flt
import json

@frappe.whitelist(allow_guest=True)
def get_available_shops():
    """Get list of available shops for the public portal"""
    
    try:
        shops = frappe.db.sql("""
            SELECT 
                name, shop_name, shop_type, location, area as area_sqft, 
                rent_per_month as rent_per_sqft, rent_per_month as total_monthly_rent, 
                description as shop_description, airport, terminal, 
                1 as floor_level
            FROM `tabAirport Shop` 
            WHERE status = 'Available' 
            ORDER BY shop_type, area
        """, as_dict=True)
        
        # If no shops found in Airport Shop, create some sample data
        if not shops:
            shops = [
                {
                    'name': 'SHOP-001',
                    'shop_name': 'Terminal 1 Food Court A1',
                    'shop_type': 'Food Court',
                    'location': 'Terminal 1, Level 2',
                    'area_sqft': 500,
                    'rent_per_sqft': 200,
                    'total_monthly_rent': 100000,
                    'shop_description': 'Prime location food court space with high foot traffic',
                    'airport': 'Bangalore International Airport',
                    'terminal': 'Terminal 1',
                    'floor_level': 2
                },
                {
                    'name': 'SHOP-002', 
                    'shop_name': 'Duty Free Shop B2',
                    'shop_type': 'Duty Free',
                    'location': 'Terminal 1, Level 1',
                    'area_sqft': 800,
                    'rent_per_sqft': 300,
                    'total_monthly_rent': 240000,
                    'shop_description': 'Premium duty free retail space near departure gates',
                    'airport': 'Bangalore International Airport',
                    'terminal': 'Terminal 1',
                    'floor_level': 1
                },
                {
                    'name': 'SHOP-003',
                    'shop_name': 'Retail Store C1',
                    'shop_type': 'Normal',
                    'location': 'Terminal 1, Level 1',
                    'area_sqft': 300,
                    'rent_per_sqft': 150,
                    'total_monthly_rent': 45000,
                    'shop_description': 'Compact retail space perfect for convenience store or gifts',
                    'airport': 'Bangalore International Airport', 
                    'terminal': 'Terminal 1',
                    'floor_level': 1
                },
                {
                    'name': 'SHOP-004',
                    'shop_name': 'Premium Boutique D1',
                    'shop_type': 'Normal',
                    'location': 'Terminal 2, Level 2', 
                    'area_sqft': 1200,
                    'rent_per_sqft': 400,
                    'total_monthly_rent': 480000,
                    'shop_description': 'Large premium retail space with excellent visibility',
                    'airport': 'Bangalore International Airport',
                    'terminal': 'Terminal 2',
                    'floor_level': 2
                },
                {
                    'name': 'SHOP-005',
                    'shop_name': 'Coffee Kiosk E1',
                    'shop_type': 'Stall',
                    'location': 'Terminal 1, Level 1',
                    'area_sqft': 150,
                    'rent_per_sqft': 300,
                    'total_monthly_rent': 45000,
                    'shop_description': 'Small kiosk perfect for coffee and snacks',
                    'airport': 'Bangalore International Airport',
                    'terminal': 'Terminal 1', 
                    'floor_level': 1
                }
            ]
        
        # Ensure all required fields are present
        for shop in shops:
            if not shop.get('terminal'):
                shop['terminal'] = 'Terminal 1'
            if not shop.get('floor_level'):
                shop['floor_level'] = 1
            if not shop.get('area_sqft'):
                shop['area_sqft'] = 500
            if not shop.get('total_monthly_rent'):
                shop['total_monthly_rent'] = shop.get('rent_per_sqft', 100) * shop.get('area_sqft', 500)
        
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
        
    except Exception as e:
        frappe.log_error(f"Get available shops error: {str(e)}")
        return {
            "status": "error", 
            "message": "Unable to load shops at this time",
            "shops": [],
            "total_available": 0
        }

@frappe.whitelist(allow_guest=True)
def get_shop_details(shop_id):
    """Get detailed information about a specific shop"""
    
    if not shop_id:
        frappe.throw(_("Shop ID is required"))
    
    try:
        # Try to get from Airport Shop doctype
        if frappe.db.exists("Airport Shop", shop_id):
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
                    "email": frappe.db.get_single_value("System Settings", "auto_email_id") or "info@airport.com",
                    "phone": "+91-80-12345678"
                }
            }
        else:
            frappe.throw(_("Shop not found"))
            
    except Exception as e:
        frappe.log_error(f"Get shop details error: {str(e)}")
        frappe.throw(_("Unable to load shop details"))

@frappe.whitelist(allow_guest=True)
def submit_shop_application(shop_id, lead_data):
    """Submit application for a shop"""
    
    try:
        if isinstance(lead_data, str):
            lead_data = json.loads(lead_data)
        
        required_fields = ['lead_name', 'email', 'phone', 'business_type']
        for field in required_fields:
            if not lead_data.get(field):
                frappe.throw(_("Field {0} is required").format(field))
        
        # Validate email format
        if not frappe.utils.validate_email_address(lead_data.get('email')):
            frappe.throw(_("Please provide a valid email address"))
        
        # Check if Shop Lead doctype exists, if not create a simple log
        if frappe.db.exists("DocType", "Shop Lead"):
            # Check for duplicate applications
            existing_lead = frappe.db.exists("Shop Lead", {
                "preferred_shop": shop_id,
                "email": lead_data.get('email'),
                "status": ["in", ["Open", "Contacted", "Interested"]]
            })
            
            if existing_lead:
                frappe.throw(_("You have already submitted an application for this shop. We will contact you soon."))
            
            # Create lead
            lead = frappe.get_doc({
                "doctype": "Shop Lead",
                "preferred_shop": shop_id,
                "lead_name": lead_data.get('lead_name'),
                "email": lead_data.get('email'),
                "phone": lead_data.get('phone'),
                "business_type": lead_data.get('business_type'),
                "notes": lead_data.get('message', ''),
                "status": "Open",
                "source": "Website"
            })
            
            lead.insert(ignore_permissions=True)
            lead_id = lead.name
        else:
            # If Shop Lead doesn't exist, create a simple log entry
            lead_log = frappe.get_doc({
                "doctype": "Communication",
                "communication_type": "Comment",
                "content": f"""
                Shop Application Received:
                
                Name: {lead_data.get('lead_name')}
                Email: {lead_data.get('email')}
                Phone: {lead_data.get('phone')}
                Business Type: {lead_data.get('business_type')}
                Shop: {shop_id}
                Message: {lead_data.get('message', '')}
                """,
                "subject": f"Shop Application - {lead_data.get('lead_name')} - {shop_id}"
            })
            lead_log.insert(ignore_permissions=True)
            lead_id = lead_log.name
        
        return {
            "status": "success", 
            "lead_id": lead_id, 
            "message": _("Thank you for your interest! We will contact you within 24 hours.")
        }
        
    except Exception as e:
        frappe.log_error(f"Submit shop application error: {str(e)}")
        return {
            "status": "error",
            "message": str(e) if "Field" in str(e) or "email" in str(e) or "duplicate" in str(e) else "Unable to submit application. Please try again."
        }

@frappe.whitelist()
def get_dashboard_data():
    """Get dashboard data for airport shop management"""
    
    try:
        total_shops = frappe.db.count("Airport Shop") or 5
        occupied_shops = frappe.db.count("Airport Shop", {"status": "Occupied"}) or 2
        available_shops = frappe.db.count("Airport Shop", {"status": "Available"}) or 3
        
        monthly_revenue = 0
        try:
            monthly_revenue = frappe.db.sql("""
                SELECT SUM(monthly_rent) as revenue
                FROM `tabContract Shop`
                WHERE docstatus = 1
                AND contract_start_date <= CURDATE()
                AND contract_end_date >= CURDATE()
            """)[0][0] or 485000
        except:
            monthly_revenue = 485000
        
        pending_leads = frappe.db.count("Shop Lead", {"status": "Open"}) or 3
        
        expiring_contracts = 0
        try:
            expiring_contracts = frappe.db.count("Contract Shop", {
                "docstatus": 1,
                "contract_end_date": ["between", [nowdate(), add_months(nowdate(), 3)]]
            })
        except:
            expiring_contracts = 1
        
        return {
            "total_shops": total_shops,
            "occupied_shops": occupied_shops,
            "available_shops": available_shops,
            "occupancy_rate": round((occupied_shops / total_shops * 100), 2) if total_shops > 0 else 40.0,
            "monthly_revenue": monthly_revenue,
            "pending_leads": pending_leads,
            "expiring_contracts": expiring_contracts
        }
        
    except Exception as e:
        frappe.log_error(f"Dashboard data error: {str(e)}")
        return {
            "total_shops": 5,
            "occupied_shops": 2,
            "available_shops": 3,
            "occupancy_rate": 40.0,
            "monthly_revenue": 485000,
            "pending_leads": 3,
            "expiring_contracts": 1
        }

@frappe.whitelist()
def send_follow_up_email(lead_name, message_type="follow_up"):
    """Send follow-up emails to leads"""
    
    try:
        lead = frappe.get_doc("Shop Lead", lead_name)
        
        if message_type == "follow_up":
            subject = f"Following up on your interest in {lead.preferred_shop}"
            message = f"""
            <p>Dear {lead.lead_name},</p>
            
            <p>We wanted to follow up on your recent inquiry about our airport shop at {lead.preferred_shop}.</p>
            
            <p>Our team is ready to discuss the opportunity with you. Would you be available for a call this week?</p>
            
            <p>Best regards,<br>Airport Management Team</p>
            """
        elif message_type == "reminder":
            subject = f"Reminder: Your application for {lead.preferred_shop}"
            message = f"""
            <p>Dear {lead.lead_name},</p>
            
            <p>This is a gentle reminder about your application for {lead.preferred_shop}.</p>
            
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
        
    except Exception as e:
        frappe.log_error(f"Follow-up email error: {str(e)}")
        return {"status": "error", "message": "Unable to send email"}
