# Copyright (c) 2025, nandhakishore and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    """
    Airport Shop Report - Shows comprehensive information about airport shops,
    their contracts, occupancy, and revenue.
    """
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data


def get_columns():
    """Define the columns for the Airport Shop Report."""
    return [
        {
            "label": _("Shop ID"),
            "fieldname": "shop_id",
            "fieldtype": "Link",
            "options": "Airport Shop",
            "width": 120
        },
        {
            "label": _("Shop Name"),
            "fieldname": "shop_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Airport"),
            "fieldname": "airport",
            "fieldtype": "Link",
            "options": "Airport",
            "width": 120
        },
        {
            "label": _("Terminal"),
            "fieldname": "terminal",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Shop Type"),
            "fieldname": "shop_type",
            "fieldtype": "Link",
            "options": "Shop Type",
            "width": 120
        },
        {
            "label": _("Area (sq ft)"),
            "fieldname": "area",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Current Tenant"),
            "fieldname": "current_tenant",
            "fieldtype": "Link",
            "options": "Tenant",
            "width": 150
        },
        {
            "label": _("Contract Status"),
            "fieldname": "contract_status",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Monthly Rent"),
            "fieldname": "monthly_rent",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Contract Start"),
            "fieldname": "contract_start",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Contract End"),
            "fieldname": "contract_end",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Revenue YTD"),
            "fieldname": "revenue_ytd",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Status"),
            "fieldname": "shop_status",
            "fieldtype": "Data",
            "width": 100
        }
    ]


def get_data(filters):
    """Get the data for Airport Shop Report."""
    conditions = get_conditions(filters)
    
    # Base query to get shop information
    shop_query = f"""
        SELECT 
            s.name as shop_id,
            s.shop_name,
            s.airport,
            s.terminal,
            s.shop_type,
            s.area,
            s.status as shop_status
        FROM 
            `tabAirport Shop` s
        {conditions}
        ORDER BY 
            s.airport, s.terminal, s.shop_name
    """
    
    shop_data = frappe.db.sql(shop_query, as_dict=True)
    
    # Enhance data with contract and revenue information
    for row in shop_data:
        # Get current active contract
        contract_info = get_current_contract(row.shop_id)
        if contract_info:
            row.update(contract_info)
        else:
            # No active contract
            row.update({
                'current_tenant': None,
                'contract_status': 'Vacant',
                'monthly_rent': 0,
                'contract_start': None,
                'contract_end': None
            })
        
        # Get revenue information
        row['revenue_ytd'] = get_shop_revenue_ytd(row.shop_id)
    
    return shop_data


def get_conditions(filters):
    """Build WHERE conditions based on filters."""
    conditions = ["WHERE 1=1"]
    
    if filters.get("airport"):
        conditions.append(f"AND s.airport = '{filters['airport']}'")
    
    if filters.get("shop_type"):
        conditions.append(f"AND s.shop_type = '{filters['shop_type']}'")
    
    if filters.get("terminal"):
        conditions.append(f"AND s.terminal = '{filters['terminal']}'")
    
    if filters.get("status"):
        conditions.append(f"AND s.status = '{filters['status']}'")
    
    return " ".join(conditions)


def get_current_contract(shop_id):
    """Get current active contract for a shop."""
    try:
        # Check for active Shop Lease Contract
        contract = frappe.db.sql("""
            SELECT 
                slc.tenant as current_tenant,
                slc.status as contract_status,
                slc.monthly_rent,
                slc.start_date as contract_start,
                slc.end_date as contract_end
            FROM 
                `tabShop Lease Contract` slc
            WHERE 
                slc.shop = %s 
                AND slc.status = 'Active'
                AND slc.docstatus = 1
                AND slc.start_date <= CURDATE()
                AND slc.end_date >= CURDATE()
            ORDER BY 
                slc.start_date DESC
            LIMIT 1
        """, (shop_id,), as_dict=True)
        
        if contract:
            return contract[0]
        
        # Check for any recent contract if no active one
        recent_contract = frappe.db.sql("""
            SELECT 
                slc.tenant as current_tenant,
                slc.status as contract_status,
                slc.monthly_rent,
                slc.start_date as contract_start,
                slc.end_date as contract_end
            FROM 
                `tabShop Lease Contract` slc
            WHERE 
                slc.shop = %s 
                AND slc.docstatus = 1
            ORDER BY 
                slc.end_date DESC
            LIMIT 1
        """, (shop_id,), as_dict=True)
        
        if recent_contract:
            contract_info = recent_contract[0]
            # Update status based on dates
            if contract_info['contract_end'] < frappe.utils.today():
                contract_info['contract_status'] = 'Expired'
            elif contract_info['contract_start'] > frappe.utils.today():
                contract_info['contract_status'] = 'Future'
            return contract_info
            
    except Exception as e:
        frappe.log_error(f"Error getting contract for shop {shop_id}: {e}")
    
    return None


def get_shop_revenue_ytd(shop_id):
    """Get year-to-date revenue for a shop."""
    try:
        year_start = frappe.utils.get_year_start()
        
        # Get revenue from monthly invoices
        revenue = frappe.db.sql("""
            SELECT 
                COALESCE(SUM(mi.total_amount), 0) as revenue
            FROM 
                `tabMonthly Invoice` mi
            WHERE 
                mi.shop = %s 
                AND mi.docstatus = 1
                AND mi.invoice_date >= %s
        """, (shop_id, year_start))
        
        if revenue and revenue[0][0]:
            return revenue[0][0]
            
    except Exception as e:
        frappe.log_error(f"Error getting revenue for shop {shop_id}: {e}")
    
    return 0.0


# Additional utility functions for the report

@frappe.whitelist()
def get_report_filters():
    """Get available filter options for the report."""
    return {
        'airports': frappe.get_all('Airport', fields=['name', 'city'], order_by='city'),
        'shop_types': frappe.get_all('Shop Type', fields=['name', 'description'], order_by='name'),
        'terminals': frappe.db.sql("SELECT DISTINCT terminal FROM `tabAirport Shop` WHERE terminal IS NOT NULL ORDER BY terminal"),
        'status_options': ['Active', 'Inactive', 'Under Maintenance', 'Under Construction']
    }


@frappe.whitelist()
def get_shop_details(shop_id):
    """Get detailed information for a specific shop."""
    shop = frappe.get_doc('Airport Shop', shop_id)
    
    # Get contract history
    contracts = frappe.get_all(
        'Shop Lease Contract',
        filters={'shop': shop_id},
        fields=['name', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'status'],
        order_by='start_date desc'
    )
    
    # Get revenue history
    revenue_history = frappe.db.sql("""
        SELECT 
            DATE_FORMAT(invoice_date, '%%Y-%%m') as month,
            SUM(total_amount) as revenue
        FROM 
            `tabMonthly Invoice`
        WHERE 
            shop = %s 
            AND docstatus = 1
            AND invoice_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
        GROUP BY 
            DATE_FORMAT(invoice_date, '%%Y-%%m')
        ORDER BY 
            month
    """, (shop_id,), as_dict=True)
    
    return {
        'shop': shop.as_dict(),
        'contracts': contracts,
        'revenue_history': revenue_history
    }
