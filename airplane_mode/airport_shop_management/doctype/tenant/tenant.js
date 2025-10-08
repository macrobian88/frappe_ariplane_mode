// Copyright (c) 2024, macrobian88 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tenant', {
    refresh: function(frm) {
        // Add custom buttons and actions
        if (frm.doc.shop && frm.doc.contract_start_date && frm.doc.contract_end_date) {
            frm.add_custom_button(__('View Shop Details'), function() {
                frappe.set_route('Form', 'Airport Shop', frm.doc.shop);
            });
        }
        
        if (frm.doc.customer) {
            frm.add_custom_button(__('View Customer'), function() {
                frappe.set_route('Form', 'Customer', frm.doc.customer);
            });
        }
    },
    
    validate: function(frm) {
        // Validate contract dates
        if (frm.doc.contract_start_date && frm.doc.contract_end_date) {
            if (frm.doc.contract_start_date >= frm.doc.contract_end_date) {
                frappe.msgprint(__('Contract end date must be after start date'));
                frappe.validated = false;
            }
        }
    },
    
    shop: function(frm) {
        // When shop is selected, check availability
        if (frm.doc.shop && frm.doc.contract_start_date && frm.doc.contract_end_date) {
            frappe.call({
                method: 'airplane_mode.airport_shop_management.doctype.tenant.tenant.check_shop_availability',
                args: {
                    shop: frm.doc.shop,
                    start_date: frm.doc.contract_start_date,
                    end_date: frm.doc.contract_end_date,
                    exclude_tenant: frm.doc.name
                },
                callback: function(r) {
                    if (r.message && !r.message.available) {
                        frappe.msgprint(__('Warning: This shop has overlapping rental periods'));
                    }
                }
            });
        }
    }
});

@frappe.whitelist()
def check_shop_availability(shop, start_date, end_date, exclude_tenant=None):
    """Check if a shop is available for the given date range"""
    filters = {
        "shop": shop,
        "contract_start_date": ["<=", end_date],
        "contract_end_date": [">=", start_date]
    }
    
    if exclude_tenant:
        filters["name"] = ["!=", exclude_tenant]
    
    overlapping = frappe.get_list("Tenant", filters=filters)
    
    return {
        "available": len(overlapping) == 0,
        "overlapping_contracts": len(overlapping)
    }
