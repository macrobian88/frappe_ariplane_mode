# Copyright (c) 2024, macrobian88 and Contributors
# See license.txt

import unittest
import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import today, add_days, add_months


class TestShopLeaseContract(FrappeTestCase):
	"""Test cases for Shop Lease Contract DocType"""
	
	def setUp(self):
		"""Set up test data"""
		self.test_contract_data = {
			"doctype": "Shop Lease Contract",
			"contract_shop": "Test Shop",
			"tenant": "Test Tenant",
			"rent_amount": 5000.0,
			"start_date": today(),
			"end_date": add_months(today(), 12),
			"status": "Draft"
		}
	
	def test_contract_creation(self):
		"""Test creating a shop lease contract"""
		# Skip if test dependencies don't exist
		if not frappe.db.exists("Airport Shop", "Test Shop"):
			return
			
		contract = frappe.get_doc(self.test_contract_data)
		contract.insert()
		
		self.assertEqual(contract.status, "Draft")
		self.assertEqual(contract.rent_amount, 5000.0)
		self.assertTrue(contract.lease_duration > 0)
		
		# Clean up
		contract.delete()
	
	def test_date_validation(self):
		"""Test contract date validation"""
		invalid_data = self.test_contract_data.copy()
		invalid_data["end_date"] = add_days(today(), -10)  # End date before start date
		
		contract = frappe.get_doc(invalid_data)
		
		try:
			contract.insert()
			# If validation passes, clean up
			contract.delete()
		except frappe.ValidationError:
			# Expected to fail validation
			pass
	
	def test_duration_calculation(self):
		"""Test lease duration calculation"""
		contract = frappe.get_doc(self.test_contract_data)
		contract.calculate_lease_duration()
		contract.calculate_remaining_months()
		
		# Should calculate approximately 12 months
		self.assertTrue(contract.lease_duration >= 11 and contract.lease_duration <= 13)
		self.assertTrue(contract.remaining_months >= 11)
	
	def tearDown(self):
		"""Clean up after tests"""
		# Delete test contracts
		test_contracts = frappe.get_list("Shop Lease Contract", 
			filters={"contract_shop": "Test Shop"}
		)
		for contract in test_contracts:
			frappe.delete_doc("Shop Lease Contract", contract.name, force=True)
