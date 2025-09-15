import frappe
from frappe import _
from frappe.utils import getdate, add_days, format_date
from frappe.utils.pdf import get_pdf
import json


def send_weekly_reports():
    """
    Send weekly reports to relevant stakeholders
    Scheduled to run weekly via hooks.py
    """
    try:
        frappe.log_error("Starting weekly report automation", "Report Automation")
        
        # Send occupancy report to management
        send_occupancy_report()
        
        # Send revenue summary to finance team
        send_revenue_summary()
        
        # Send contract expiry alerts
        send_contract_expiry_alerts()
        
        # Send lead summary to sales team
        send_lead_summary()
        
        frappe.log_error("Weekly reports sent successfully", "Report Automation")
        
    except Exception as e:
        frappe.log_error(f"Weekly report automation failed: {str(e)}", "Report Automation Error")


def send_occupancy_report():
    """
    Send shop occupancy report to airport management
    """
    try:
        # Get occupancy data
        occupancy_data = get_occupancy_data()
        
        # Get recipients
        recipients = get_report_recipients("occupancy")
        
        if not recipients:
            frappe.log_error("No recipients found for occupancy report", "Report Automation")
            return
        
        # Generate report content
        subject = f"Weekly Shop Occupancy Report - {format_date(getdate())}"
        
        template_data = {
            "total_shops": occupancy_data.get("total_shops", 0),
            "occupied_shops": occupancy_data.get("occupied_shops", 0),
            "occupancy_rate": occupancy_data.get("occupancy_rate", 0),
            "available_shops": occupancy_data.get("available_shops", 0),
            "shop_breakdown": occupancy_data.get("shop_breakdown", []),
            "report_date": format_date(getdate())
        }
        
        # Send email with report
        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            template="weekly_occupancy_report",
            args=template_data,
            attachments=[]
        )
        
        frappe.log_error(f"Occupancy report sent to {len(recipients)} recipients", "Report Automation")
        
    except Exception as e:
        frappe.log_error(f"Occupancy report sending failed: {str(e)}", "Report Automation Error")


def send_revenue_summary():
    """
    Send revenue summary to finance team
    """
    try:
        # Get revenue data for the past week
        end_date = getdate()
        start_date = add_days(end_date, -7)
        
        revenue_data = get_revenue_data(start_date, end_date)
        
        # Get recipients
        recipients = get_report_recipients("revenue")
        
        if not recipients:
            frappe.log_error("No recipients found for revenue report", "Report Automation")
            return
        
        # Generate report content
        subject = f"Weekly Revenue Summary - {format_date(start_date)} to {format_date(end_date)}"
        
        template_data = {
            "total_revenue": revenue_data.get("total_revenue", 0),
            "collected_amount": revenue_data.get("collected_amount", 0),
            "outstanding_amount": revenue_data.get("outstanding_amount", 0),
            "collection_efficiency": revenue_data.get("collection_efficiency", 0),
            "payment_breakdown": revenue_data.get("payment_breakdown", []),
            "start_date": format_date(start_date),
            "end_date": format_date(end_date)
        }
        
        # Send email with report
        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            template="weekly_revenue_summary",
            args=template_data
        )
        
        frappe.log_error(f"Revenue summary sent to {len(recipients)} recipients", "Report Automation")
        
    except Exception as e:
        frappe.log_error(f"Revenue summary sending failed: {str(e)}", "Report Automation Error")


def send_contract_expiry_alerts():
    """
    Send contract expiry alerts to management
    """
    try:
        # Get contracts expiring in next 30 days
        expiring_contracts = get_expiring_contracts()
        
        if not expiring_contracts:
            frappe.log_error("No expiring contracts found", "Report Automation")
            return
        
        # Get recipients
        recipients = get_report_recipients("contracts")
        
        if not recipients:
            frappe.log_error("No recipients found for contract expiry alerts", "Report Automation")
            return
        
        # Generate alert content
        subject = f"Contract Expiry Alert - {len(expiring_contracts)} contracts expiring soon"
        
        template_data = {
            "expiring_contracts": expiring_contracts,
            "total_expiring": len(expiring_contracts),
            "alert_date": format_date(getdate())
        }
        
        # Send email with alert
        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            template="contract_expiry_alert",
            args=template_data
        )
        
        frappe.log_error(f"Contract expiry alerts sent for {len(expiring_contracts)} contracts", "Report Automation")
        
    except Exception as e:
        frappe.log_error(f"Contract expiry alert sending failed: {str(e)}", "Report Automation Error")


