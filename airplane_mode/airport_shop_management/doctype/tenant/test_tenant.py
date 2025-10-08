# Copyright (c) 2024, macrobian88 and Contributors
# See license.txt

import unittest
import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import today, add_days


class TestTenant(FrappeTestCase):
	"""Test cases for Tenant DocType"""
	
	def setUp(self):
		"""Set up test data"""
		# Create test customer if not exists
		if not frappe.db.exists("Customer", "Test Customer"):
			customer = frappe.get_doc({
				"doctype": "Customer",
				"customer_name": "Test Customer",
				"customer_type": "Individual"
			})
			customer.insert()
		
		# Create test shop if not exists
		if not frappe.db.exists("Airport Shop", "TEST-SHOP-001"):
			shop = frappe.get_doc({
				"doctype": "Airport Shop",
				"shop_number": "TEST-SHOP-001",
				"shop_name": "Test Shop",
				"status": "Available"
			})
			shop.insert()
		
		self.test_tenant_data = {
			"doctype": "Tenant",
			"email": "test@example.com",
			"shop": "TEST-SHOP-001",
			"contract_start_date": today(),
			"contract_end_date": add_days(today(), 365),
			"customer": "Test Customer"
		}
	
	def test_tenant_creation(self):
		"""Test creating a tenant"""
		tenant = frappe.get_doc(self.test_tenant_data)
		tenant.insert()
		
		self.assertEqual(tenant.email, "test@example.com")
		self.assertEqual(tenant.customer, "Test Customer")
		
		# Clean up
		tenant.delete()
	
	def test_contract_date_validation(self):
		"""Test contract date validation"""
		invalid_data = self.test_tenant_data.copy()
		invalid_data["contract_end_date"] = add_days(today(), -10)  # End date before start date
		
		tenant = frappe.get_doc(invalid_data)
		
		with self.assertRaises(frappe.ValidationError):
			tenant.insert()
	
	def tearDown(self):
		"""Clean up after tests"""
		# Delete test tenants
		test_tenants = frappe.get_list("Tenant", 
			filters={"email": "test@example.com"}
		)
		for tenant in test_tenants:
			frappe.delete_doc("Tenant", tenant.name, force=True)
		
		# Delete test shop
		if frappe.db.exists("Airport Shop", "TEST-SHOP-001"):
			frappe.delete_doc("Airport Shop", "TEST-SHOP-001", force=True)
		
		# Delete test customer
		if frappe.db.exists("Customer", "Test Customer"):
			frappe.delete_doc("Customer", "Test Customer", force=True)
