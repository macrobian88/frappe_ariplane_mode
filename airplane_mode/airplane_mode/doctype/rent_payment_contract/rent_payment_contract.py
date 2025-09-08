import frappe
from frappe.model.document import Document
from frappe.utils import today

class RentPaymentContract(Document):

    def before_insert(self):
        """Fetch unpaid bills from the linked contract_shop"""
        print("before_insert: Fetching unpaid bills")
        self.fetch_unpaid_bills()

    def fetch_unpaid_bills(self):
        """Fetch unpaid bills from the parent contract_shop"""
        if not self.contract_shop:
            print("No contract_shop selected, skipping fetch")
            return

        contract = frappe.get_doc("contract_shop", self.contract_shop)
        print(f"fetch_unpaid_bills: Found contract {contract.name}")

        self.set("bills", [])  # Clear previous rows

        for row in contract.bills:
            print(f"Checking bill {row.month} - {row.payment_status}")
            if row.payment_status != "Paid":
                self.append("bills", {
                    "month": row.month,
                    "bill_amount": row.bill_amount,
                    "due_date": row.due_date,
                    "payment_status": "Unpaid",
                    "payment_date": None
                })

    def before_save(self):
        """Calculate total payment in this RentPaymentContract"""
        print("before_save: Calculating total payment")
        total = 0.0
        for row in self.bills:
            print(f"Bill {row.month}: {row.payment_status}, {row.bill_amount}")
            if row.payment_status == "Paid":
                if not row.payment_date:
                    row.payment_date = today()
                total += row.bill_amount or 0.0

        self.payment_amount = total
        if total > 0 and not self.payment_date:
            self.payment_date = today()
        print(f"Total payment calculated: {self.payment_amount}")

    def on_submit(self):
        """Submit payment safely without touching submitted child rows"""
        print("on_submit: submitting payment to parent contract")
        self.submit_payment()

    def submit_payment(self):
        """
        Submit RentPaymentContract safely:
        - Only update parent totals and status.
        - Do NOT touch submitted child table rows.
        """
        if not self.contract_shop:
            frappe.throw("Please select a Contract Shop.")

        # Calculate total paid in this RentPaymentContract
        total_paid = sum([row.bill_amount for row in self.bills if row.payment_status == "Paid"])
        print(f"Total paid in this contract: {total_paid}")

        # Update parent contract totals safely
        contract = frappe.get_doc("contract_shop", self.contract_shop)

        # Compute new total paid: add current payment to existing total
        new_total_paid = (contract.total_paid_amount or 0.0) + total_paid

        # Update parent fields only
        frappe.db.set_value("contract_shop", contract.name, "total_paid_amount", new_total_paid)
        print(f"Updated parent total_paid_amount: {new_total_paid}")

        # Optional: update status if fully paid
        all_paid = all(row.payment_status == "Paid" for row in self.bills)
        if all_paid:
            frappe.db.set_value("contract_shop", contract.name, "status", "Completed")
            print(f"Parent contract status set to Completed")
        else:
            frappe.db.set_value("contract_shop", contract.name, "status", "Active")
            print(f"Parent contract status set to Active")

        frappe.msgprint(f"Payment submitted successfully! Parent contract totals updated.")
