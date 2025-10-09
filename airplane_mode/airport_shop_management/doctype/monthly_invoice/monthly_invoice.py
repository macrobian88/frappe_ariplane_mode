# Copyright (c) 2025, nandhakishore and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class MonthlyInvoice(Document):
	def validate(self):
		"""Validate the Monthly Invoice before saving"""
		if self.payment_status == "Paid" and not self.payment_date:
			self.payment_date = today()
			
	def on_submit(self):
		"""Actions to perform when the invoice is submitted"""
		if self.payment_status == "Paid":
			self.update_payment_status()
			
	def update_payment_status(self):
		"""Update payment status and date"""
		if self.payment_status == "Paid" and not self.payment_date:
			self.payment_date = today()
			self.save()


# Module-level permission functions (FIXED: Moved outside the class)
def get_permission_query_conditions(user):
	"""Return permission query conditions for Monthly Invoice"""
	if not user:
		user = frappe.session.user
	
	if "System Manager" in frappe.get_roles(user):
		return ""
	
	# Regular users can only see invoices for their contracts
	return f"""(`tabMonthly Invoice`.owner = '{user}')"""


def has_permission(doc, user):
	"""Check if user has permission for Monthly Invoice document"""
	if not user:
		user = frappe.session.user
	
	if "System Manager" in frappe.get_roles(user):
		return True
	
	# Check if user owns the contract
	if doc.contract:
		contract = frappe.get_doc("Shop Lease Contract", doc.contract)
		return contract.owner == user or contract.tenant_email == user
	
	return False


def update_payment_status(doc, method):
	"""Hook function called on Monthly Invoice submission"""
	if doc.payment_status == "Paid" and not doc.payment_date:
		doc.payment_date = today()
