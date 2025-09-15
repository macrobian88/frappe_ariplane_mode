import frappe
from frappe import _
from frappe.utils import nowdate

def send_lead_notifications(doc, method):
    """Send notifications when a new lead is created"""
    
    send_admin_notification(doc)
    send_lead_confirmation(doc)

def send_admin_notification(lead):
    """Send notification to admin about new lead"""
    try:
        shop = frappe.get_doc("Airport Shop", lead.shop)
        
        admin_emails = frappe.db.get_single_value("System Settings", "auto_email_id")
        if not admin_emails:
            admin_emails = "admin@airport.com"
        
        frappe.sendmail(
            recipients=[admin_emails],
            subject=f"New Shop Lead: {shop.shop_name}",
            message=f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                    🏪 New Shop Lead Received
                </h2>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #2980b9; margin-top: 0;">Shop Details</h3>
                    <p><strong>Shop Name:</strong> {shop.shop_name}</p>
                    <p><strong>Shop ID:</strong> {lead.shop}</p>
                    <p><strong>Location:</strong> {shop.location}</p>
                    <p><strong>Area:</strong> {shop.area_sqft} sq ft</p>
                    <p><strong>Monthly Rent:</strong> ₹{shop.total_monthly_rent:,.2f}</p>
                </div>
                
                <div style="background-color: #e8f5e8; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #27ae60; margin-top: 0;">Lead Information</h3>
                    <p><strong>Name:</strong> {lead.lead_name}</p>
                    <p><strong>Email:</strong> {lead.email}</p>
                    <p><strong>Phone:</strong> {lead.phone}</p>
                    <p><strong>Business Type:</strong> {lead.business_type}</p>
                    <p><strong>Date:</strong> {lead.lead_date}</p>
                    <p><strong>Source:</strong> {lead.source or 'Direct'}</p>
                </div>
                
                {f'<div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;"><h4 style="color: #856404; margin-top: 0;">Message from Lead:</h4><p style="font-style: italic;">{lead.message}</p></div>' if lead.message else ''}
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{frappe.utils.get_url()}/app/shop-lead/{lead.name}" 
                       style="background-color: #3498db; color: white; padding: 12px 25px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        📋 View Lead Details
                    </a>
                </div>
            </div>
            """,
            delayed=False
        )
        
        # Also create a notification in the system
        frappe.get_doc({
            "doctype": "Notification Log",
            "subject": f"New Shop Lead: {shop.shop_name}",
            "for_user": admin_emails,
            "type": "Alert",
            "document_type": "Shop Lead",
            "document_name": lead.name
        }).insert(ignore_permissions=True)
        
    except Exception as e:
        frappe.log_error(f"Failed to send admin notification for lead {lead.name}: {str(e)}")

def send_lead_confirmation(lead):
    """Send confirmation email to the lead"""
    try:
        shop = frappe.get_doc("Airport Shop", lead.shop)
        
        company_name = frappe.db.get_single_value("Global Defaults", "default_company") or "Airport Management"
        contact_email = frappe.db.get_single_value("System Settings", "auto_email_id") or "admin@airport.com"
        
        frappe.sendmail(
            recipients=[lead.email],
            subject=f"Thank you for your interest in {shop.shop_name}",
            message=f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0; font-size: 28px;">✈️ Thank You!</h1>
                    <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">
                        Your application has been received
                    </p>
                </div>
                
                <div style="padding: 30px; background-color: #ffffff; border: 1px solid #e0e0e0;">
                    <p style="font-size: 16px; color: #2c3e50; margin-bottom: 20px;">
                        Dear <strong>{lead.lead_name}</strong>,
                    </p>
                    
                    <p style="color: #34495e; line-height: 1.6;">
                        Thank you for your interest in <strong>{shop.shop_name}</strong> at our airport. 
                        We have received your application and our team will review it shortly.
                    </p>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0;">
                        <h3 style="color: #2980b9; margin-top: 0; margin-bottom: 15px;">📍 Shop Details</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px 0; color: #7f8c8d; width: 40%;">Shop Name:</td>
                                <td style="padding: 8px 0; color: #2c3e50; font-weight: bold;">{shop.shop_name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #7f8c8d;">Location:</td>
                                <td style="padding: 8px 0; color: #2c3e50;">{shop.location}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #7f8c8d;">Area:</td>
                                <td style="padding: 8px 0; color: #2c3e50;">{shop.area_sqft} sq ft</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #7f8c8d;">Monthly Rent:</td>
                                <td style="padding: 8px 0; color: #27ae60; font-weight: bold; font-size: 18px;">₹{shop.total_monthly_rent:,.2f}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <div style="background-color: #e8f5e8; padding: 20px; border-radius: 8px; margin: 25px 0;">
                        <h3 style="color: #27ae60; margin-top: 0; margin-bottom: 10px;">⏰ What's Next?</h3>
                        <ul style="color: #2c3e50; padding-left: 20px; line-height: 1.8;">
                            <li>Our team will review your application within <strong>24 hours</strong></li>
                            <li>We'll contact you to discuss terms and conditions</li>
                            <li>If approved, we'll schedule a site visit</li>
                            <li>Contract signing and key handover</li>
                        </ul>
                    </div>
                    
                    <div style="border-top: 2px solid #ecf0f1; padding-top: 20px; margin-top: 30px;">
                        <h3 style="color: #2c3e50; margin-bottom: 15px;">📞 Need Immediate Assistance?</h3>
                        <p style="color: #7f8c8d; margin: 5px 0;">Email: <a href="mailto:{contact_email}" style="color: #3498db;">{contact_email}</a></p>
                        <p style="color: #7f8c8d; margin: 5px 0;">Phone: +91-80-12345678</p>
                        <p style="color: #7f8c8d; margin: 5px 0;">Business Hours: 9:00 AM - 6:00 PM (Mon-Sat)</p>
                    </div>
                </div>
                
                <div style="background-color: #34495e; color: #ecf0f1; padding: 20px; 
                            text-align: center; border-radius: 0 0 10px 10px;">
                    <p style="margin: 0; font-size: 14px;">
                        Best regards,<br>
                        <strong>{company_name} Team</strong>
                    </p>
                    <p style="margin: 10px 0 0 0; font-size: 12px; opacity: 0.8;">
                        This is an automated message. Please do not reply to this email.
                    </p>
                </div>
            </div>
            """,
            delayed=False
        )
        
    except Exception as e:
        frappe.log_error(f"Failed to send confirmation email to lead {lead.name}: {str(e)}")

