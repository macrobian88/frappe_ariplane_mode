import frappe
from frappe import _


def get_context(context):
    """
    Get context for shop application page
    """
    context.title = _("Apply for Shop")
    context.description = _("Submit your application to rent a shop space")
    
    # Get specific shop if provided in URL
    shop_param = frappe.form_dict.get('shop')
    if shop_param:
        try:
            shop_details = frappe.get_doc("Airport Shop", shop_param)
            if shop_details.status == "Available":
                context.selected_shop = {
                    "name": shop_details.name,
                    "shop_name": shop_details.shop_name,
                    "shop_type": shop_details.shop_type,
                    "area": shop_details.area,
                    "rent_per_month": shop_details.rent_per_month,
                    "location": shop_details.location,
                    "description": shop_details.description
                }
        except Exception:
            context.selected_shop = None
    else:
        context.selected_shop = None
    
    # Get available shop types for dropdown
    try:
        context.shop_types = frappe.get_all(
            "Shop Type",
            fields=["name", "shop_type_name", "description"],
            order_by="shop_type_name"
        )
    except Exception:
        context.shop_types = []
    
    # Get available shops for dropdown
    try:
        context.available_shops = frappe.get_all(
            "Airport Shop",
            filters={"status": "Available"},
            fields=["name", "shop_name", "shop_type", "area", "rent_per_month"],
            order_by="shop_name"
        )
    except Exception:
        context.available_shops = []
    
    # Handle form submission
    if frappe.form_dict.get('submit_application'):
        try:
            create_shop_lead(frappe.form_dict)
            context.success_message = _("Your application has been submitted successfully! We will contact you soon.")
        except Exception as e:
            context.error_message = _("There was an error submitting your application. Please try again.")
            frappe.log_error(f"Shop application error: {str(e)}")
    
    return context


def create_shop_lead(form_data):
    """
    Create a new Shop Lead from the application form
    """
    # Create new Shop Lead document
    lead = frappe.new_doc("Shop Lead")
    
    # Basic information
    lead.lead_name = form_data.get('full_name')
    lead.email = form_data.get('email')
    lead.phone = form_data.get('phone')
    lead.company_name = form_data.get('company_name')
    
    # Shop preferences
    lead.preferred_shop = form_data.get('preferred_shop') if form_data.get('preferred_shop') != 'any' else None
    lead.preferred_shop_type = form_data.get('preferred_shop_type')
    lead.budget_range = form_data.get('budget_range')
    
    # Business details
    lead.business_type = form_data.get('business_type')
    lead.business_description = form_data.get('business_description')
    lead.experience_years = int(form_data.get('experience_years', 0)) if form_data.get('experience_years') else 0
    
    # Additional information
    lead.notes = form_data.get('additional_notes')
    lead.source = "Website Application"
    lead.status = "Open"
    
    # Save the document
    lead.insert(ignore_permissions=True)
    
    return lead


@frappe.whitelist(allow_guest=True)
def submit_shop_application():
    """
    API endpoint to handle shop application submission
    """
    try:
        # Validate required fields
        required_fields = ['full_name', 'email', 'phone', 'business_type']
        for field in required_fields:
            if not frappe.form_dict.get(field):
                frappe.throw(_("Please fill all required fields"))
        
        # Create the lead
        lead = create_shop_lead(frappe.form_dict)
        
        return {
            "success": True,
            "message": _("Application submitted successfully!"),
            "lead_id": lead.name
        }
        
    except Exception as e:
        frappe.log_error(f"Shop application API error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }
