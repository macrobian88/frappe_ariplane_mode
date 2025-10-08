# Copyright (c) 2024, macrobian88 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShopType(Document):
	"""Shop Type DocType Controller"""
	
	def validate(self):
		"""Validate the Shop Type document"""
		self.validate_type_name()
		
	def validate_type_name(self):
		"""Validate that type name is unique"""
		if self.type_name:
			existing = frappe.get_list("Shop Type", 
				filters={
					"type_name": self.type_name,
					"name": ["!=", self.name],
					"enabled": 1
				}
			)
			if existing:
				frappe.throw(f"Shop Type '{self.type_name}' already exists")
	
	def before_save(self):
		"""Actions before saving the document"""
		pass
		
	def on_update(self):
		"""Actions after updating the document"""
		pass

@frappe.whitelist()
def get_enabled_shop_types():
	"""Get all enabled shop types"""
	return frappe.get_list("Shop Type", 
		filters={"enabled": 1}, 
		fields=["name", "type_name"],
		order_by="type_name"
	)
