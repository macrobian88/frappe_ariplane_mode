// Monthly Invoice JavaScript

frappe.ui.form.on('Monthly Invoice', {
    refresh: function(frm) {
        // Add custom print button for rent receipt
        if (frm.doc.payment_status === 'Paid' && !frm.is_new()) {
            frm.add_custom_button(__('Print Receipt'), function() {
                // Use the correct print method for Frappe v15
                window.open(`/printview?doctype=${encodeURIComponent(frm.doc.doctype)}&name=${encodeURIComponent(frm.doc.name)}&format=Rent%20Receipt%20Format&no_letterhead=0&letterhead=No%20Letterhead&settings=%7B%7D&_lang=en`, '_blank');
            }, __('Print'));
            
            // Alternative method - using frappe.print_format
            frm.add_custom_button(__('Download Receipt PDF'), function() {
                frappe.call({
                    method: 'frappe.utils.print_format.download_pdf',
                    args: {
                        doctype: frm.doc.doctype,
                        name: frm.doc.name,
                        format: 'Rent Receipt Format',
                        no_letterhead: 1
                    },
                    callback: function(r) {
                        if(r.message) {
                            var w = window.open();
                            w.document.write(r.message);
                            w.print();
                        }
                    }
                });
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
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Shop Lease Contract',
                    name: frm.doc.contract
                },
                callback: function(r) {
                    if (r.message) {
                        let contract_doc = r.message;
                        
                        // Set tenant name
                        if (contract_doc.tenant) {
                            frappe.call({
                                method: 'frappe.client.get_value',
                                args: {
                                    doctype: 'Tenant',
                                    filters: {'name': contract_doc.tenant},
                                    fieldname: ['full_name', 'customer']
                                },
                                callback: function(tenant_r) {
                                    if (tenant_r.message) {
                                        frm.set_value('tenant_name', tenant_r.message.full_name || tenant_r.message.customer);
                                    }
                                }
                            });
                        }
                        
                        // Set shop details
                        if (contract_doc.contract_shop) {
                            frappe.call({
                                method: 'frappe.client.get_value',
                                args: {
                                    doctype: 'Airport Shop',
                                    filters: {'name': contract_doc.contract_shop},
                                    fieldname: ['shop_number', 'shop_name']
                                },
                                callback: function(shop_r) {
                                    if (shop_r.message) {
                                        frm.set_value('shop_details', `${shop_r.message.shop_number} - ${shop_r.message.shop_name}`);
                                    }
                                }
                            });
                        }
                        
                        // Auto-set invoice amount from contract
                        if (contract_doc.rent_amount && !frm.doc.invoice_amount) {
                            frm.set_value('invoice_amount', contract_doc.rent_amount);
                        }
                    }
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
            let month_code = frm.doc.month ? frm.doc.month.substring(0, 3).toUpperCase() : 'XXX';
            let year = new Date().getFullYear();
            let random_code = Math.random().toString(36).substr(2, 4).toUpperCase();
            frm.set_value('receipt_number', `RCP-${year}-${month_code}-${random_code}`);
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