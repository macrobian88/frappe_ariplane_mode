# Copyright (c) 2025, nandhakishore and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate

class ContractShop(Document):
	def validate(self):
		"""Validate the Contract Shop before saving"""
		if self.start_date and self.end_date:
			if getdate(self.start_date) >= getdate(self.end_date):
				frappe.throw("Start Date cannot be greater than or equal to End Date")
		
		# Update status based on end date
		if self.end_date and getdate(self.end_date) < getdate(today()):
			self.status = "Expired"
	
	def before_save(self):
		"""Actions before saving the document"""
		# Set title field for better identification
		if not hasattr(self, '_title'):
			self.title = f"{self.shop_name} - {self.tenant_name}"
	
	def on_update(self):
		"""Actions after the document is updated"""
		# Create monthly invoices if contract is active
		if self.status == "Active" and not self.flags.ignore_create_invoices:
			self.create_monthly_invoices()
	
	def create_monthly_invoices(self):
		"""Create monthly invoices for active contracts"""
		# This can be enhanced to automatically create invoices
		pass

# Hook functions for contract management
def create_invoice(doc, method):
	"""Create monthly invoice for contract"""
	if doc.status == "Active":
		# Implementation for creating invoices
		pass

def validate_contract(doc, method):
	"""Validate contract details"""
	if doc.start_date and doc.end_date:
		if getdate(doc.start_date) >= getdate(doc.end_date):
			frappe.throw("Contract start date cannot be after end date")

def update_contract_payment_status(doc, method):
	"""Update contract payment status based on invoices/payments"""
	# Implementation for updating payment status
	pass
