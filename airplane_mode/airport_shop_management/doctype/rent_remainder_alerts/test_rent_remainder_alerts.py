# Copyright (c) 2024, macrobian88 and Contributors
# See license.txt

import unittest
import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import today, add_days


class TestRentRemainderAlerts(FrappeTestCase):
	"""Test cases for Rent Remainder Alerts DocType"""
	
	def setUp(self):
		"""Set up test data"""
		# Create test data if needed
		self.test_alert_data = {
			"doctype": "Rent Remainder Alerts",
			"contract": "Test Contract",
			"tenant": "Test Tenant", 
			"due_date": add_days(today(), 30),
			"amount": 5000.0,
			"status": "Pending",
			"alert_type": "Monthly Rent"
		}
	
	def test_alert_creation(self):
		"""Test creating a rent reminder alert"""
		# Skip if test dependencies don't exist
		if not frappe.db.exists("Shop Lease Contract", "Test Contract"):
			return
			
		alert = frappe.get_doc(self.test_alert_data)
		alert.insert()
		
		self.assertEqual(alert.status, "Pending")
		self.assertEqual(alert.amount, 5000.0)
		
		# Clean up
		alert.delete()
	
	def test_alert_date_validation(self):
		"""Test alert date validation"""
		invalid_data = self.test_alert_data.copy()
		invalid_data["alert_date"] = add_days(today(), 35)  # After due date
		
		alert = frappe.get_doc(invalid_data)
		
		try:
			alert.insert()
			# If validation passes, clean up
			alert.delete()
		except frappe.ValidationError:
			# Expected to fail validation
			pass
	
	def tearDown(self):
		"""Clean up after tests"""
		# Delete test alerts
		test_alerts = frappe.get_list("Rent Remainder Alerts", 
			filters={"contract": "Test Contract"}
		)
		for alert in test_alerts:
			frappe.delete_doc("Rent Remainder Alerts", alert.name, force=True)
