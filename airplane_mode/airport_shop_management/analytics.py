import frappe
from frappe import _
from frappe.utils import getdate, add_months
import calendar


def update_monthly_metrics():
    """
    Update monthly analytics and metrics for airport shop management
    Scheduled to run monthly via hooks.py
    """
    try:
        frappe.log_error("Starting monthly metrics update", "Analytics")
        
        current_date = getdate()
        current_month = current_date.month
        current_year = current_date.year
        
        # Update shop occupancy metrics
        update_shop_occupancy_metrics(current_year, current_month)
        
        # Update revenue metrics
        update_revenue_metrics(current_year, current_month)
        
        # Update contract metrics
        update_contract_metrics(current_year, current_month)
        
        # Update lead conversion metrics
        update_lead_metrics(current_year, current_month)
        
        frappe.log_error("Monthly metrics update completed successfully", "Analytics")
        
    except Exception as e:
        frappe.log_error(f"Monthly metrics update failed: {str(e)}", "Analytics Error")


def update_shop_occupancy_metrics(year, month):
    """
    Update shop occupancy statistics
    """
    try:
        # Get total shops
        total_shops = frappe.db.count("Airport Shop")
        
        # Get occupied shops (with active contracts)
        occupied_shops = frappe.db.sql("""
            SELECT COUNT(DISTINCT cs.shop) as occupied_count
            FROM `tabContract Shop` cs 
            WHERE cs.status = 'Active'
            AND cs.contract_start_date <= CURDATE()
            AND cs.contract_end_date >= CURDATE()
        """, as_dict=True)[0].occupied_count or 0
        
        # Calculate occupancy rate
        occupancy_rate = (occupied_shops / total_shops * 100) if total_shops > 0 else 0
        
        # Create or update metrics record
        metrics_doc = get_or_create_monthly_metrics(year, month)
        metrics_doc.total_shops = total_shops
        metrics_doc.occupied_shops = occupied_shops
        metrics_doc.occupancy_rate = occupancy_rate
        metrics_doc.available_shops = total_shops - occupied_shops
        metrics_doc.save()
        
        frappe.log_error(f"Shop occupancy metrics updated: {occupancy_rate}% occupancy", "Analytics")
        
    except Exception as e:
        frappe.log_error(f"Shop occupancy metrics update failed: {str(e)}", "Analytics Error")


def update_revenue_metrics(year, month):
    """
    Update revenue analytics
    """
    try:
        # Get start and end dates for the month
        start_date = getdate(f"{year}-{month:02d}-01")
        last_day = calendar.monthrange(year, month)[1]
        end_date = getdate(f"{year}-{month:02d}-{last_day}")
        
        # Calculate monthly revenue from invoices
        monthly_revenue = frappe.db.sql("""
            SELECT COALESCE(SUM(si.grand_total), 0) as total_revenue
            FROM `tabSales Invoice` si
            WHERE si.posting_date BETWEEN %s AND %s
            AND si.docstatus = 1
            AND si.customer_group = 'Airport Tenant'
        """, (start_date, end_date), as_dict=True)[0].total_revenue or 0
        
        # Calculate pending revenue (unpaid invoices)
        pending_revenue = frappe.db.sql("""
            SELECT COALESCE(SUM(si.outstanding_amount), 0) as pending_amount
            FROM `tabSales Invoice` si
            WHERE si.outstanding_amount > 0
            AND si.docstatus = 1
            AND si.customer_group = 'Airport Tenant'
        """, as_dict=True)[0].pending_amount or 0
        
        # Update metrics
        metrics_doc = get_or_create_monthly_metrics(year, month)
        metrics_doc.monthly_revenue = monthly_revenue
        metrics_doc.pending_revenue = pending_revenue
        metrics_doc.collection_efficiency = ((monthly_revenue - pending_revenue) / monthly_revenue * 100) if monthly_revenue > 0 else 0
        metrics_doc.save()
        
        frappe.log_error(f"Revenue metrics updated: {monthly_revenue} monthly revenue", "Analytics")
        
    except Exception as e:
        frappe.log_error(f"Revenue metrics update failed: {str(e)}", "Analytics Error")


def update_contract_metrics(year, month):
    """
    Update contract-related metrics
    """
    try:
        # Get contracts expiring in next 30 days
        expiring_contracts = frappe.db.sql("""
            SELECT COUNT(*) as expiring_count
            FROM `tabContract Shop` cs
            WHERE cs.status = 'Active'
            AND cs.contract_end_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
        """, as_dict=True)[0].expiring_count or 0
        
        # Get new contracts signed this month
        start_date = getdate(f"{year}-{month:02d}-01")
        last_day = calendar.monthrange(year, month)[1]
        end_date = getdate(f"{year}-{month:02d}-{last_day}")
        
        new_contracts = frappe.db.sql("""
            SELECT COUNT(*) as new_count
            FROM `tabContract Shop` cs
            WHERE cs.creation BETWEEN %s AND %s
            AND cs.docstatus = 1
        """, (start_date, end_date), as_dict=True)[0].new_count or 0
        
        # Get total active contracts
        active_contracts = frappe.db.count("Contract Shop", {"status": "Active"})
        
        # Update metrics
        metrics_doc = get_or_create_monthly_metrics(year, month)
        metrics_doc.expiring_contracts = expiring_contracts
        metrics_doc.new_contracts = new_contracts
        metrics_doc.active_contracts = active_contracts
        metrics_doc.save()
        
        frappe.log_error(f"Contract metrics updated: {new_contracts} new contracts", "Analytics")
        
    except Exception as e:
        frappe.log_error(f"Contract metrics update failed: {str(e)}", "Analytics Error")


