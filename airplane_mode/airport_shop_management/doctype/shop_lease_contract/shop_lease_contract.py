# Copyright (c) 2024, macrobian88 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, date_diff, add_months, today


class ShopLeaseContract(Document):
	"""Shop Lease Contract DocType Controller"""
	
	def validate(self):
		"""Validate the Shop Lease Contract document"""
		self.validate_dates()
		self.calculate_lease_duration()
		self.calculate_remaining_months()
		
	def validate_dates(self):
		"""Validate contract dates"""
		if self.start_date and self.end_date:
			if getdate(self.start_date) >= getdate(self.end_date):
				frappe.throw("End date must be after start date")
	
	def calculate_lease_duration(self):
		"""Calculate lease duration in months"""
		if self.start_date and self.end_date:
			start = getdate(self.start_date)
			end = getdate(self.end_date)
			self.lease_duration = date_diff(end, start) // 30  # Approximate months
	
	def calculate_remaining_months(self):
		"""Calculate remaining months in the contract"""
		if self.end_date:
			end = getdate(self.end_date)
			today_date = getdate(today())
			if end > today_date:
				self.remaining_months = max(0, date_diff(end, today_date) // 30)
			else:
				self.remaining_months = 0
	
	def before_save(self):
		"""Actions before saving the document"""
		pass
		
	def on_update(self):
		"""Actions after updating the document"""
		# Update shop occupancy status
		if self.contract_shop and self.status == "Active":
			shop_doc = frappe.get_doc("Airport Shop", self.contract_shop)
			shop_doc.status = "Occupied"
			if self.tenant:
				tenant_doc = frappe.get_doc("Tenant", self.tenant)
				shop_doc.tenant = tenant_doc.customer
			shop_doc.save()
		
	def on_submit(self):
		"""Actions on document submission"""
		self.status = "Active"
		self.on_update()
		
	def on_cancel(self):
		"""Actions on document cancellation"""
		self.status = "Cancelled"
		# Free up the shop
		if self.contract_shop:
			shop_doc = frappe.get_doc("Airport Shop", self.contract_shop)
			shop_doc.status = "Available"
			shop_doc.tenant = ""
			shop_doc.save()

@frappe.whitelist()
def get_active_contracts():
	"""Get all active shop lease contracts"""
	return frappe.get_list("Shop Lease Contract",
		filters={"status": "Active"},
		fields=["name", "contract_shop", "tenant", "rent_amount", "start_date", "end_date"],
		order_by="start_date desc"
	)

@frappe.whitelist()
def get_expiring_contracts(days=30):
	"""Get contracts expiring within specified days"""
	from frappe.utils import add_days
	
	future_date = add_days(today(), int(days))
	
	return frappe.get_list("Shop Lease Contract",
		filters={
			"status": "Active",
			"end_date": ["between", [today(), future_date]]
		},
		fields=["name", "contract_shop", "tenant", "end_date", "rent_amount"],
		order_by="end_date"
	)

@frappe.whitelist()
def extend_contract(contract_name, new_end_date):
	"""Extend a contract to a new end date"""
	contract = frappe.get_doc("Shop Lease Contract", contract_name)
	
	if getdate(new_end_date) <= getdate(contract.end_date):
		frappe.throw("New end date must be after current end date")
	
	contract.end_date = new_end_date
	contract.calculate_lease_duration()
	contract.calculate_remaining_months()
	contract.save()
	
	return f"Contract {contract_name} extended to {new_end_date}"
