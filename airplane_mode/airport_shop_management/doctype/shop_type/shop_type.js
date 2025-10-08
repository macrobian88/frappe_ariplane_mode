// Copyright (c) 2024, macrobian88 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shop Type', {
    refresh: function(frm) {
        // Add custom buttons
        if (frm.doc.name && !frm.doc.__islocal) {
            frm.add_custom_button(__('View Shops of this Type'), function() {
                frappe.route_options = {
                    "shop_type": frm.doc.name
                };
                frappe.set_route("List", "Airport Shop");
            });
        }
    },
    
    validate: function(frm) {
        // Basic validation
        if (frm.doc.type_name) {
            frm.doc.type_name = frm.doc.type_name.trim();
        }
    },
    
    type_name: function(frm) {
        // Format type name
        if (frm.doc.type_name) {
            // Capitalize first letter of each word
            frm.set_value('type_name', 
                frm.doc.type_name.toLowerCase().replace(/\b\w/g, l => l.toUpperCase())
            );
        }
    }
});
