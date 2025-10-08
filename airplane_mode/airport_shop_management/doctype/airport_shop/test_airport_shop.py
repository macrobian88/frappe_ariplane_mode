# Copyright (c) 2024, macrobian88 and Contributors
# See license.txt

import unittest
import frappe
from frappe.tests.utils import FrappeTestCase


class TestAirportShop(FrappeTestCase):
	"""Test cases for Airport Shop DocType"""
	
	def setUp(self):
		"""Set up test data"""
		self.test_shop_data = {
			"doctype": "Airport Shop",
			"shop_number": "TEST-001",
			"shop_name": "Test Shop",
			"status": "Available",
			"area": 100.0,
			"rent_per_month": 5000.0
		}
	
	def test_shop_creation(self):
		"""Test creating an airport shop"""
		shop = frappe.get_doc(self.test_shop_data)
		shop.insert()
		
		self.assertEqual(shop.shop_number, "TEST-001")
		self.assertEqual(shop.shop_name, "Test Shop")
		self.assertEqual(shop.status, "Available")
		
		# Clean up
		shop.delete()
	
	def test_unique_shop_number(self):
		"""Test that shop numbers must be unique"""
		# Create first shop
		shop1 = frappe.get_doc(self.test_shop_data)
		shop1.insert()
		
		# Try to create second shop with same number
		shop2 = frappe.get_doc(self.test_shop_data)
		
		with self.assertRaises(frappe.ValidationError):
			shop2.insert()
		
		# Clean up
		shop1.delete()
	
	def tearDown(self):
		"""Clean up after tests"""
		# Delete any remaining test shops
		test_shops = frappe.get_list("Airport Shop", 
			filters={"shop_number": ["like", "TEST-%"]}
		)
		for shop in test_shops:
			frappe.delete_doc("Airport Shop", shop.name, force=True)
