import frappe
from frappe.model.document import Document
from frappe.utils import today, month_diff, getdate

class MonthlyInvoice(Document):

    def before_save(self):
        """Auto-fill payment date and update parent contract immediately"""
        if self.payment_status.lower() == "paid" and not self.payment_date:
            self.payment_date = today()

        if not self.contract:
            return

        # Fetch all invoices for this contract
        invoices = frappe.get_all(
            "Monthly Invoice",
            filters={"contract": self.contract},
            fields=["invoice_amount", "payment_status"]
        )

        total_paid = 0.0
        unpaid_count = 0
        all_paid = True

        for inv in invoices:
            status = inv.payment_status.lower()
            if status == "paid":
                total_paid += inv.invoice_amount or 0.0
            else:
                all_paid = False
                unpaid_count += 1

        
        status_to_set = "Completed" if all_paid else "Active"

       
        frappe.db.set_value("Shop Lease Contract", self.contract, "total_paid_amount", total_paid)
        frappe.db.set_value("Shop Lease Contract", self.contract, "status", status_to_set)
        frappe.db.set_value("Shop Lease Contract", self.contract, "remaining_months", unpaid_count)
