import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class MonthlyBill(Document):
    def before_save(self):
        """Auto-fill payment date if bill is marked as Paid."""
        if self.payment_status == "Paid" and not self.payment_date:
            self.payment_date = nowdate()
