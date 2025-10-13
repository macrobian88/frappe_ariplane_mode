// Monthly Invoice JavaScript

frappe.ui.form.on('Monthly Invoice', {
    refresh: function(frm) {
        // Add custom print button for rent receipt
        if (frm.doc.payment_status === 'Paid' && !frm.is_new()) {
            frm.add_custom_button(__('Print Receipt'), function() {
                // Use the standard print view with our custom format
                window.open(`/printview?doctype=${encodeURIComponent(frm.doc.doctype)}&name=${encodeURIComponent(frm.doc.name)}&format=Rent%20Receipt%20Format&no_letterhead=0&letterhead=No%20Letterhead&settings=%7B%7D&_lang=en`, '_blank');
            }, __('Print'));
            
            // Alternative: Generate PDF using server-side method
            frm.add_custom_button(__('Download PDF'), function() {
                frappe.call({
                    method: 'airplane_mode.airport_shop_management.doctype.monthly_invoice.monthly_invoice.get_receipt_html',
                    args: {
                        name: frm.doc.name
                    },
                    callback: function(r) {
                        if(r.message && r.message.html) {
                            // Create a new window with the receipt HTML
                            var printWindow = window.open('', '_blank');
                            printWindow.document.write(r.message.html);
                            printWindow.document.close();
                            
                            // Auto-print after a short delay
                            setTimeout(function() {
                                printWindow.print();
                            }, 1000);
                        }
                    },
                    error: function(r) {
                        frappe.msgprint(__('Error generating receipt: ' + (r.message || 'Unknown error')));
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
        
        // Show payment status indicator
        if (frm.doc.payment_status === 'Paid') {
            frm.dashboard.add_indicator(__('Payment Received'), 'green');
        } else if (frm.doc.payment_status === 'Overdue') {
            frm.dashboard.add_indicator(__('Payment Overdue'), 'red');
        }
    },
    
    contract: function(frm) {
        // Auto-fetch contract details using server-side method
        if (frm.doc.contract) {
            frappe.call({
                method: 'airplane_mode.airport_shop_management.doctype.monthly_invoice.monthly_invoice.get_contract_details',
                args: {
                    contract: frm.doc.contract
                },
                callback: function(r) {
                    if (r.message) {
                        // Set tenant name if not already set
                        if (r.message.tenant_name && !frm.doc.tenant_name) {
                            frm.set_value('tenant_name', r.message.tenant_name);
                        }
                        
                        // Set shop details if not already set
                        if (r.message.shop_details && !frm.doc.shop_details) {
                            frm.set_value('shop_details', r.message.shop_details);
                        }
                        
                        // Set invoice amount from contract if not already set
                        if (r.message.rent_amount && !frm.doc.invoice_amount) {
                            frm.set_value('invoice_amount', r.message.rent_amount);
                        }
                    }
                },
                error: function(r) {
                    console.log('Error fetching contract details:', r);
                }
            });
        }
    },
    
    payment_status: function(frm) {
        // Handle payment status changes
        if (frm.doc.payment_status === 'Paid') {
            // Auto-set payment date if not already set
            if (!frm.doc.payment_date) {
                frm.set_value('payment_date', frappe.datetime.get_today());
            }
            
            // Show success message
            frappe.show_alert({
                message: __('Payment marked as received. Receipt can now be generated.'),
                indicator: 'green'
            });
        }
        
        // Refresh the form to show/hide print buttons
        frm.refresh();
    },
    
    due_date: function(frm) {
        // Check if payment is overdue
        if (frm.doc.due_date && frm.doc.payment_status === 'Unpaid') {
            let due_date = frappe.datetime.str_to_obj(frm.doc.due_date);
            let today = new Date();
            if (due_date < today) {
                frappe.show_alert({
                    message: __('This invoice is overdue!'),
                    indicator: 'red'
                });
            }
        }
    },
    
    invoice_amount: function(frm) {
        // Validate invoice amount
        if (frm.doc.invoice_amount < 0) {
            frappe.msgprint(__('Invoice amount cannot be negative'));
            frm.set_value('invoice_amount', 0);
        }
    }
});

// Add custom indicator for payment status in list view
frappe.listview_settings['Monthly Invoice'] = {
    add_fields: ['payment_status', 'due_date', 'invoice_amount', 'payment_date'],
    get_indicator: function(doc) {
        if (doc.payment_status === 'Paid') {
            return [__('Paid'), 'green', 'payment_status,=,Paid'];
        } else if (doc.payment_status === 'Overdue') {
            return [__('Overdue'), 'red', 'payment_status,=,Overdue'];
        } else if (doc.payment_status === 'Unpaid') {
            // Check if overdue based on due date
            if (doc.due_date && frappe.datetime.str_to_obj(doc.due_date) < new Date()) {
                return [__('Overdue'), 'red', 'payment_status,=,Unpaid'];
            }
            return [__('Unpaid'), 'orange', 'payment_status,=,Unpaid'];
        }
        return [__('Draft'), 'grey', 'payment_status,=,'];
    },
    
    onload: function(listview) {
        // Add custom buttons to list view
        listview.page.add_inner_button(__('Generate Monthly Invoices'), function() {
            frappe.new_doc('Monthly Invoice');
        });
    }
};

// Custom method to validate form before submission
frappe.ui.form.on('Monthly Invoice', {
    before_submit: function(frm) {
        // Validate required fields
        if (!frm.doc.contract) {
            frappe.msgprint(__('Contract is required'));
            return false;
        }
        
        if (!frm.doc.month) {
            frappe.msgprint(__('Month is required'));
            return false;
        }
        
        if (!frm.doc.invoice_amount || frm.doc.invoice_amount <= 0) {
            frappe.msgprint(__('Valid invoice amount is required'));
            return false;
        }
        
        if (!frm.doc.due_date) {
            frappe.msgprint(__('Due date is required'));
            return false;
        }
        
        return true;
    }
});