def send_lead_summary():
    """
    Send lead summary to sales team
    """
    try:
        # Get lead data for the past week
        end_date = getdate()
        start_date = add_days(end_date, -7)
        
        lead_data = get_lead_data(start_date, end_date)
        
        # Get recipients
        recipients = get_report_recipients("leads")
        
        if not recipients:
            frappe.log_error("No recipients found for lead summary", "Report Automation")
            return
        
        # Generate report content
        subject = f"Weekly Lead Summary - {format_date(start_date)} to {format_date(end_date)}"
        
        template_data = {
            "new_leads": lead_data.get("new_leads", 0),
            "converted_leads": lead_data.get("converted_leads", 0),
            "pending_leads": lead_data.get("pending_leads", 0),
            "conversion_rate": lead_data.get("conversion_rate", 0),
            "lead_details": lead_data.get("lead_details", []),
            "start_date": format_date(start_date),
            "end_date": format_date(end_date)
        }
        
        # Send email with report
        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            template="weekly_lead_summary",
            args=template_data
        )
        
        frappe.log_error(f"Lead summary sent to {len(recipients)} recipients", "Report Automation")
        
    except Exception as e:
        frappe.log_error(f"Lead summary sending failed: {str(e)}", "Report Automation Error")


def get_occupancy_data():
    """
    Get current occupancy data
    """
    try:
        # Total shops
        total_shops = frappe.db.count("Airport Shop")
        
        # Occupied shops
        occupied_shops = frappe.db.sql("""
            SELECT COUNT(DISTINCT cs.shop) as count
            FROM `tabContract Shop` cs
            WHERE cs.status = 'Active'
            AND cs.contract_start_date <= CURDATE()
            AND cs.contract_end_date >= CURDATE()
        """, as_dict=True)[0].count or 0
        
        # Calculate rates
        occupancy_rate = (occupied_shops / total_shops * 100) if total_shops > 0 else 0
        available_shops = total_shops - occupied_shops
        
        # Shop breakdown by type
        shop_breakdown = frappe.db.sql("""
            SELECT 
                st.shop_type_name,
                COUNT(asp.name) as total_shops,
                COUNT(cs.shop) as occupied_shops,
                (COUNT(cs.shop) / COUNT(asp.name) * 100) as occupancy_rate
            FROM `tabShop Type` st
            LEFT JOIN `tabAirport Shop` asp ON st.name = asp.shop_type
            LEFT JOIN `tabContract Shop` cs ON asp.name = cs.shop 
                AND cs.status = 'Active'
                AND cs.contract_start_date <= CURDATE()
                AND cs.contract_end_date >= CURDATE()
            GROUP BY st.shop_type_name
        """, as_dict=True)
        
        return {
            "total_shops": total_shops,
            "occupied_shops": occupied_shops,
            "occupancy_rate": occupancy_rate,
            "available_shops": available_shops,
            "shop_breakdown": shop_breakdown
        }
        
    except Exception as e:
        frappe.log_error(f"Occupancy data retrieval failed: {str(e)}", "Report Automation Error")
        return {}


def get_revenue_data(start_date, end_date):
    """
    Get revenue data for specified period
    """
    try:
        # Total revenue
        total_revenue = frappe.db.sql("""
            SELECT COALESCE(SUM(si.grand_total), 0) as amount
            FROM `tabSales Invoice` si
            WHERE si.posting_date BETWEEN %s AND %s
            AND si.docstatus = 1
        """, (start_date, end_date), as_dict=True)[0].amount or 0
        
        # Collected amount
        collected_amount = frappe.db.sql("""
            SELECT COALESCE(SUM(si.grand_total - si.outstanding_amount), 0) as amount
            FROM `tabSales Invoice` si
            WHERE si.posting_date BETWEEN %s AND %s
            AND si.docstatus = 1
        """, (start_date, end_date), as_dict=True)[0].amount or 0
        
        # Outstanding amount
        outstanding_amount = total_revenue - collected_amount
        
        # Collection efficiency
        collection_efficiency = (collected_amount / total_revenue * 100) if total_revenue > 0 else 0
        
        # Payment breakdown
        payment_breakdown = frappe.db.sql("""
            SELECT 
                si.customer,
                si.grand_total,
                si.outstanding_amount,
                (si.grand_total - si.outstanding_amount) as paid_amount
            FROM `tabSales Invoice` si
            WHERE si.posting_date BETWEEN %s AND %s
            AND si.docstatus = 1
            ORDER BY si.grand_total DESC
        """, (start_date, end_date), as_dict=True)
        
        return {
            "total_revenue": total_revenue,
            "collected_amount": collected_amount,
            "outstanding_amount": outstanding_amount,
            "collection_efficiency": collection_efficiency,
            "payment_breakdown": payment_breakdown
        }
        
    except Exception as e:
        frappe.log_error(f"Revenue data retrieval failed: {str(e)}", "Report Automation Error")
        return {}


def get_expiring_contracts():
    """
    Get contracts expiring in next 30 days
    """
    try:
        today = getdate()
        thirty_days_later = add_days(today, 30)
        
        expiring_contracts = frappe.db.sql("""
            SELECT 
                cs.name,
                cs.tenant_name,
                cs.shop,
                cs.contract_end_date,
                DATEDIFF(cs.contract_end_date, CURDATE()) as days_remaining,
                asp.shop_name,
                cs.monthly_rent
            FROM `tabContract Shop` cs
            INNER JOIN `tabAirport Shop` asp ON cs.shop = asp.name
            WHERE cs.status = 'Active'
            AND cs.contract_end_date BETWEEN CURDATE() AND %s
            ORDER BY cs.contract_end_date ASC
        """, (thirty_days_later,), as_dict=True)
        
        return expiring_contracts
        
    except Exception as e:
        frappe.log_error(f"Expiring contracts retrieval failed: {str(e)}", "Report Automation Error")
        return []


