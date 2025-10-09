# Copyright (c) 2025, nandhakishore and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import formatdate

class RentPaymentContract(Document):
	def validate(self):
		"""Validate the Rent Payment Contract before saving"""
		if self.amount_paid <= 0:
			frappe.throw("Amount Paid must be greater than zero")
	
	def on_submit(self):
		"""Actions to perform when the payment is submitted"""
		# Update related Monthly Invoice if exists
		self.update_monthly_invoice()
		
	def update_monthly_invoice(self):
		"""Update the corresponding Monthly Invoice payment status"""
		if self.contract_reference and self.payment_date:
			# Find corresponding monthly invoice
			month = formatdate(self.payment_date, "MMM").lower()
			invoice_name = f"{self.contract_reference}-{month}"
			
			if frappe.db.exists("Monthly Invoice", invoice_name):
				invoice = frappe.get_doc("Monthly Invoice", invoice_name)
				if invoice.payment_status != "Paid":
					invoice.payment_status = "Paid"
					invoice.payment_date = self.payment_date
					invoice.save()
					frappe.msgprint(f"Updated Monthly Invoice {invoice_name}")

def update_monthly_invoice(doc, method):
	"""Hook function called on Rent Payment Contract submission"""
	if doc.payment_status == "Completed":
		doc.update_monthly_invoice()
