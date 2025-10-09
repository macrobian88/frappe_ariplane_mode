# airplane_mode/patches/v1_0/update_airplane_ticket_status_options.py

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def execute():
    """
    Update Airplane Ticket status field to include 'Cancelled' option
    """
    try:
        # Check if Airplane Ticket DocType exists
        if not frappe.db.exists("DocType", "Airplane Ticket"):
            print("Airplane Ticket DocType not found")
            return
        
        # Get the DocType document
        doctype_doc = frappe.get_doc("DocType", "Airplane Ticket")
        
        # Find the status field
        status_field = None
        for field in doctype_doc.fields:
            if field.fieldname == "status":
                status_field = field
                break
        
        if status_field:
            # Check current options
            current_options = status_field.options or ""
            print(f"Current status options: {current_options}")
            
            # Add Cancelled if not present
            if "Cancelled" not in current_options:
                new_options = "Booked\nChecked-In\nBoarded\nCancelled"
                status_field.options = new_options
                
                # Save the doctype
                doctype_doc.save()
                
                # Clear cache and reload
                frappe.clear_cache(doctype="Airplane Ticket")
                frappe.reload_doctype("Airplane Ticket")
                
                print("✅ Successfully added 'Cancelled' status to Airplane Ticket")
                
                # Create some sample cancelled tickets for demonstration
                create_sample_cancelled_tickets()
                
            else:
                print("ℹ️ 'Cancelled' status already exists in Airplane Ticket")
        else:
            print("⚠️ Status field not found in Airplane Ticket DocType")
            
        # Ensure the workspace counters are updated
        update_workspace_counters()
            
    except Exception as e:
        print(f"❌ Error updating Airplane Ticket status: {str(e)}")
        frappe.log_error(f"Error in update_airplane_ticket_status_options patch: {str(e)}")

def create_sample_cancelled_tickets():
    """Create sample cancelled tickets for demonstration"""
    try:
        # Get existing tickets that can be cancelled
        existing_tickets = frappe.get_list("Airplane Ticket", 
                                         filters={"status": ["!=", "Cancelled"]}, 
                                         limit=2)
        
        cancelled_count = 0
        for ticket in existing_tickets:
            try:
                # Create a cancelled version
                original_ticket = frappe.get_doc("Airplane Ticket", ticket.name)
                new_ticket = frappe.copy_doc(original_ticket)
                new_ticket.status = "Cancelled"
                new_ticket.insert()
                cancelled_count += 1
                print(f"✅ Created cancelled ticket: {new_ticket.name}")
                
                if cancelled_count >= 1:  # Create only 1 sample cancelled ticket
                    break
                    
            except Exception as e:
                print(f"Warning: Could not create cancelled ticket: {str(e)}")
                continue
                
        if cancelled_count > 0:
            print(f"✅ Created {cancelled_count} sample cancelled ticket(s)")
        else:
            print("ℹ️ No sample cancelled tickets created")
            
    except Exception as e:
        print(f"Warning: Error creating sample data: {str(e)}")

def update_workspace_counters():
    """Ensure workspace counters are properly configured"""
    try:
        # Check if Airplane Mode workspace exists
        if frappe.db.exists("Workspace", "Airplane Mode"):
            workspace = frappe.get_doc("Workspace", "Airplane Mode")
            
            # Define counter configurations
            counter_configs = [
                {
                    "label": "Total Tickets",
                    "document_type": "Airplane Ticket",
                    "function": "Count",
                    "color": "#FF5858",
                    "filters_json": "[]"
                },
                {
                    "label": "Confirmed Tickets", 
                    "document_type": "Airplane Ticket",
                    "function": "Count",
                    "color": "#29CD42",
                    "filters_json": "[[\"Airplane Ticket\",\"status\",\"in\",[\"Booked\",\"Checked-In\",\"Boarded\"]]]"
                },
                {
                    "label": "Cancelled Tickets",
                    "document_type": "Airplane Ticket", 
                    "function": "Count",
                    "color": "#FF8D2D",
                    "filters_json": "[[\"Airplane Ticket\",\"status\",\"=\",\"Cancelled\"]]"
                },
                {
                    "label": "Total Flights",
                    "document_type": "Airplane Flight",
                    "function": "Count", 
                    "color": "#5E64FF",
                    "filters_json": "[]"
                },
                {
                    "label": "Total Revenue",
                    "document_type": "Airplane Ticket",
                    "function": "Sum",
                    "aggregate_function_based_on": "total_price",
                    "color": "#28A745",
                    "filters_json": "[[\"Airplane Ticket\",\"status\",\"!=\",\"Cancelled\"]]"
                }
            ]
            
            # Clear existing number cards
            workspace.number_cards = []
            
            # Add new number cards
            for config in counter_configs:
                workspace.append("number_cards", {
                    "label": config["label"],
                    "document_type": config["document_type"],
                    "function": config["function"],
                    "aggregate_function_based_on": config.get("aggregate_function_based_on", ""),
                    "color": config["color"],
                    "filters_json": config["filters_json"],
                    "is_public": 1,
                    "show_percentage_stats": 1,
                    "stats_time_interval": "Daily"
                })
            
            workspace.save()
            print("✅ Updated workspace counters")
            
    except Exception as e:
        print(f"Warning: Could not update workspace counters: {str(e)}")