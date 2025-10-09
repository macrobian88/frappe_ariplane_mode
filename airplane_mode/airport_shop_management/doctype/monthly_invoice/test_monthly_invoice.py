# Copyright (c) 2025, nandhakishore and Contributors
# See license.txt

import frappe
import unittest

class TestMonthlyInvoice(unittest.TestCase):
	def setUp(self):
		"""Set up test fixtures"""
		# Create test data if needed
		pass
		
	def test_monthly_invoice_creation(self):
		"""Test basic Monthly Invoice creation"""
		# Test case for creating a monthly invoice
		invoice = frappe.get_doc({
			"doctype": "Monthly Invoice",
			"title": "Test Invoice",
			"invoice_amount": 1000,
			"payment_status": "Unpaid"
		})
		invoice.insert()
		
		self.assertEqual(invoice.payment_status, "Unpaid")
		self.assertEqual(invoice.invoice_amount, 1000)
		
		# Clean up
		invoice.delete()
		
	def test_payment_status_update(self):
		"""Test payment status update functionality"""
		invoice = frappe.get_doc({
			"doctype": "Monthly Invoice", 
			"title": "Test Payment Invoice",
			"invoice_amount": 1500,
			"payment_status": "Paid"
		})
		invoice.insert()
		
		# Payment date should be set automatically when status is Paid
		self.assertIsNotNone(invoice.payment_date)
		
		# Clean up
		invoice.delete()
		
	def tearDown(self):
		"""Clean up after tests"""
		pass
