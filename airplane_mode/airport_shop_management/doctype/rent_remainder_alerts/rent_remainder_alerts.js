// Copyright (c) 2024, macrobian88 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rent Remainder Alerts', {
    refresh: function(frm) {
        // Add custom buttons
        if (frm.doc.status === "Pending" && !frm.doc.__islocal) {
            frm.add_custom_button(__('Send Alert Now'), function() {
                frappe.call({
                    method: 'send_alert',
                    doc: frm.doc,
                    callback: function(r) {
                        if (!r.exc) {
                            frappe.msgprint(__('Alert sent successfully'));
                            frm.reload_doc();
                        }
                    }
                });
            });
        }
        
        if (frm.doc.contract) {
            frm.add_custom_button(__('View Contract'), function() {
                frappe.set_route('Form', 'Shop Lease Contract', frm.doc.contract);
            });
        }
        
        if (frm.doc.tenant) {
            frm.add_custom_button(__('View Tenant'), function() {
                frappe.set_route('Form', 'Tenant', frm.doc.tenant);
            });
        }
        
        // Add bulk actions to list view
        if (frm.is_new()) {
            frm.add_custom_button(__('Create Monthly Alerts'), function() {
                frappe.call({
                    method: 'airplane_mode.airport_shop_management.doctype.rent_remainder_alerts.rent_remainder_alerts.create_rent_alerts',
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(r.message);
                            frm.reload_doc();
                        }
                    }
                });
            });
        }
    },
    
    contract: function(frm) {
        // Auto-populate tenant and amount when contract is selected
        if (frm.doc.contract) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Shop Lease Contract',
                    name: frm.doc.contract
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('tenant', r.message.tenant);
                        frm.set_value('amount', r.message.rent_amount);
                    }
                }
            });
        }
    },
    
    validate: function(frm) {
        // Validate dates
        if (frm.doc.alert_date && frm.doc.due_date) {
            if (frm.doc.alert_date > frm.doc.due_date) {
                frappe.msgprint(__('Alert date cannot be after due date'));
                frappe.validated = false;
            }
        }
    }
});
