// Copyright (c) 2024, macrobian88 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Airport Shop', {
    refresh: function(frm) {
        // Add custom buttons or actions when form is refreshed
        if (frm.doc.status === "Occupied") {
            frm.set_df_property('tenant', 'reqd', 1);
            frm.set_df_property('contact_number', 'reqd', 1);
        } else {
            frm.set_df_property('tenant', 'reqd', 0);
            frm.set_df_property('contact_number', 'reqd', 0);
        }
        
        // Add custom button to generate rent receipt
        if (frm.doc.status === "Occupied" && frm.doc.tenant) {
            frm.add_custom_button(__('Generate Rent Receipt'), function() {
                generate_rent_receipt(frm);
            });
        }
    },
    
    status: function(frm) {
        // Handle status change
        if (frm.doc.status === "Available") {
            // Clear tenant information when status is set to Available
            frm.set_value('tenant', '');
            frm.set_value('contact_number', '');
        }
        
        // Refresh form to update required fields
        frm.refresh_fields();
    },
    
    validate: function(frm) {
        // Validate that tenant is provided when status is Occupied
        if (frm.doc.status === "Occupied" && !frm.doc.tenant) {
            frappe.msgprint(__("Tenant name is required when status is Occupied"));
            frappe.validated = false;
        }
    }
});

function generate_rent_receipt(frm) {
    frappe.call({
        method: "airplane_mode.airport_shop_management.doctype.airport_shop.airport_shop.generate_rent_receipt",
        args: {
            shop_name: frm.doc.name
        },
        callback: function(r) {
            if (r.message) {
                frappe.msgprint(__("Rent receipt generated successfully"));
                // You can add more functionality here like printing or opening the receipt
            }
        }
    });
}
