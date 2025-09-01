# Copyright (c) 2025, nandhakishore and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, flt

allowed_after_submit = ('payment_status', 'payment_entry', 'start_date', 'end_date')

class contract_shop(Document):
    def on_update(self):
        if self.docstatus == 1:
            before = self.get_doc_before_save()
            if before:
                system_fields = ["creation", "modified", "modified_by", "owner", "name", "idx", "docstatus"]
                for field in self.as_dict():
                    if field in system_fields:
                        continue
                    if field not in allowed_after_submit and self.get(field) != before.get(field):
                        frappe.throw(f"Cannot change field {field} after submission")




def create_invoice(doc, method=None):
    frappe.msgprint(f"create_invoice called for Contract {doc.name}")
    logger = frappe.logger("airplane_mode")  # initialize your app-specific logger
	
    logger.info(f"[create_invoice] Starting for Contract: {doc.name}")

    if doc.invoice_generated:
        logger.info(f"[create_invoice] Invoice already generated for {doc.name}. Skipping.")
        return

    if not doc.tenant:
        frappe.throw("Contract must have a Tenant before creating an invoice.")
        logger.error(f"[create_invoice] Tenant missing for Contract: {doc.name}")
        return

    try:
        tenant_doc = frappe.get_doc("Tenant", doc.tenant)
        customer = getattr(tenant_doc, "customer", None)
        if not customer:
            frappe.throw("Tenant must be linked to a Customer before creating an invoice.")
            logger.error(f"[create_invoice] Tenant {doc.tenant} has no linked customer.")
            return
        logger.info(f"[create_invoice] Tenant {doc.tenant} linked to Customer: {customer}")
    except Exception as e:
        logger.error(f"[create_invoice] Error retrieving Tenant {doc.tenant}: {str(e)}")
        raise

    items = [{
        "item_name": "Shop Rent",
        "description": f"Rent for shop {doc.shop}",
        "qty": 1,
        "rate": doc.rent_amount,
        "income_account": "Sales - TEGD"
    }]

    try:
        si = frappe.get_doc({
            "doctype": "Sales Invoice",
            "customer": customer,
            "posting_date": nowdate(),
            "due_date": doc.end_date or nowdate(),
            "items": items,
            "contract": doc.name
        }).insert(ignore_permissions=True)

        si.submit()
        logger.info(f"[create_invoice] Sales Invoice {si.name} submitted for Contract {doc.name}")
    except Exception as e:
        logger.error(f"[create_invoice] Error creating/submitting Sales Invoice: {str(e)}")
        raise

    frappe.db.set_value("contract_shop", doc.name, {
        "invoice_generated": 1,
        "invoice_name": si.name
    })
    frappe.db.commit()
    logger.info(f"[create_invoice] Contract {doc.name} updated with invoice {si.name}")


@frappe.whitelist()
def mark_invoice_as_paid(contract_name):
    contract = frappe.get_doc("contract_shop", contract_name)

    if not contract.invoice_name:
        frappe.throw("No invoice linked to this contract")

    si = frappe.get_doc("Sales Invoice", contract.invoice_name)

    if flt(si.outstanding_amount) <= 0:
        frappe.msgprint("Invoice already fully paid")
        return {"status": "already_paid", "invoice": si.name}

    try:
        company = si.company
        # Get default cash or bank account for the company
        paid_to_account = frappe.get_cached_value("Company", company, "default_cash_account") or \
                          frappe.get_cached_value("Company", company, "default_bank_account")

        if not paid_to_account:
            frappe.throw(f"Default Cash or Bank account not set for Company {company}")

        paid_to_account_currency = frappe.get_cached_value('Account', paid_to_account, 'account_currency')

        pe = frappe.get_doc({
            "doctype": "Payment Entry",
            "payment_type": "Receive",
            "party_type": "Customer",
            "party": si.customer,
            "paid_amount": flt(si.outstanding_amount),
            "received_amount": flt(si.outstanding_amount),
            "company": company,
            "mode_of_payment": "Cash",
            "paid_to": paid_to_account,
            "paid_to_account_currency": paid_to_account_currency,
            "references": [{
                "reference_doctype": "Sales Invoice",
                "reference_name": si.name,
                "allocated_amount": flt(si.outstanding_amount)
            }],
            "target_exchange_rate": 1
        }).insert()

        pe.submit()

        # Use db.set_value to update after submission safely
        frappe.db.set_value("contract_shop", contract_name, "payment_status", "Paid")
        frappe.db.set_value("contract_shop", contract_name, "payment_entry", pe.name)
        frappe.db.commit()

        frappe.msgprint(f"Marked contract {contract_name} as paid, Payment Entry {pe.name} created.")
        return {"status": "paid", "payment_entry": pe.name}

    except Exception as e:
        frappe.log_error(f"Error marking invoice as paid for contract {contract_name}: {str(e)}")
        frappe.throw(f"Failed to mark invoice as paid: {str(e)}")
