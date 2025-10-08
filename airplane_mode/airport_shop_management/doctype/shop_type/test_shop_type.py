# Copyright (c) 2024, macrobian88 and Contributors
# See license.txt

import unittest
import frappe
from frappe.tests.utils import FrappeTestCase


class TestShopType(FrappeTestCase):
	"""Test cases for Shop Type DocType"""
	
	def setUp(self):
		"""Set up test data"""
		self.test_shop_type_data = {
			"doctype": "Shop Type",
			"type_name": "Test Shop Type",
			"enabled": 1,
			"description": "Test shop type for unit testing"
		}
	
	def test_shop_type_creation(self):
		"""Test creating a shop type"""
		shop_type = frappe.get_doc(self.test_shop_type_data)
		shop_type.insert()
		
		self.assertEqual(shop_type.type_name, "Test Shop Type")
		self.assertEqual(shop_type.enabled, 1)
		
		# Clean up
		shop_type.delete()
	
	def test_unique_type_name(self):
		"""Test that type names must be unique"""
		# Create first shop type
		shop_type1 = frappe.get_doc(self.test_shop_type_data)
		shop_type1.insert()
		
		# Try to create second shop type with same name
		shop_type2 = frappe.get_doc(self.test_shop_type_data)
		
		with self.assertRaises(frappe.ValidationError):
			shop_type2.insert()
		
		# Clean up
		shop_type1.delete()
	
	def test_disabled_shop_type(self):
		"""Test that disabled shop types allow duplicate names"""
		# Create disabled shop type
		shop_type1_data = self.test_shop_type_data.copy()
		shop_type1_data["enabled"] = 0
		shop_type1 = frappe.get_doc(shop_type1_data)
		shop_type1.insert()
		
		# Create another with same name but enabled
		shop_type2 = frappe.get_doc(self.test_shop_type_data)
		shop_type2.insert()  # This should work since first is disabled
		
		# Clean up
		shop_type1.delete()
		shop_type2.delete()
	
	def tearDown(self):
		"""Clean up after tests"""
		# Delete any remaining test shop types
		test_shop_types = frappe.get_list("Shop Type", 
			filters={"type_name": ["like", "Test%"]}
		)
		for shop_type in test_shop_types:
			frappe.delete_doc("Shop Type", shop_type.name, force=True)
