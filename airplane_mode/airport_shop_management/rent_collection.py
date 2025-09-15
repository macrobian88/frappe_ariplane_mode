import frappe
from frappe import _
from frappe.utils import nowdate, add_months, getdate, today, cint
import json

def process_monthly_invoices():
    """Process monthly rent invoices for all active contracts"""
    
    today_date = getdate(today())
    
    # Get contracts that need invoicing (due date is today or past)
    contracts = frappe.db.sql("""
        SELECT name, customer, shop, monthly_rent, start_date, end_date
        FROM `tabContract Shop`
        WHERE docstatus = 1
        AND end_date >= %s
        AND (next_invoice_date <= %s OR next_invoice_date IS NULL)
    """, (today_date, today_date), as_dict=True)
    
    processed_count = 0
    failed_count = 0
    
    for contract in contracts:
        try:
            create_monthly_invoice(contract)
            processed_count += 1
        except Exception as e:
            frappe.log_error(f"Failed to create invoice for contract {contract.name}: {str(e)}")
            failed_count += 1
    
    # Log summary
    frappe.logger().info(f"Monthly invoice processing completed. Processed: {processed_count}, Failed: {failed_count}")
    
    return {
        "processed": processed_count,
        "failed": failed_count,
        "total": len(contracts)
    }

def create_monthly_invoice(contract):
    """Create monthly rent invoice for a contract"""
    
    # Check if invoice already exists for this month
    current_month = getdate(today()).replace(day=1)
    existing_invoice = frappe.db.exists("Sales Invoice", {
        "customer": contract.customer,
        "custom_contract_shop": contract.name,
        "posting_date": [">=", current_month],
        "posting_date": ["<", add_months(current_month, 1)]
    })
    
    if existing_invoice:
        return existing_invoice
    
    # Get customer details
    customer = frappe.get_doc("Customer", contract.customer)
    
    # Create Sales Invoice
    invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": contract.customer,
        "posting_date": today(),
        "due_date": add_months(today(), 1),
        "custom_contract_shop": contract.name,
        "custom_shop": contract.shop,
        "items": [{
            "item_code": "Shop Rent",
            "item_name": f"Monthly Rent - {contract.shop}",
            "description": f"Monthly rent for shop {contract.shop} as per contract {contract.name}",
            "qty": 1,
            "rate": contract.monthly_rent,
            "amount": contract.monthly_rent
        }],
        "taxes_and_charges": "",
        "tc_name": "Standard Terms and Conditions"
    })
    
    invoice.insert()
    invoice.submit()
    
    # Update contract next invoice date
    frappe.db.set_value("Contract Shop", contract.name, 
                        "next_invoice_date", add_months(today(), 1))
    
    # Send invoice email
    send_invoice_email(invoice, contract)
    
    return invoice.name

