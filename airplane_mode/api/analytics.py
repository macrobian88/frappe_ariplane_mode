import frappe
from frappe import _
from frappe.utils import nowdate, add_months, getdate

@frappe.whitelist()
def get_shop_analytics(shop_id=None, date_range=None):
    """Get analytics data for shops"""
    
    filters = {}
    if shop_id:
        filters["shop"] = shop_id
    
    # Get lead analytics
    lead_data = frappe.db.sql("""
        SELECT 
            status,
            COUNT(*) as count,
            DATE_FORMAT(lead_date, '%Y-%m') as month
        FROM `tabShop Lead`
        WHERE lead_date >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
        GROUP BY status, month
        ORDER BY month DESC
    """, as_dict=True)
    
    # Get revenue analytics from contracts
    revenue_data = frappe.db.sql("""
        SELECT 
            DATE_FORMAT(start_date, '%Y-%m') as month,
            SUM(monthly_rent) as total_rent,
            COUNT(*) as active_contracts
        FROM `tabContract Shop`
        WHERE docstatus = 1
        AND start_date >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
        GROUP BY month
        ORDER BY month DESC
    """, as_dict=True)
    
    # Get shop occupancy
    occupancy_data = frappe.db.sql("""
        SELECT 
            s.shop_type,
            COUNT(*) as total_shops,
            SUM(CASE WHEN s.status = 'Occupied' THEN 1 ELSE 0 END) as occupied_shops,
            ROUND((SUM(CASE WHEN s.status = 'Occupied' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as occupancy_rate
        FROM `tabAirport Shop` s
        WHERE s.is_active = 1
        GROUP BY s.shop_type
    """, as_dict=True)
    
    return {
        "status": "success",
        "lead_analytics": lead_data,
        "revenue_analytics": revenue_data,
        "occupancy_analytics": occupancy_data
    }

@frappe.whitelist()
def get_revenue_trends():
    """Get monthly revenue trends"""
    
    revenue_trends = frappe.db.sql("""
        SELECT 
            DATE_FORMAT(creation, '%Y-%m') as month,
            SUM(grand_total) as revenue,
            COUNT(*) as invoice_count
        FROM `tabSales Invoice`
        WHERE docstatus = 1
        AND creation >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
        AND customer IN (
            SELECT DISTINCT customer 
            FROM `tabContract Shop` 
            WHERE docstatus = 1
        )
        GROUP BY month
        ORDER BY month ASC
    """, as_dict=True)
    
    return {
        "status": "success",
        "revenue_trends": revenue_trends
    }

@frappe.whitelist()
def get_occupancy_forecast():
    """Get occupancy forecast based on contract end dates"""
    
    ending_contracts = frappe.db.sql("""
        SELECT 
            DATE_FORMAT(end_date, '%Y-%m') as month,
            COUNT(*) as ending_contracts,
            SUM(monthly_rent) as revenue_at_risk
        FROM `tabContract Shop`
        WHERE docstatus = 1
        AND end_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 12 MONTH)
        GROUP BY month
        ORDER BY month ASC
    """, as_dict=True)
    
    return {
        "status": "success",
        "ending_contracts": ending_contracts
    }

@frappe.whitelist()
def get_lead_conversion_metrics():
    """Get lead conversion analytics"""
    
    conversion_data = frappe.db.sql("""
        SELECT 
            COUNT(*) as total_leads,
            SUM(CASE WHEN status = 'Converted' THEN 1 ELSE 0 END) as converted_leads,
            SUM(CASE WHEN status = 'Lost' THEN 1 ELSE 0 END) as lost_leads,
            SUM(CASE WHEN status IN ('New', 'Contacted', 'Interested') THEN 1 ELSE 0 END) as active_leads,
            ROUND((SUM(CASE WHEN status = 'Converted' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as conversion_rate
        FROM `tabShop Lead`
        WHERE lead_date >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
    """, as_dict=True)
    
    # Lead source analysis
    source_data = frappe.db.sql("""
        SELECT 
            COALESCE(source, 'Direct') as source,
            COUNT(*) as lead_count,
            SUM(CASE WHEN status = 'Converted' THEN 1 ELSE 0 END) as converted_count,
            ROUND((SUM(CASE WHEN status = 'Converted' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as conversion_rate
        FROM `tabShop Lead`
        WHERE lead_date >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
        GROUP BY source
        ORDER BY lead_count DESC
    """, as_dict=True)
    
    return {
        "status": "success",
        "conversion_metrics": conversion_data[0] if conversion_data else {},
        "source_analytics": source_data
    }

@frappe.whitelist()
def get_financial_summary():
    """Get financial summary for airport shop management"""
    
    # Current month revenue
    current_month_revenue = frappe.db.sql("""
        SELECT SUM(monthly_rent) as revenue
        FROM `tabContract Shop`
        WHERE docstatus = 1
        AND start_date <= CURDATE()
        AND end_date >= CURDATE()
    """)[0][0] or 0
    
    # Total revenue this year
    yearly_revenue = frappe.db.sql("""
        SELECT SUM(grand_total) as revenue
        FROM `tabSales Invoice`
        WHERE docstatus = 1
        AND YEAR(posting_date) = YEAR(CURDATE())
        AND customer IN (
            SELECT DISTINCT customer 
            FROM `tabContract Shop` 
            WHERE docstatus = 1
        )
    """)[0][0] or 0
    
    # Outstanding payments
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
    
    # Average shop rent
    avg_rent = frappe.db.sql("""
        SELECT AVG(monthly_rent) as avg_rent
        FROM `tabContract Shop`
        WHERE docstatus = 1
        AND start_date <= CURDATE()
        AND end_date >= CURDATE()
    """)[0][0] or 0
    
    return {
        "status": "success",
        "current_month_revenue": current_month_revenue,
        "yearly_revenue": yearly_revenue,
        "outstanding_amount": outstanding_amount,
        "average_rent": avg_rent
    }
