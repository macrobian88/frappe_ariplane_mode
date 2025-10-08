# Copyright (c) 2024, macrobian88 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Tenant(Document):
	"""Tenant DocType Controller"""
	
	def validate(self):
		"""Validate the Tenant document"""
		self.validate_contract_dates()
		self.validate_shop_availability()
		
	def validate_contract_dates(self):
		"""Validate contract start and end dates"""
		if self.contract_start_date and self.contract_end_date:
			if self.contract_start_date >= self.contract_end_date:
				frappe.throw("Contract end date must be after start date")
	
	def validate_shop_availability(self):
		"""Check if shop is available for the tenant"""
		if self.shop:
			# Check if there are any overlapping contracts for this shop
			overlapping = frappe.get_list("Tenant",
				filters={
					"shop": self.shop,
					"name": ["!=", self.name],
					"contract_start_date": ["<=", self.contract_end_date],
					"contract_end_date": [">=", self.contract_start_date]
				}
			)
			if overlapping:
				frappe.throw(f"Shop {self.shop} has overlapping rental period with another tenant")
	
	def before_save(self):
		"""Actions before saving the document"""
		pass
		
	def on_update(self):
		"""Actions after updating the document"""
		# Update shop occupancy status
		if self.shop:
			shop_doc = frappe.get_doc("Airport Shop", self.shop)
			# Check if contract is currently active
			from frappe.utils import today, getdate
			today_date = getdate(today())
			
			if (getdate(self.contract_start_date) <= today_date <= getdate(self.contract_end_date)):
				shop_doc.status = "Occupied"
				shop_doc.tenant = self.customer
			else:
				shop_doc.status = "Available"
				shop_doc.tenant = ""
			
			shop_doc.save()