def send_invoice_email(invoice, contract):
    """Send invoice email to customer"""
    try:
        frappe.sendmail(
            recipients=[invoice.contact_email or invoice.customer],
            subject=f"Monthly Rent Invoice - {contract.shop}",
            message=f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0; font-size: 24px;">📄 Monthly Rent Invoice</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">Invoice #{invoice.name}</p>
                </div>
                
                <div style="padding: 30px; background-color: #ffffff; border: 1px solid #e0e0e0;">
                    <p style="font-size: 16px; color: #2c3e50; margin-bottom: 20px;">
                        Dear Valued Customer,
                    </p>
                    
                    <p style="color: #34495e; line-height: 1.6;">
                        Please find your monthly rent invoice details below:
                    </p>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #2980b9; margin-top: 0;">Invoice Details</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px 0; color: #7f8c8d; width: 40%;">Invoice Number:</td>
                                <td style="padding: 8px 0; color: #2c3e50; font-weight: bold;">{invoice.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #7f8c8d;">Shop:</td>
                                <td style="padding: 8px 0; color: #2c3e50;">{contract.shop}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #7f8c8d;">Amount:</td>
                                <td style="padding: 8px 0; color: #27ae60; font-weight: bold; font-size: 18px;">₹{invoice.grand_total:,.2f}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #7f8c8d;">Due Date:</td>
                                <td style="padding: 8px 0; color: #e74c3c; font-weight: bold;">{invoice.due_date}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #7f8c8d;">Invoice Date:</td>
                                <td style="padding: 8px 0; color: #2c3e50;">{invoice.posting_date}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h4 style="color: #856404; margin-top: 0;">⚠️ Important Notice</h4>
                        <p style="color: #856404; margin: 0;">
                            Please ensure payment is made by the due date to avoid any late fees or penalties.
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{frappe.utils.get_url()}/app/sales-invoice/{invoice.name}" 
                           style="background-color: #3498db; color: white; padding: 12px 25px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            📋 View Invoice Details
                        </a>
                    </div>
                    
                    <div style="border-top: 2px solid #ecf0f1; padding-top: 20px; margin-top: 30px;">
                        <h3 style="color: #2c3e50; margin-bottom: 15px;">💳 Payment Methods</h3>
                        <p style="color: #7f8c8d; margin: 5px 0;">• Bank Transfer</p>
                        <p style="color: #7f8c8d; margin: 5px 0;">• Online Payment Portal</p>
                        <p style="color: #7f8c8d; margin: 5px 0;">• Cash Payment at Office</p>
                    </div>
                </div>
                
                <div style="background-color: #34495e; color: #ecf0f1; padding: 20px; 
                            text-align: center; border-radius: 0 0 10px 10px;">
                    <p style="margin: 0; font-size: 14px;">
                        Thank you for your business!<br>
                        <strong>Airport Management Team</strong>
                    </p>
                    <p style="margin: 10px 0 0 0; font-size: 12px; opacity: 0.8;">
                        For any queries, contact us at admin@airport.com
                    </p>
                </div>
            </div>
            """,
            attachments=[frappe.attach_print("Sales Invoice", invoice.name, file_name=f"Invoice-{invoice.name}.pdf")]
        )
        
    except Exception as e:
        frappe.log_error(f"Failed to send invoice email for {invoice.name}: {str(e)}")

@frappe.whitelist()
def generate_manual_invoice(contract_name):
    """Manually generate invoice for a contract"""
    
    contract = frappe.get_doc("Contract Shop", contract_name)
    if contract.docstatus != 1:
        frappe.throw(_("Contract must be submitted to generate invoice"))
    
    invoice_name = create_monthly_invoice(contract.as_dict())
    
    return {
        "status": "success",
        "invoice": invoice_name,
        "message": _("Invoice generated successfully")
    }

def send_rent_reminders():
    """Send rent reminder emails for overdue invoices"""
    
    # Get overdue invoices
    overdue_invoices = frappe.db.sql("""
        SELECT 
            si.name, si.customer, si.due_date, si.outstanding_amount,
            cs.shop, cs.name as contract_name
        FROM `tabSales Invoice` si
        LEFT JOIN `tabContract Shop` cs ON cs.name = si.custom_contract_shop
        WHERE si.docstatus = 1
        AND si.outstanding_amount > 0
        AND si.due_date < CURDATE()
        AND si.customer IN (
            SELECT DISTINCT customer 
            FROM `tabContract Shop` 
            WHERE docstatus = 1
        )
        ORDER BY si.due_date ASC
    """, as_dict=True)
    
    reminder_count = 0
    
    for invoice in overdue_invoices:
        try:
            send_overdue_reminder(invoice)
            reminder_count += 1
        except Exception as e:
            frappe.log_error(f"Failed to send reminder for invoice {invoice.name}: {str(e)}")
    
    frappe.logger().info(f"Sent {reminder_count} rent reminder emails")
    
    return {
        "reminders_sent": reminder_count,
        "total_overdue": len(overdue_invoices)
    }

def send_overdue_reminder(invoice_info):
    """Send overdue payment reminder email"""
    
    customer = frappe.get_doc("Customer", invoice_info.customer)
    days_overdue = (getdate(today()) - getdate(invoice_info.due_date)).days
    
    frappe.sendmail(
        recipients=[customer.email_id or customer.name],
        subject=f"Payment Reminder - Overdue Invoice {invoice_info.name}",
        message=f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); 
                        color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="margin: 0; font-size: 24px;">⚠️ Payment Reminder</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">{days_overdue} days overdue</p>
            </div>
            
            <div style="padding: 30px; background-color: #ffffff; border: 1px solid #e0e0e0;">
                <p style="font-size: 16px; color: #2c3e50; margin-bottom: 20px;">
                    Dear {customer.customer_name},
                </p>
                
                <p style="color: #34495e; line-height: 1.6;">
                    This is a reminder that your rent payment is now <strong>{days_overdue} days overdue</strong>.
                </p>
                
                <div style="background-color: #f8d7da; padding: 20px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #dc3545;">
                    <h3 style="color: #721c24; margin-top: 0;">Overdue Invoice Details</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; color: #7f8c8d; width: 40%;">Invoice Number:</td>
                            <td style="padding: 8px 0; color: #2c3e50; font-weight: bold;">{invoice_info.name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #7f8c8d;">Shop:</td>
                            <td style="padding: 8px 0; color: #2c3e50;">{invoice_info.shop}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #7f8c8d;">Due Date:</td>
                            <td style="padding: 8px 0; color: #e74c3c; font-weight: bold;">{invoice_info.due_date}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #7f8c8d;">Outstanding Amount:</td>
                            <td style="padding: 8px 0; color: #e74c3c; font-weight: bold; font-size: 18px;">₹{invoice_info.outstanding_amount:,.2f}</td>
                        </tr>
                    </table>
                </div>
                
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h4 style="color: #856404; margin-top: 0;">🚨 Immediate Action Required</h4>
                    <p style="color: #856404; margin: 0;">
                        Please make the payment immediately to avoid late fees and potential contract termination.
                    </p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{frappe.utils.get_url()}/app/sales-invoice/{invoice_info.name}" 
                       style="background-color: #e74c3c; color: white; padding: 12px 25px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        💳 Pay Now
                    </a>
                </div>
            </div>
            
            <div style="background-color: #34495e; color: #ecf0f1; padding: 20px; 
                        text-align: center; border-radius: 0 0 10px 10px;">
                <p style="margin: 0; font-size: 14px;">
                    For payment assistance, contact us immediately<br>
                    <strong>Email: admin@airport.com | Phone: +91-80-12345678</strong>
                </p>
            </div>
        </div>
        """,
        delayed=False
    )

@frappe.whitelist()
def get_rent_collection_summary():
    """Get summary of rent collection status"""
    
    # Current month collections
    current_month_collected = frappe.db.sql("""
        SELECT SUM(paid_amount) as collected
        FROM `tabSales Invoice`
        WHERE docstatus = 1
        AND MONTH(posting_date) = MONTH(CURDATE())
        AND YEAR(posting_date) = YEAR(CURDATE())
        AND customer IN (
            SELECT DISTINCT customer 
            FROM `tabContract Shop` 
            WHERE docstatus = 1
        )
    """)[0][0] or 0
    
    # Outstanding amount
    outstanding_amount = frappe.db.sql("""
        SELECT SUM(outstanding_amount) as outstanding
        FROM `tabSales Invoice`
        WHERE docstatus = 1
        AND outstanding_amount > 0
        AND customer IN (
            SELECT DISTINCT customer 
            FROM `tabContract Shop` 
            WHERE docstatus = 1
        )
    """)[0][0] or 0
    
    # Overdue invoices
    overdue_count = frappe.db.sql("""
        SELECT COUNT(*) as count
        FROM `tabSales Invoice`
        WHERE docstatus = 1
        AND outstanding_amount > 0
        AND due_date < CURDATE()
        AND customer IN (
            SELECT DISTINCT customer 
            FROM `tabContract Shop` 
            WHERE docstatus = 1
        )
    """)[0][0] or 0
    
    return {
        "current_month_collected": current_month_collected,
        "outstanding_amount": outstanding_amount,
        "overdue_count": overdue_count,
        "collection_rate": round((current_month_collected / (current_month_collected + outstanding_amount) * 100), 2) if (current_month_collected + outstanding_amount) > 0 else 0
    }
