# Copyright (c) 2024, macrobian88 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirportShop(Document):
	"""Airport Shop DocType Controller"""
	
	def validate(self):
		"""Validate the Airport Shop document"""
		self.validate_shop_number()
		
	def validate_shop_number(self):
		"""Validate that shop number is unique"""
		if self.shop_number:
			existing = frappe.get_list("Airport Shop", 
				filters={
					"shop_number": self.shop_number,
					"name": ["!=", self.name]
				}
			)
			if existing:
				frappe.throw(f"Shop number {self.shop_number} already exists")
	
	def before_save(self):
		"""Actions before saving the document"""
		pass
		
	def on_update(self):
		"""Actions after updating the document"""
		pass
		
	def on_submit(self):
		"""Actions on document submission"""
		pass
		
	def on_cancel(self):
		"""Actions on document cancellation"""
		pass

@frappe.whitelist()
def generate_rent_receipt(shop_name):
	"""Generate a rent receipt for the shop"""
	shop = frappe.get_doc("Airport Shop", shop_name)
	
	if not shop.tenant:
		frappe.throw("No tenant assigned to this shop")
	
	# Create a simple rent receipt (you can customize this based on your needs)
	receipt_data = {
		"shop_number": shop.shop_number,
		"shop_name": shop.shop_name,
		"tenant": shop.tenant,
		"rent_amount": shop.rent_per_month,
		"receipt_date": frappe.utils.today()
	}
	
	frappe.msgprint(f"Rent receipt generated for {shop.tenant}")
	return receipt_data