def get_lead_data(start_date, end_date):
    """
    Get lead data for specified period
    """
    try:
        # New leads
        new_leads = frappe.db.sql("""
            SELECT COUNT(*) as count
            FROM `tabShop Lead` sl
            WHERE sl.creation BETWEEN %s AND %s
        """, (start_date, end_date), as_dict=True)[0].count or 0
        
        # Converted leads
        converted_leads = frappe.db.sql("""
            SELECT COUNT(DISTINCT sl.name) as count
            FROM `tabShop Lead` sl
            INNER JOIN `tabContract Shop` cs ON sl.email = cs.tenant_email
            WHERE sl.creation BETWEEN %s AND %s
            AND cs.docstatus = 1
        """, (start_date, end_date), as_dict=True)[0].count or 0
        
        # Pending leads
        pending_leads = frappe.db.count("Shop Lead", {
            "status": "Open",
            "creation": ["between", [start_date, end_date]]
        })
        
        # Conversion rate
        conversion_rate = (converted_leads / new_leads * 100) if new_leads > 0 else 0
        
        # Lead details
        lead_details = frappe.db.sql("""
            SELECT 
                sl.lead_name,
                sl.email,
                sl.phone,
                sl.preferred_shop_type,
                sl.status,
                sl.creation
            FROM `tabShop Lead` sl
            WHERE sl.creation BETWEEN %s AND %s
            ORDER BY sl.creation DESC
        """, (start_date, end_date), as_dict=True)
        
        return {
            "new_leads": new_leads,
            "converted_leads": converted_leads,
            "pending_leads": pending_leads,
            "conversion_rate": conversion_rate,
            "lead_details": lead_details
        }
        
    except Exception as e:
        frappe.log_error(f"Lead data retrieval failed: {str(e)}", "Report Automation Error")
        return {}


def get_report_recipients(report_type):
    """
    Get email recipients for different report types
    """
    try:
        recipients = []
        
        if report_type == "occupancy":
            # Airport managers and shop managers
            recipients = frappe.get_all(
                "User",
                filters={"enabled": 1},
                fields=["email"]
            )
            # Filter users with appropriate roles
            filtered_recipients = []
            for user in recipients:
                user_roles = frappe.get_roles(user.email)
                if "Airport Manager" in user_roles or "Shop Manager" in user_roles:
                    filtered_recipients.append(user.email)
            recipients = filtered_recipients
            
        elif report_type == "revenue":
            # Finance team and airport managers
            recipients = frappe.get_all(
                "User", 
                filters={"enabled": 1},
                fields=["email"]
            )
            filtered_recipients = []
            for user in recipients:
                user_roles = frappe.get_roles(user.email)
                if "Airport Manager" in user_roles or "Accounts Manager" in user_roles:
                    filtered_recipients.append(user.email)
            recipients = filtered_recipients
            
        elif report_type == "contracts":
            # Airport managers and shop managers
            recipients = frappe.get_all(
                "User",
                filters={"enabled": 1}, 
                fields=["email"]
            )
            filtered_recipients = []
            for user in recipients:
                user_roles = frappe.get_roles(user.email)
                if "Airport Manager" in user_roles or "Shop Manager" in user_roles:
                    filtered_recipients.append(user.email)
            recipients = filtered_recipients
            
        elif report_type == "leads":
            # Sales team and shop managers
            recipients = frappe.get_all(
                "User",
                filters={"enabled": 1},
                fields=["email"]
            )
            filtered_recipients = []
            for user in recipients:
                user_roles = frappe.get_roles(user.email)
                if "Shop Manager" in user_roles or "Sales User" in user_roles:
                    filtered_recipients.append(user.email)
            recipients = filtered_recipients
        
        # Fallback to administrator if no specific recipients found
        if not recipients:
            recipients = ["administrator@example.com"]
        
        return recipients
        
    except Exception as e:
        frappe.log_error(f"Recipients retrieval failed: {str(e)}", "Report Automation Error")
        return []


@frappe.whitelist()
def generate_manual_report(report_type, start_date=None, end_date=None):
    """
    Generate reports manually on demand
    """
    try:
        if not start_date:
            start_date = add_days(getdate(), -7)
        if not end_date:
            end_date = getdate()
        
        if report_type == "occupancy":
            return get_occupancy_data()
        elif report_type == "revenue":
            return get_revenue_data(start_date, end_date)
        elif report_type == "contracts":
            return get_expiring_contracts()
        elif report_type == "leads":
            return get_lead_data(start_date, end_date)
        else:
            frappe.throw(_("Invalid report type"))
            
    except Exception as e:
        frappe.log_error(f"Manual report generation failed: {str(e)}", "Report Automation Error")
        frappe.throw(_("Report generation failed"))
