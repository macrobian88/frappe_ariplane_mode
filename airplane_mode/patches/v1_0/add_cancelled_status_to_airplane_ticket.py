# airplane_mode/patches/v1_0/add_cancelled_status_to_airplane_ticket.py

import frappe

def execute():
    """
    Add 'Cancelled' status option to Airplane Ticket DocType
    """
    try:
        # Check if Airplane Ticket DocType exists
        if not frappe.db.exists("DocType", "Airplane Ticket"):
            return
        
        # Get the status field
        status_field = frappe.get_doc("DocField", {
            "parent": "Airplane Ticket",
            "fieldname": "status"
        })
        
        if status_field:
            # Update the options to include Cancelled
            current_options = status_field.options or ""
            if "Cancelled" not in current_options:
                # Add Cancelled to the options
                new_options = current_options + "\nCancelled" if current_options else "Booked\nChecked-In\nBoarded\nCancelled"
                
                frappe.db.set_value("DocField", status_field.name, "options", new_options)
                
                # Clear cache and reload doctype
                frappe.clear_cache(doctype="Airplane Ticket")
                frappe.reload_doctype("Airplane Ticket")
                
                print("Successfully added 'Cancelled' status to Airplane Ticket DocType")
            else:
                print("'Cancelled' status already exists in Airplane Ticket DocType")
        else:
            print("Status field not found in Airplane Ticket DocType")
            
    except Exception as e:
        print(f"Error updating Airplane Ticket status field: {str(e)}")
        frappe.log_error(f"Error in add_cancelled_status_to_airplane_ticket patch: {str(e)}")