// Monthly Invoice JavaScript

frappe.ui.form.on('Monthly Invoice', {
    refresh: function(frm) {
        // Add custom print button for rent receipt
        if (frm.doc.payment_status === 'Paid' && !frm.is_new()) {
            frm.add_custom_button(__('Print Receipt'), function() {
                frappe.route_options = {
                    'doctype': 'Monthly Invoice',
                    'name': frm.doc.name,
                    'format': 'Rent Receipt Format'
                };
                frappe.set_route('print');
            }, __('Print'));
        }
        
        // Show alert if payment is overdue
        if (frm.doc.payment_status === 'Unpaid' && frm.doc.due_date) {
            let due_date = frappe.datetime.str_to_obj(frm.doc.due_date);
            let today = new Date();
            if (due_date < today) {
                frm.dashboard.add_indicator(__('Payment Overdue'), 'red');
            }
        }
    },
    
    contract: function(frm) {
        // Auto-fetch tenant name and shop details when contract is selected
        if (frm.doc.contract) {
            frappe.db.get_doc('Shop Lease Contract', frm.doc.contract)
                .then(contract_doc => {
                    if (contract_doc.tenant) {
                        frappe.db.get_value('Tenant', contract_doc.tenant, ['full_name', 'customer'])
                            .then(tenant_data => {
                                frm.set_value('tenant_name', tenant_data.message.full_name || tenant_data.message.customer);
                            });
                    }
                    
                    if (contract_doc.contract_shop) {
                        frappe.db.get_value('Airport Shop', contract_doc.contract_shop, ['shop_number', 'shop_name'])
                            .then(shop_data => {
                                frm.set_value('shop_details', `${shop_data.message.shop_number} - ${shop_data.message.shop_name}`);
                            });
                    }
                    
                    // Auto-set invoice amount from contract
                    if (contract_doc.rent_amount) {
                        frm.set_value('invoice_amount', contract_doc.rent_amount);
                    }
                });
        }
    },
    
    payment_status: function(frm) {
        // Auto-set payment date when status changes to Paid
        if (frm.doc.payment_status === 'Paid' && !frm.doc.payment_date) {
            frm.set_value('payment_date', frappe.datetime.get_today());
        }
        
        // Generate receipt number when payment is marked as paid
        if (frm.doc.payment_status === 'Paid' && !frm.doc.receipt_number) {
            let receipt_no = `RCP-${frm.doc.name}`;
            frm.set_value('receipt_number', receipt_no);
        }
        
        // Clear payment fields if status changes back to Unpaid
        if (frm.doc.payment_status === 'Unpaid') {
            frm.set_value('payment_date', '');
            frm.set_value('payment_mode', '');
            frm.set_value('payment_reference', '');
            frm.set_value('receipt_number', '');
        }
    },
    
    due_date: function(frm) {
        // Update payment status to overdue if due date has passed
        if (frm.doc.due_date && frm.doc.payment_status === 'Unpaid') {
            let due_date = frappe.datetime.str_to_obj(frm.doc.due_date);
            let today = new Date();
            if (due_date < today) {
                frm.set_value('payment_status', 'Overdue');
            }
        }
    },
    
    before_save: function(frm) {
        // Auto-generate receipt number format
        if (frm.doc.payment_status === 'Paid' && !frm.doc.receipt_number) {
            let month_code = frm.doc.month ? frm.doc.month.substring(0, 3).toUpperCase() : 'XXX';
            let year = new Date().getFullYear();
            frm.set_value('receipt_number', `RCP-${year}-${month_code}-${Math.random().toString(36).substr(2, 4).toUpperCase()}`);
        }
    }
});

// Add custom indicator for payment status
frappe.listview_settings['Monthly Invoice'] = {
    add_fields: ['payment_status', 'due_date', 'invoice_amount'],
    get_indicator: function(doc) {
        if (doc.payment_status === 'Paid') {
            return [__('Paid'), 'green', 'payment_status,=,Paid'];
        } else if (doc.payment_status === 'Overdue') {
            return [__('Overdue'), 'red', 'payment_status,=,Overdue'];
        } else if (doc.payment_status === 'Unpaid') {
            // Check if overdue
            if (doc.due_date && frappe.datetime.str_to_obj(doc.due_date) < new Date()) {
                return [__('Overdue'), 'red', 'payment_status,=,Unpaid'];
            }
            return [__('Unpaid'), 'orange', 'payment_status,=,Unpaid'];
        }
    }
};