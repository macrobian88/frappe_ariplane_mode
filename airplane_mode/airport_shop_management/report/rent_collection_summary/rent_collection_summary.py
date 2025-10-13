# Copyright (c) 2025, Airplane Mode and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate, today, add_months, cstr

def execute(filters=None):
    """Main report execution function"""
    if not filters:
        filters = {}
    
    columns = get_columns()
    data = get_data(filters)
    chart_data = get_chart_data(data)
    summary = get_summary(data)
    
    return columns, data, None, chart_data, summary

def get_columns():
    """Define report columns"""
    return [
        {
            "fieldname": "invoice_name",
            "label": _("Invoice"),
            "fieldtype": "Link",
            "options": "Monthly Invoice",
            "width": 120
        },
        {
            "fieldname": "contract",
            "label": _("Contract"),
            "fieldtype": "Link",
            "options": "Shop Lease Contract",
            "width": 120
        },
        {
            "fieldname": "tenant_name",
            "label": _("Tenant"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "shop_details",
            "label": _("Shop"),
            "fieldtype": "Data",
            "width": 180
        },
        {
            "fieldname": "month",
            "label": _("Month"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "invoice_date",
            "label": _("Invoice Date"),
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "due_date",
            "label": _("Due Date"),
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "invoice_amount",
            "label": _("Invoice Amount"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "payment_status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "payment_date",
            "label": _("Payment Date"),
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "payment_mode",
            "label": _("Payment Mode"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "days_overdue",
            "label": _("Days Overdue"),
            "fieldtype": "Int",
            "width": 100
        },
        {
            "fieldname": "receipt_number",
            "label": _("Receipt No."),
            "fieldtype": "Data",
            "width": 120
        }
    ]

def get_data(filters):
    """Fetch and process invoice data"""
    conditions = get_conditions(filters)
    
    data = frappe.db.sql(f"""
        SELECT 
            mi.name as invoice_name,
            mi.contract,
            mi.tenant_name,
            mi.shop_details,
            mi.month,
            mi.invoice_date,
            mi.due_date,
            mi.invoice_amount,
            mi.payment_status,
            mi.payment_date,
            mi.payment_mode,
            mi.receipt_number,
            CASE 
                WHEN mi.payment_status IN ('Unpaid', 'Overdue') AND mi.due_date < CURDATE()
                THEN DATEDIFF(CURDATE(), mi.due_date)
                ELSE 0
            END as days_overdue
        FROM `tabMonthly Invoice` mi
        WHERE mi.docstatus = 1
        {conditions}
        ORDER BY 
            mi.invoice_date DESC,
            mi.due_date ASC,
            mi.payment_status DESC
    """, as_dict=1)
    
    return data

def get_conditions(filters):
    """Build SQL conditions based on filters"""
    conditions = []
    
    if filters.get("from_date"):
        conditions.append(f"mi.invoice_date >= '{filters['from_date']}'")
    
    if filters.get("to_date"):
        conditions.append(f"mi.invoice_date <= '{filters['to_date']}'")
    
    if filters.get("contract"):
        conditions.append(f"mi.contract = '{filters['contract']}'")
    
    if filters.get("payment_status"):
        if isinstance(filters['payment_status'], list):
            status_list = "', '".join(filters['payment_status'])
            conditions.append(f"mi.payment_status IN ('{status_list}')")
        else:
            conditions.append(f"mi.payment_status = '{filters['payment_status']}'")
    
    if filters.get("tenant"):
        conditions.append(f"mi.tenant_name LIKE '%{filters['tenant']}%'")
    
    if filters.get("shop"):
        conditions.append(f"mi.shop_details LIKE '%{filters['shop']}%'")
    
    if filters.get("overdue_only"):
        conditions.append("mi.payment_status IN ('Unpaid', 'Overdue') AND mi.due_date < CURDATE()")
    
    return " AND " + " AND ".join(conditions) if conditions else ""

def get_chart_data(data):
    """Generate chart data for visualization"""
    if not data:
        return None
    
    # Payment Status Distribution
    status_counts = {}
    total_amounts = {}
    
    for row in data:
        status = row.get('payment_status', 'Unknown')
        amount = flt(row.get('invoice_amount', 0))
        
        status_counts[status] = status_counts.get(status, 0) + 1
        total_amounts[status] = total_amounts.get(status, 0) + amount
    
    return {
        "data": {
            "labels": list(status_counts.keys()),
            "datasets": [
                {
                    "name": "Count",
                    "values": list(status_counts.values())
                },
                {
                    "name": "Amount",
                    "values": list(total_amounts.values())
                }
            ]
        },
        "type": "donut",
        "height": 300,
        "colors": ["#28a745", "#ffc107", "#dc3545", "#6c757d"]
    }

def get_summary(data):
    """Generate summary statistics"""
    if not data:
        return []
    
    total_invoices = len(data)
    total_amount = sum(flt(row.get('invoice_amount', 0)) for row in data)
    
    paid_invoices = [row for row in data if row.get('payment_status') == 'Paid']
    unpaid_invoices = [row for row in data if row.get('payment_status') == 'Unpaid']
    overdue_invoices = [row for row in data if row.get('payment_status') == 'Overdue' or (
        row.get('payment_status') == 'Unpaid' and row.get('days_overdue', 0) > 0)]
    
    paid_amount = sum(flt(row.get('invoice_amount', 0)) for row in paid_invoices)
    unpaid_amount = sum(flt(row.get('invoice_amount', 0)) for row in unpaid_invoices)
    overdue_amount = sum(flt(row.get('invoice_amount', 0)) for row in overdue_invoices)
    
    collection_rate = (paid_amount / total_amount * 100) if total_amount > 0 else 0
    
    return [
        {
            "value": total_invoices,
            "label": _("Total Invoices"),
            "datatype": "Int"
        },
        {
            "value": total_amount,
            "label": _("Total Amount"),
            "datatype": "Currency"
        },
        {
            "value": len(paid_invoices),
            "label": _("Paid Invoices"),
            "datatype": "Int"
        },
        {
            "value": paid_amount,
            "label": _("Paid Amount"),
            "datatype": "Currency"
        },
        {
            "value": len(unpaid_invoices),
            "label": _("Unpaid Invoices"),
            "datatype": "Int"
        },
        {
            "value": unpaid_amount,
            "label": _("Unpaid Amount"),
            "datatype": "Currency"
        },
        {
            "value": len(overdue_invoices),
            "label": _("Overdue Invoices"),
            "datatype": "Int"
        },
        {
            "value": overdue_amount,
            "label": _("Overdue Amount"),
            "datatype": "Currency"
        },
        {
            "value": f"{collection_rate:.1f}%",
            "label": _("Collection Rate"),
            "datatype": "Data"
        }
    ]