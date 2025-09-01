// Copyright (c) 2025, nandhakishore and contributors
// For license information, please see license.txt

// frappe.ui.form.on("contract_shop", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('contract_shop', {
  refresh: function(frm) {
    if (!frm.doc.invoice_generated) {
      frm.add_custom_button('Generate Invoice', () => {
        frappe.call({
          method: "airplane_mode.airplane_mode.doctype.contract.contract.create_invoice",
          args: { doc: frm.doc }, // if you expose a wrapper that accepts name instead
          callback: () => frm.reload_doc()
        });
      });
    } else if (frm.doc.invoice_generated && !frm.doc.paid) {
      frm.add_custom_button('Mark as Paid', () => {
        frappe.call({
          method: "airplane_mode.airplane_mode.doctype.contract.contract.mark_invoice_as_paid",
          args: { contract_name: frm.doc.name },
          callback: () => frm.reload_doc()
        });
      });
    }
  }
});