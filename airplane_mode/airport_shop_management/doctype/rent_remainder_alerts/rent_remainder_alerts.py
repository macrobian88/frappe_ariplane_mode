# Copyright (c) 2024, macrobian88 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, add_days, getdate


class RentRemainderAlerts(Document):
	"""Rent Remainder Alerts DocType Controller"""
	
	def validate(self):
		"""Validate the Rent Remainder Alerts document"""
		self.validate_dates()
		
	def validate_dates(self):
		"""Validate alert dates"""
		if self.alert_date and self.due_date:
			if getdate(self.alert_date) > getdate(self.due_date):
				frappe.throw("Alert date cannot be after due date")
	
	def before_save(self):
		"""Actions before saving the document"""
		if not self.alert_date:
			# Set default alert date to 5 days before due date
			if self.due_date:
				self.alert_date = add_days(self.due_date, -5)
		
	def on_update(self):
		"""Actions after updating the document"""
		pass
	
	def send_alert(self):
		"""Send rent reminder alert"""
		if self.tenant and self.contract:
			tenant_doc = frappe.get_doc("Tenant", self.tenant)
			if tenant_doc.email:
				# Send email notification
				subject = f"Rent Payment Reminder - {self.contract}"
				message = f"""
				Dear {tenant_doc.customer},
				
				This is a friendly reminder that your rent payment for {self.contract} is due on {self.due_date}.
				
				Amount Due: {self.amount}
				Due Date: {self.due_date}
				
				Please ensure payment is made on time to avoid any late fees.
				
				Thank you.
				"""
				
				frappe.sendmail(
					recipients=[tenant_doc.email],
					subject=subject,
					message=message
				)
				
				# Update status
				self.db_set('status', 'Sent')
				self.db_set('sent_date', today())

@frappe.whitelist()
def create_rent_alerts():
	"""Create rent reminder alerts for upcoming due dates"""
	from frappe.utils import add_days, today
	
	# Get all active shop lease contracts
	contracts = frappe.get_list("Shop Lease Contract",
		filters={"status": "Active"},
		fields=["name", "tenant", "rent_amount"]
	)
	
	alerts_created = 0
	for contract in contracts:
		# Calculate next due date (assuming monthly rent)
		next_due_date = add_days(today(), 30)  # Next month
		
		# Check if alert already exists
		existing_alert = frappe.get_list("Rent Remainder Alerts",
			filters={
				"contract": contract.name,
				"due_date": next_due_date,
				"status": ["in", ["Pending", "Sent"]]
			}
		)
		
		if not existing_alert:
			# Create new alert
			alert = frappe.get_doc({
				"doctype": "Rent Remainder Alerts",
				"contract": contract.name,
				"tenant": contract.tenant,
				"due_date": next_due_date,
				"amount": contract.rent_amount,
				"status": "Pending",
				"alert_type": "Monthly Rent"
			})
			alert.insert()
			alerts_created += 1
	
	return f"Created {alerts_created} rent reminder alerts"

@frappe.whitelist()
def send_pending_alerts():
	"""Send all pending rent reminder alerts"""
	pending_alerts = frappe.get_list("Rent Remainder Alerts",
		filters={
			"status": "Pending",
			"alert_date": ["<=", today()]
		}
	)
	
	sent_count = 0
	for alert in pending_alerts:
		alert_doc = frappe.get_doc("Rent Remainder Alerts", alert.name)
		alert_doc.send_alert()
		sent_count += 1
	
	return f"Sent {sent_count} rent reminder alerts"

@frappe.whitelist()
def check_rent_due_alerts():
	"""Main method called by scheduler to check and process rent due alerts"""
	try:
		# Step 1: Create new alerts for upcoming due dates
		create_result = create_rent_alerts()
		
		# Step 2: Send pending alerts
		send_result = send_pending_alerts()
		
		# Log results
		frappe.log_error(
			title="Rent Due Alerts Check",
			message=f"Daily rent alerts check completed successfully.\n{create_result}\n{send_result}"
		)
		
		return {
			"success": True,
			"create_result": create_result,
			"send_result": send_result
		}
		
	except Exception as e:
		frappe.log_error(
			title="Rent Due Alerts Error",
			message=f"Error during rent due alerts check: {str(e)}"
		)
		return {
			"success": False,
			"error": str(e)
		}