@frappe.whitelist()
def send_follow_up_email(lead_name, message_type="follow_up"):
    """Send follow-up emails to leads"""
    
    lead = frappe.get_doc("Shop Lead", lead_name)
    
    if message_type == "follow_up":
        subject = f"Following up on your interest in {lead.shop}"
        message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Following up on your inquiry</h2>
            
            <p>Dear {lead.lead_name},</p>
            
            <p>We wanted to follow up on your recent inquiry about our airport shop at {lead.shop}.</p>
            
            <p>Our team is ready to discuss the opportunity with you. Would you be available for a call this week?</p>
            
            <p>Please let us know your preferred time, and we'll arrange a discussion.</p>
            
            <p>Best regards,<br>Airport Management Team</p>
        </div>
        """
    elif message_type == "reminder":
        subject = f"Reminder: Your application for {lead.shop}"
        message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Application Reminder</h2>
            
            <p>Dear {lead.lead_name},</p>
            
            <p>This is a gentle reminder about your application for {lead.shop}.</p>
            
            <p>If you're still interested, please let us know so we can proceed with the next steps.</p>
            
            <p>Best regards,<br>Airport Management Team</p>
        </div>
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

@frappe.whitelist()
def bulk_email_leads(lead_names, email_template, subject):
    """Send bulk emails to multiple leads"""
    
    if isinstance(lead_names, str):
        lead_names = json.loads(lead_names)
    
    success_count = 0
    failed_count = 0
    
    for lead_name in lead_names:
        try:
            lead = frappe.get_doc("Shop Lead", lead_name)
            
            frappe.sendmail(
                recipients=[lead.email],
                subject=subject,
                message=email_template.format(lead_name=lead.lead_name, shop=lead.shop)
            )
            
            # Add comment to lead
            frappe.get_doc({
                "doctype": "Comment",
                "comment_type": "Comment",
                "reference_doctype": "Shop Lead",
                "reference_name": lead_name,
                "content": f"Bulk email sent: {subject}"
            }).insert(ignore_permissions=True)
            
            success_count += 1
            
        except Exception as e:
            frappe.log_error(f"Failed to send bulk email to lead {lead_name}: {str(e)}")
            failed_count += 1
    
    return {
        "status": "success",
        "message": f"Bulk email completed. {success_count} sent, {failed_count} failed.",
        "success_count": success_count,
        "failed_count": failed_count
    }
