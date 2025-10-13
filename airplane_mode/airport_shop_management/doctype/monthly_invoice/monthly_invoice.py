# Copyright (c) 2025, Airplane Mode and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MonthlyInvoice(Document):
    def validate(self):
        """Validate and set default values"""
        self.set_tenant_and_shop_details()
        self.set_invoice_amount_from_contract()
        self.generate_receipt_number()
    
    def set_tenant_and_shop_details(self):
        """Auto-fetch tenant and shop details from contract"""
        if self.contract and not (self.tenant_name and self.shop_details):
            try:
                contract_doc = frappe.get_doc("Shop Lease Contract", self.contract)
                
                # Set tenant name
                if contract_doc.tenant and not self.tenant_name:
                    tenant_doc = frappe.get_doc("Tenant", contract_doc.tenant)
                    self.tenant_name = tenant_doc.full_name or tenant_doc.customer or tenant_doc.name
                
                # Set shop details
                if contract_doc.contract_shop and not self.shop_details:
                    shop_doc = frappe.get_doc("Airport Shop", contract_doc.contract_shop)
                    self.shop_details = f"{shop_doc.shop_number} - {shop_doc.shop_name}"
                    
            except Exception as e:
                frappe.log_error(f"Error fetching contract details: {str(e)}", "Monthly Invoice Validation")
    
    def set_invoice_amount_from_contract(self):
        """Auto-set invoice amount from contract if not already set"""
        if self.contract and not self.invoice_amount:
            try:
                contract_doc = frappe.get_doc("Shop Lease Contract", self.contract)
                if contract_doc.rent_amount:
                    self.invoice_amount = contract_doc.rent_amount
            except Exception as e:
                frappe.log_error(f"Error fetching rent amount: {str(e)}", "Monthly Invoice Validation")
    
    def generate_receipt_number(self):
        """Generate receipt number when payment status is Paid"""
        if self.payment_status == "Paid" and not self.receipt_number:
            try:
                # Generate receipt number format: RCP-YYYY-MON-XXXX
                import datetime
                import random
                import string
                
                year = datetime.datetime.now().year
                month_code = self.month[:3].upper() if self.month else "XXX"
                random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                
                self.receipt_number = f"RCP-{year}-{month_code}-{random_code}"
            except Exception as e:
                frappe.log_error(f"Error generating receipt number: {str(e)}", "Monthly Invoice Validation")
    
    def before_save(self):
        """Before save operations"""
        # Set payment date when status changes to Paid
        if self.payment_status == "Paid" and not self.payment_date:
            self.payment_date = frappe.utils.today()
        
        # Clear payment fields if status changes to Unpaid
        if self.payment_status == "Unpaid":
            self.payment_date = None
            self.payment_mode = None
            self.payment_reference = None
            self.receipt_number = None
        
        # Check for overdue status
        if self.payment_status == "Unpaid" and self.due_date:
            if frappe.utils.getdate(self.due_date) < frappe.utils.getdate():
                self.payment_status = "Overdue"
    
    def after_insert(self):
        """After insert operations"""
        self.update_contract_payment_summary()
    
    def on_update(self):
        """After update operations"""
        self.update_contract_payment_summary()
    
    def update_contract_payment_summary(self):
        """Update contract payment summary when invoice is created or updated"""
        if self.contract:
            try:
                # Calculate total paid and outstanding amounts for the contract
                paid_invoices = frappe.get_all("Monthly Invoice",
                    filters={"contract": self.contract, "payment_status": "Paid"},
                    fields=["invoice_amount"]
                )
                
                total_paid = sum(invoice.invoice_amount for invoice in paid_invoices)
                
                # Update contract totals (if these fields exist in Shop Lease Contract)
                frappe.db.set_value("Shop Lease Contract", self.contract, "total_paid_amount", total_paid)
                
            except Exception as e:
                frappe.log_error(f"Error updating contract payment summary: {str(e)}", "Monthly Invoice Update")

# Permission query conditions for list view access
def get_permission_query_conditions(user):
    """Define permission conditions for Monthly Invoice list view"""
    if not user:
        user = frappe.session.user
    
    # Allow System Manager and Airport Shop Manager to see all records
    if "System Manager" in frappe.get_roles(user) or "Airport Shop Manager" in frappe.get_roles(user):
        return None
    
    # For other users, show only their own records or records they have access to
    return """`tabMonthly Invoice`.owner = '{user}'""".format(user=frappe.db.escape(user))

