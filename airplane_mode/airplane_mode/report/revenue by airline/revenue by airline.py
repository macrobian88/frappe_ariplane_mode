import frappe
from frappe.utils import flt

def execute(filters=None):
    data = frappe.db.sql("""
        SELECT
            ai.airline AS airline,
            SUM(at.total_price) AS revenue
        FROM `tabAirplane Ticket` at
        JOIN `tabAirplane Flight` af ON af.name = at.flight
        JOIN `tabAirplane` ai ON ai.name = af.airplane
        WHERE at.docstatus = 1
        GROUP BY ai.airline
        ORDER BY revenue DESC
    """, as_dict=True)

    columns = [
        {"label": "Airline", "fieldname": "airline", "fieldtype": "Data", "width": 200},
        {"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 150},
    ]

    # add a donut chart
    chart = {
        "data": {
            "labels": [d["airline"] for d in data],
            "datasets": [{"values": [flt(d["revenue"]) for d in data]}],
        },
        "type": "donut",
    }

    # add a summary row
    total_revenue = sum(d["revenue"] for d in data)
    summary = [{"value": total_revenue, "label": "Total Revenue", "datatype": "Currency"}]

    return columns, data, None, chart, summary
