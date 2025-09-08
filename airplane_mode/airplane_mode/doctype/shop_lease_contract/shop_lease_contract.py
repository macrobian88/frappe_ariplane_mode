import frappe
from frappe.model.document import Document
from frappe.utils import month_diff, getdate, flt, add_months, today
import calendar

class ShopLeaseContract(Document):

    def validate(self):
        """Auto-calculate lease duration and remaining months"""
        if self.start_date and self.end_date:
            # Total lease duration
            months = month_diff(self.end_date, self.start_date) + 1
            if months <= 0:
                frappe.throw("End Date must be after Start Date")
            self.lease_duration = months

            # Calculate remaining months based on unpaid invoices
            unpaid_invoices = frappe.get_all(
                "Monthly Invoice",
                filters={"contract": self.name, "payment_status": "unpaid"},
                fields=["name"]
            )
            remaining = len(unpaid_invoices)
            
            # Fallback: if no invoices exist yet, calculate from today
            if remaining == 0:
                remaining = month_diff(getdate(self.end_date), getdate(today()))
            
            self.remaining_months = max(remaining, 0)

    def on_submit(self):
        """Set status Active and generate monthly invoices"""
        self.db_set("status", "Active")
        self.create_monthly_invoices()

    def create_monthly_invoices(self):
        if not (self.start_date and self.end_date and self.rent_amount):
            return

        months = month_diff(self.end_date, self.start_date) + 1
        monthly_rent = flt(self.rent_amount) / months
        start = getdate(self.start_date)

        for i in range(months):
            due = add_months(start, i)
            month_name = calendar.month_name[due.month]
            month_label = f"{month_name} {due.year}"

            # Avoid duplicate invoices
            if frappe.db.exists("Monthly Invoice", {"contract": self.name, "month": month_label}):
                continue

            invoice = frappe.get_doc({
                "doctype": "Monthly Invoice",
                "contract": self.name,
                "month": month_label,
                "due_date": due,
                "invoice_amount": round(monthly_rent, 2),
                "payment_status": "unpaid"
            })
            invoice.insert(ignore_permissions=True)