def has_permission(doc, user):
    """Check if user has permission to access a specific Monthly Invoice"""
    if not user:
        user = frappe.session.user
    
    # Allow System Manager and Airport Shop Manager full access
    if "System Manager" in frappe.get_roles(user) or "Airport Shop Manager" in frappe.get_roles(user):
        return True
    
    # Check if user is the owner
    if doc.owner == user:
        return True
    
    # Additional permission logic can be added here
    # For example, check if user is associated with the tenant or contract
    
    return False

@frappe.whitelist()
def get_contract_details(contract):
    """API method to get contract details for JavaScript"""
    try:
        if not contract:
            return {}
        
        contract_doc = frappe.get_doc("Shop Lease Contract", contract)
        result = {
            "rent_amount": contract_doc.rent_amount,
            "tenant_name": "",
            "shop_details": ""
        }
        
        # Get tenant details
        if contract_doc.tenant:
            tenant_doc = frappe.get_doc("Tenant", contract_doc.tenant)
            result["tenant_name"] = tenant_doc.full_name or tenant_doc.customer or tenant_doc.name
        
        # Get shop details
        if contract_doc.contract_shop:
            shop_doc = frappe.get_doc("Airport Shop", contract_doc.contract_shop)
            result["shop_details"] = f"{shop_doc.shop_number} - {shop_doc.shop_name}"
        
        return result
        
    except Exception as e:
        frappe.log_error(f"Error in get_contract_details: {str(e)}", "Monthly Invoice API")
        return {}

@frappe.whitelist()
def get_receipt_html(name):
    """Get formatted receipt HTML for printing"""
    try:
        doc = frappe.get_doc("Monthly Invoice", name)
        if doc.payment_status != "Paid":
            frappe.throw("Receipt can only be generated for paid invoices")
        
        # Use the print format to generate HTML
        print_format = "Rent Receipt Format"
        html = frappe.get_print(doc.doctype, doc.name, print_format)
        return {"html": html}
        
    except Exception as e:
        frappe.log_error(f"Error generating receipt HTML: {str(e)}", "Monthly Invoice Receipt")
        frappe.throw(f"Error generating receipt: {str(e)}")

@frappe.whitelist()
def create_monthly_invoices_for_active_contracts():
    """Create monthly invoices for all active contracts"""
    try:
        import datetime
        
        # Get current month and year
        now = datetime.datetime.now()
        current_month = now.strftime("%B %Y")
        
        # Get all active contracts
        active_contracts = frappe.get_all("Shop Lease Contract", 
            filters={"status": "Active"}, 
            fields=["name", "tenant", "contract_shop", "rent_amount"]
        )
        
        created_count = 0
        for contract in active_contracts:
            # Check if invoice already exists for this month
            existing_invoice = frappe.db.exists("Monthly Invoice", {
                "contract": contract.name,
                "month": current_month
            })
            
            if not existing_invoice:
                # Create new invoice
                invoice = frappe.new_doc("Monthly Invoice")
                invoice.contract = contract.name
                invoice.month = current_month
                invoice.invoice_amount = contract.rent_amount
                invoice.due_date = datetime.date(now.year, now.month, 5)  # Due on 5th of month
                invoice.payment_status = "Unpaid"
                
                invoice.save()
                invoice.submit()
                created_count += 1
        
        return {"message": f"Created {created_count} monthly invoices", "count": created_count}
        
    except Exception as e:
        frappe.log_error(f"Error creating monthly invoices: {str(e)}", "Monthly Invoice Batch Creation")
        frappe.throw(f"Error creating monthly invoices: {str(e)}")

@frappe.whitelist()
def get_overdue_invoices():
    """Get list of overdue invoices"""
    try:
        overdue_invoices = frappe.get_all("Monthly Invoice",
            filters={
                "payment_status": ["in", ["Unpaid", "Overdue"]],
                "due_date": ["<", frappe.utils.today()],
                "docstatus": 1
            },
            fields=["name", "contract", "month", "due_date", "invoice_amount", "tenant_name", "shop_details"],
            order_by="due_date asc"
        )
        
        return overdue_invoices
        
    except Exception as e:
        frappe.log_error(f"Error getting overdue invoices: {str(e)}", "Monthly Invoice Overdue")
        return []