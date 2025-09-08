import frappe
from frappe.model.document import Document
from frappe.utils import month_diff, getdate, flt, add_months
import calendar

class contract_shop(Document):

    def validate(self):
        """Auto-calculate lease duration"""
        if self.start_date and self.end_date:
            months = month_diff(self.end_date, self.start_date) + 1
            if months <= 0:
                frappe.throw("End Date must be after Start Date")
            self.lease_duration = months

    def before_save(self):
        """Generate bills automatically"""
        self.set("bills", [])

        if not (self.start_date and self.end_date and self.rent_amount):
            return

        months = month_diff(self.end_date, self.start_date) + 1
        monthly_rent = flt(self.rent_amount) / months
        start = getdate(self.start_date)

        for i in range(months):
            due = add_months(start, i)
            month_name = calendar.month_name[due.month]

            self.append("bills", {
                "month": f"{month_name} {due.year}",
                "bill_amount": round(monthly_rent, 2),
                "due_date": due,
                "payment_status": "Unpaid"
            })

    def on_submit(self):
        """Mark contract as Active on submission"""
        self.db_set("status", "Active")

    def update_status_if_completed(self):
        """Mark Completed if all bills Paid"""
        if all(b.payment_status == "Paid" for b in self.bills):
            self.db_set("status", "Completed")
        else:
            self.db_set("status", "Active")
