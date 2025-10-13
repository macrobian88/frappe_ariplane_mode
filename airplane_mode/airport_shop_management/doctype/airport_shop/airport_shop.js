// Copyright (c) 2025, Airplane Mode and contributors
// For license information, please see license.txt

frappe.ui.form.on('Airport Shop', {
    refresh: function(frm) {
        // Set filters for better user experience
        frm.set_query('airport', function() {
            return {
                filters: {
                    'status': 'Active'
                }
            };
        });
        
        // Add custom buttons based on status
        if (!frm.is_new()) {
            if (frm.doc.status === 'Available') {
                frm.add_custom_button(__('Mark as Occupied'), function() {
                    frappe.prompt({
                        fieldname: 'tenant_name',
                        label: __('Tenant Name'),
                        fieldtype: 'Data',
                        reqd: 1
                    }, function(values) {
                        frm.set_value('status', 'Occupied');
                        frm.set_value('tenant', values.tenant_name);
                        frm.save();
                    }, __('Assign Tenant'));
                }, __('Actions'));
            } else if (frm.doc.status === 'Occupied') {
                frm.add_custom_button(__('Mark as Available'), function() {
                    frappe.confirm(__('Are you sure you want to mark this shop as available?'), function() {
                        frm.set_value('status', 'Available');
                        frm.set_value('tenant', '');
                        frm.save();
                    });
                }, __('Actions'));
                
                frm.add_custom_button(__('Create Lease Contract'), function() {
                    frappe.new_doc('Shop Lease Contract', {
                        'contract_shop': frm.doc.name,
                        'rent_amount': frm.doc.rent_per_month
                    });
                }, __('Actions'));
            }
            
            // Add maintenance button
            frm.add_custom_button(__('Mark for Maintenance'), function() {
                frappe.prompt({
                    fieldname: 'maintenance_reason',
                    label: __('Maintenance Reason'),
                    fieldtype: 'Small Text',
                    reqd: 1
                }, function(values) {
                    frm.set_value('status', 'Maintenance');
                    frm.set_value('description', values.maintenance_reason);
                    frm.save();
                }, __('Maintenance Details'));
            }, __('Actions'));
        }
        
        // Show status indicator
        if (frm.doc.status) {
            let indicator_class = '';
            switch(frm.doc.status) {
                case 'Available':
                    indicator_class = 'green';
                    break;
                case 'Occupied':
                    indicator_class = 'red';
                    break;
                case 'Maintenance':
                    indicator_class = 'orange';
                    break;
            }
            frm.dashboard.add_indicator(__('Status: {0}', [frm.doc.status]), indicator_class);
        }
    },
    
    airport: function(frm) {
        // Auto-fetch airport name when airport is selected
        if (frm.doc.airport) {
            frappe.db.get_value('Airport', frm.doc.airport, 'airport_name')
                .then(r => {
                    if (r.message && r.message.airport_name) {
                        frm.set_value('airport_name', r.message.airport_name);
                    }
                });
        }
    },
    
    shop_type: function(frm) {
        // Auto-fetch shop type name when shop type is selected
        if (frm.doc.shop_type) {
            frappe.db.get_value('Shop Type', frm.doc.shop_type, 'shop_type_name')
                .then(r => {
                    if (r.message && r.message.shop_type_name) {
                        frm.set_value('shop_type_name', r.message.shop_type_name);
                    }
                });
        }
    },
    
    status: function(frm) {
        // Clear tenant when status changes to Available
        if (frm.doc.status === 'Available' && frm.doc.tenant) {
            frappe.confirm(__('Clear tenant information when marking as available?'), function() {
                frm.set_value('tenant', '');
                frm.set_value('contact_number', '');
            });
        }
    },
    
    validate: function(frm) {
        // Validation rules
        if (frm.doc.status === 'Occupied' && !frm.doc.tenant) {
            frappe.msgprint(__('Tenant name is required when status is Occupied'));
            frappe.validated = false;
        }
        
        if (frm.doc.rent_per_month && frm.doc.rent_per_month < 0) {
            frappe.msgprint(__('Rent per month cannot be negative'));
            frappe.validated = false;
        }
        
        if (frm.doc.area && frm.doc.area <= 0) {
            frappe.msgprint(__('Area must be greater than 0'));
            frappe.validated = false;
        }
    }
});

// Custom list view settings
frappe.listview_settings['Airport Shop'] = {
    add_fields: ['status', 'airport_name', 'shop_type_name', 'rent_per_month', 'tenant'],
    
    get_indicator: function(doc) {
        if (doc.status === 'Available') {
            return [__('Available'), 'green', 'status,=,Available'];
        } else if (doc.status === 'Occupied') {
            return [__('Occupied'), 'red', 'status,=,Occupied'];
        } else if (doc.status === 'Maintenance') {
            return [__('Maintenance'), 'orange', 'status,=,Maintenance'];
        }
        return [__('Unknown'), 'grey', ''];
    },
    
    onload: function(listview) {
        // Add custom buttons to list view
        listview.page.add_inner_button(__('Available Shops'), function() {
            listview.filter_area.add([[listview.doctype, 'status', '=', 'Available']]);
        }, __('Filter By'));
        
        listview.page.add_inner_button(__('Occupied Shops'), function() {
            listview.filter_area.add([[listview.doctype, 'status', '=', 'Occupied']]);
        }, __('Filter By'));
        
        listview.page.add_inner_button(__('By Airport'), function() {
            frappe.prompt({
                fieldname: 'airport',
                label: __('Airport'),
                fieldtype: 'Link',
                options: 'Airport',
                reqd: 1
            }, function(values) {
                listview.filter_area.add([[listview.doctype, 'airport', '=', values.airport]]);
            }, __('Select Airport'));
        }, __('Filter By'));
        
        listview.page.add_inner_button(__('By Shop Type'), function() {
            frappe.prompt({
                fieldname: 'shop_type',
                label: __('Shop Type'),
                fieldtype: 'Link',
                options: 'Shop Type',
                reqd: 1
            }, function(values) {
                listview.filter_area.add([[listview.doctype, 'shop_type', '=', values.shop_type]]);
            }, __('Select Shop Type'));
        }, __('Filter By'));
    },
    
    // Custom formatting for list view
    formatters: {
        airport_name: function(value, field, doc) {
            if (!value && doc.airport) {
                return `<span class="text-muted">${doc.airport}</span>`;
            }
            return value || 'Not Set';
        },
        
        shop_type_name: function(value, field, doc) {
            if (!value && doc.shop_type) {
                return `<span class="text-muted">${doc.shop_type}</span>`;
            }
            return value || 'Not Set';
        },
        
        rent_per_month: function(value) {
            if (value) {
                return `₹${frappe.format(value, 'Currency')}`;
            }
            return 'Not Set';
        },
        
        tenant: function(value, field, doc) {
            if (doc.status === 'Occupied' && value) {
                return `<span class="text-success">${value}</span>`;
            } else if (doc.status === 'Available') {
                return '<span class="text-muted">Available</span>';
            }
            return value || 'Not Set';
        }
    }
};