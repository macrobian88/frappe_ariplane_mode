import frappe
from frappe.utils import today

def send_rent_reminders():
    reminders_enabled = frappe.get_single("Airport Shop Settings").enable_rent_reminders
    if not reminders_enabled:
        return

    due = frappe.get_all(
        "Rent Payment",
        filters={"payment_date": today(), "status": "Unpaid"},
        fields=["name", "tenant", "amount"]
    )

    for row in due:
        tenant_doc = frappe.get_doc("Tenant", row.tenant)
        if tenant_doc.email:
            frappe.sendmail(
                recipients=[tenant_doc.email],
                subject="Airport Shop Rent Due Today",
                message=f"Dear {tenant_doc.tenant_name}, your rent ({row.amount}) is due today."
            )