def update_lead_metrics(year, month):
    """
    Update lead conversion metrics
    """
    try:
        # Get start and end dates for the month
        start_date = getdate(f"{year}-{month:02d}-01")
        last_day = calendar.monthrange(year, month)[1]
        end_date = getdate(f"{year}-{month:02d}-{last_day}")
        
        # Get new leads this month
        new_leads = frappe.db.sql("""
            SELECT COUNT(*) as new_leads_count
            FROM `tabShop Lead` sl
            WHERE sl.creation BETWEEN %s AND %s
        """, (start_date, end_date), as_dict=True)[0].new_leads_count or 0
        
        # Get converted leads (leads that resulted in contracts)
        converted_leads = frappe.db.sql("""
            SELECT COUNT(DISTINCT sl.name) as converted_count
            FROM `tabShop Lead` sl
            INNER JOIN `tabContract Shop` cs ON sl.email = cs.tenant_email
            WHERE sl.creation BETWEEN %s AND %s
            AND cs.docstatus = 1
        """, (start_date, end_date), as_dict=True)[0].converted_count or 0
        
        # Calculate conversion rate
        conversion_rate = (converted_leads / new_leads * 100) if new_leads > 0 else 0
        
        # Update metrics
        metrics_doc = get_or_create_monthly_metrics(year, month)
        metrics_doc.new_leads = new_leads
        metrics_doc.converted_leads = converted_leads
        metrics_doc.conversion_rate = conversion_rate
        metrics_doc.save()
        
        frappe.log_error(f"Lead metrics updated: {conversion_rate}% conversion rate", "Analytics")
        
    except Exception as e:
        frappe.log_error(f"Lead metrics update failed: {str(e)}", "Analytics Error")


def get_or_create_monthly_metrics(year, month):
    """
    Get existing monthly metrics document or create new one
    """
    metrics_name = f"METRICS-{year}-{month:02d}"
    
    if frappe.db.exists("Monthly Shop Metrics", metrics_name):
        return frappe.get_doc("Monthly Shop Metrics", metrics_name)
    else:
        # Create new metrics document
        metrics_doc = frappe.new_doc("Monthly Shop Metrics")
        metrics_doc.name = metrics_name
        metrics_doc.year = year
        metrics_doc.month = month
        metrics_doc.insert()
        return metrics_doc


@frappe.whitelist()
def get_dashboard_metrics(period="current_month"):
    """
    Get metrics for dashboard display
    """
    try:
        current_date = getdate()
        
        if period == "current_month":
            year = current_date.year
            month = current_date.month
        elif period == "last_month":
            last_month_date = add_months(current_date, -1)
            year = last_month_date.year
            month = last_month_date.month
        else:
            year = current_date.year
            month = current_date.month
        
        metrics_name = f"METRICS-{year}-{month:02d}"
        
        if frappe.db.exists("Monthly Shop Metrics", metrics_name):
            metrics = frappe.get_doc("Monthly Shop Metrics", metrics_name)
            return {
                "occupancy_rate": metrics.occupancy_rate or 0,
                "monthly_revenue": metrics.monthly_revenue or 0,
                "conversion_rate": metrics.conversion_rate or 0,
                "active_contracts": metrics.active_contracts or 0,
                "expiring_contracts": metrics.expiring_contracts or 0,
                "new_leads": metrics.new_leads or 0
            }
        else:
            # Return current data if no stored metrics
            return get_current_metrics()
            
    except Exception as e:
        frappe.log_error(f"Dashboard metrics retrieval failed: {str(e)}", "Analytics Error")
        return {}


def get_current_metrics():
    """
    Get current real-time metrics
    """
    try:
        # Current occupancy
        total_shops = frappe.db.count("Airport Shop")
        occupied_shops = frappe.db.sql("""
            SELECT COUNT(DISTINCT cs.shop) as count
            FROM `tabContract Shop` cs 
            WHERE cs.status = 'Active'
        """, as_dict=True)[0].count or 0
        
        occupancy_rate = (occupied_shops / total_shops * 100) if total_shops > 0 else 0
        
        # Current month revenue
        current_date = getdate()
        start_date = getdate(f"{current_date.year}-{current_date.month:02d}-01")
        
        monthly_revenue = frappe.db.sql("""
            SELECT COALESCE(SUM(si.grand_total), 0) as revenue
            FROM `tabSales Invoice` si
            WHERE si.posting_date >= %s
            AND si.docstatus = 1
        """, (start_date,), as_dict=True)[0].revenue or 0
        
        return {
            "occupancy_rate": occupancy_rate,
            "monthly_revenue": monthly_revenue,
            "active_contracts": frappe.db.count("Contract Shop", {"status": "Active"}),
            "new_leads": frappe.db.count("Shop Lead", {"status": "Open"})
        }
        
    except Exception as e:
        frappe.log_error(f"Current metrics retrieval failed: {str(e)}", "Analytics Error")
        return {}
