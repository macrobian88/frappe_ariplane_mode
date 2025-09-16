# Copyright (c) 2025, nandhakishore and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirportShop(Document):
	pass


def get_permission_query_conditions(user):
	"""
	Permission query conditions for Airport Shop doctype.
	This function is called when filtering Airport Shop records for links and searches.
	"""
	if not user:
		user = frappe.session.user
	
	# If user is Administrator or System Manager, show all records
	if user == "Administrator" or "System Manager" in frappe.get_roles(user):
		return ""
	
	# For other users, you can add custom conditions here
	# For now, return empty condition to show all records for non-admin users
	# You can modify this logic based on your specific requirements
	
	# Example: Only show shops from specific airport
	# return f"`tabAirport Shop`.airport = '{get_user_airport(user)}'"
	
	# For now, allow all users to see all airport shops
	return ""


def has_permission(doc, user=None, permission_type=None):
	"""
	Permission check for individual Airport Shop documents.
	"""
	if not user:
		user = frappe.session.user
	
	# Administrator and System Manager have full access
	if user == "Administrator" or "System Manager" in frappe.get_roles(user):
		return True
	
	# Add custom permission logic here if needed
	# For example, check if user belongs to specific airport, role, etc.
	
	# For now, allow all users to access airport shop records
	return True
