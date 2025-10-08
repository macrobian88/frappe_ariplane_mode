// Copyright (c) 2024, macrobian88 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shop Lease Contract', {
    refresh: function(frm) {
        // Add custom buttons based on status
        if (frm.doc.status === "Active" && !frm.doc.__islocal) {
            frm.add_custom_button(__('Extend Contract'), function() {
                extend_contract_dialog(frm);
            });
            
            frm.add_custom_button(__('Generate Invoice'), function() {
                generate_monthly_invoice(frm);
            });
            
            frm.add_custom_button(__('View Payment History'), function() {
                frappe.route_options = {
                    "contract": frm.doc.name
                };
                frappe.set_route("List", "Monthly Invoice");
            });
        }
        
        if (frm.doc.contract_shop) {
            frm.add_custom_button(__('View Shop'), function() {
                frappe.set_route('Form', 'Airport Shop', frm.doc.contract_shop);
            });
        }
        
        if (frm.doc.tenant) {
            frm.add_custom_button(__('View Tenant'), function() {
                frappe.set_route('Form', 'Tenant', frm.doc.tenant);
            });
        }
        
        // Set indicator color based on status
        if (frm.doc.status === "Active") {
            frm.dashboard.set_headline_alert(
                "Contract is Active",
                "green"
            );
        } else if (frm.doc.status === "Draft") {
            frm.dashboard.set_headline_alert(
                "Contract is in Draft",
                "orange"
            );
        }
    },
    
    start_date: function(frm) {
        calculate_durations(frm);
    },
    
    end_date: function(frm) {
        calculate_durations(frm);
    },
    
    tenant: function(frm) {
        // Auto-populate tenant email and details
        if (frm.doc.tenant) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Tenant',
                    name: frm.doc.tenant
                },
                callback: function(r) {
                    if (r.message) {
                        // You can add fields to display tenant info if needed
                    }
                }
            });
        }
    },
    
    contract_shop: function(frm) {
        // Check shop availability and get rent amount
        if (frm.doc.contract_shop) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Airport Shop',
                    name: frm.doc.contract_shop
                },
                callback: function(r) {
                    if (r.message) {
                        if (!frm.doc.rent_amount && r.message.rent_per_month) {
                            frm.set_value('rent_amount', r.message.rent_per_month);
                        }
                        
                        // Check if shop is available
                        if (r.message.status === "Occupied" && frm.doc.__islocal) {
                            frappe.msgprint(__('Warning: This shop is currently occupied'));
                        }
                    }
                }
            });
        }
    },
    
    validate: function(frm) {
        // Validate contract dates
        if (frm.doc.start_date && frm.doc.end_date) {
            if (frm.doc.start_date >= frm.doc.end_date) {
                frappe.msgprint(__('End date must be after start date'));
                frappe.validated = false;
            }
        }
    }
});

function calculate_durations(frm) {
    if (frm.doc.start_date && frm.doc.end_date) {
        let start = frappe.datetime.str_to_obj(frm.doc.start_date);
        let end = frappe.datetime.str_to_obj(frm.doc.end_date);
        let duration = Math.floor((end - start) / (1000 * 60 * 60 * 24 * 30)); // Approximate months
        frm.set_value('lease_duration', duration);
        
        // Calculate remaining months
        let today = new Date();
        if (end > today) {
            let remaining = Math.floor((end - today) / (1000 * 60 * 60 * 24 * 30));
            frm.set_value('remaining_months', Math.max(0, remaining));
        } else {
            frm.set_value('remaining_months', 0);
        }
    }
}

function extend_contract_dialog(frm) {
    let dialog = new frappe.ui.Dialog({
        title: __('Extend Contract'),
        fields: [
            {
                fieldtype: 'Date',
                fieldname: 'new_end_date',
                label: __('New End Date'),
                reqd: 1,
                default: frm.doc.end_date
            }
        ],
        primary_action: function(values) {
            frappe.call({
                method: 'airplane_mode.airport_shop_management.doctype.shop_lease_contract.shop_lease_contract.extend_contract',
                args: {
                    contract_name: frm.doc.name,
                    new_end_date: values.new_end_date
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint(r.message);
                        frm.reload_doc();
                        dialog.hide();
                    }
                }
            });
        },
        primary_action_label: __('Extend')
    });
    dialog.show();
}

function generate_monthly_invoice(frm) {
    frappe.call({
        method: 'airplane_mode.airport_shop_management.doctype.monthly_invoice.monthly_invoice.create_invoice_from_contract',
        args: {
            contract_name: frm.doc.name
        },
        callback: function(r) {
            if (r.message) {
                frappe.msgprint(__('Invoice created successfully'));
                frappe.set_route('Form', 'Monthly Invoice', r.message);
            }
        }
    });
}
