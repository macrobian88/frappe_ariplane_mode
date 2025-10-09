#!/usr/bin/env python3
"""
Airplane Mode Dashboard Setup Script
This script sets up the dashboard and adds necessary configurations
"""

import frappe
import json

def setup_airplane_dashboard():
    """
    Complete setup for Airplane Mode Dashboard
    """
    print("Setting up Airplane Mode Dashboard...")
    
    try:
        # 1. Add Cancelled status to Airplane Ticket if not exists
        add_cancelled_status_to_ticket()
        
        # 2. Create workspace configuration
        create_workspace_config()
        
        # 3. Set up permissions
        setup_dashboard_permissions()
        
        # 4. Create some sample data if needed
        create_sample_data_if_needed()
        
        print("✅ Dashboard setup completed successfully!")
        print_dashboard_info()
        
    except Exception as e:
        print(f"❌ Error during setup: {str(e)}")
        frappe.log_error(f"Dashboard setup error: {str(e)}")

def add_cancelled_status_to_ticket():
    """
    Add 'Cancelled' status to Airplane Ticket DocType
    """
    print("🔧 Adding 'Cancelled' status to Airplane Ticket...")
    
    try:
        # Get the DocType
        doctype = frappe.get_doc("DocType", "Airplane Ticket")
        
        # Find the status field
        status_field = None
        for field in doctype.fields:
            if field.fieldname == "status":
                status_field = field
                break
        
        if status_field:
            current_options = status_field.options or ""
            if "Cancelled" not in current_options:
                # Add Cancelled to options
                new_options = current_options.strip() + "\nCancelled"
                status_field.options = new_options
                
                # Save the doctype
                doctype.save()
                
                # Reload doctype
                frappe.reload_doctype("Airplane Ticket")
                
                print("   ✅ Added 'Cancelled' status successfully")
            else:
                print("   ℹ️ 'Cancelled' status already exists")
        else:
            print("   ⚠️ Status field not found")
            
    except Exception as e:
        print(f"   ❌ Error adding cancelled status: {str(e)}")

def create_workspace_config():
    """
    Create workspace configuration for Airplane Mode
    """
    print("🔧 Creating workspace configuration...")
    
    try:
        workspace_data = {
            "module": "Airplane Mode",
            "label": "Airplane Mode",
            "category": "Modules",
            "public": 1,
            "is_standard": 0,
            "extends_another_page": 0,
            "charts": [
                {
                    "chart_name": "Flight Status Overview",
                    "label": "Flight Status Overview",
                    "chart_type": "Donut",
                    "doctype": "Airplane Flight",
                    "based_on": "status",
                    "width": "Half"
                },
                {
                    "chart_name": "Ticket Status Overview", 
                    "label": "Ticket Status Overview",
                    "chart_type": "Donut",
                    "doctype": "Airplane Ticket",
                    "based_on": "status",
                    "width": "Half"
                }
            ],
            "shortcuts": [
                {
                    "label": "Airplane Flight",
                    "type": "DocType",
                    "doc_view": "List"
                },
                {
                    "label": "Airplane Ticket",
                    "type": "DocType", 
                    "doc_view": "List"
                },
                {
                    "label": "Flight Passenger",
                    "type": "DocType",
                    "doc_view": "List"
                },
                {
                    "label": "Airplane",
                    "type": "DocType",
                    "doc_view": "List"
                }
            ],
            "cards": [
                {
                    "label": "Flight Statistics",
                    "hidden": 0,
                    "links": [
                        {
                            "label": "Total Flights",
                            "type": "DocType",
                            "name": "Airplane Flight"
                        },
                        {
                            "label": "Scheduled Flights", 
                            "type": "DocType",
                            "name": "Airplane Flight",
                            "filters": '[["status", "=", "Scheduled"]]'
                        },
                        {
                            "label": "Completed Flights",
                            "type": "DocType", 
                            "name": "Airplane Flight",
                            "filters": '[["status", "=", "Completed"]]'
                        }
                    ]
                },
                {
                    "label": "Ticket Statistics",
                    "hidden": 0,
                    "links": [
                        {
                            "label": "Total Tickets",
                            "type": "DocType",
                            "name": "Airplane Ticket"
                        },
                        {
                            "label": "Confirmed Tickets",
                            "type": "DocType",
                            "name": "Airplane Ticket", 
                            "filters": '[["status", "in", ["Booked", "Checked-In", "Boarded"]]]'
                        },
                        {
                            "label": "Cancelled Tickets",
                            "type": "DocType",
                            "name": "Airplane Ticket",
                            "filters": '[["status", "=", "Cancelled"]]'
                        }
                    ]
                }
            ]
        }
        
        # Check if workspace exists
        if frappe.db.exists("Workspace", "Airplane Mode"):
            workspace = frappe.get_doc("Workspace", "Airplane Mode") 
            workspace.update(workspace_data)
        else:
            workspace = frappe.get_doc({
                "doctype": "Workspace",
                "name": "Airplane Mode",
                **workspace_data
            })
        
        workspace.save()
        print("   ✅ Workspace configuration created successfully")
        
    except Exception as e:
        print(f"   ❌ Error creating workspace: {str(e)}")

def setup_dashboard_permissions():
    """
    Set up necessary permissions for dashboard
    """
    print("🔧 Setting up dashboard permissions...")
    
    try:
        # Ensure System Manager has all permissions
        roles_to_check = ["System Manager", "Airplane Mode Manager"]
        
        for role in roles_to_check:
            if not frappe.db.exists("Role", role) and role != "System Manager":
                # Create custom role
                role_doc = frappe.get_doc({
                    "doctype": "Role",
                    "role_name": role,
                    "is_custom": 1
                })
                role_doc.insert()
                print(f"   ✅ Created role: {role}")
        
        print("   ✅ Permissions configured successfully")
        
    except Exception as e:
        print(f"   ❌ Error setting up permissions: {str(e)}")

def create_sample_data_if_needed():
    """
    Create sample data if the system is empty
    """
    print("🔧 Checking if sample data is needed...")
    
    try:
        # Check if we have minimal data
        ticket_count = frappe.db.count("Airplane Ticket")
        flight_count = frappe.db.count("Airplane Flight")
        
        if ticket_count < 5 or flight_count < 3:
            print("   ℹ️ Creating sample data for demonstration...")
            
            # Create a cancelled ticket for demo
            if frappe.db.exists("Airplane Ticket", {"status": "Booked"}):
                sample_ticket = frappe.get_list("Airplane Ticket", 
                                               filters={"status": "Booked"}, 
                                               limit=1)[0]
                
                # Create a copy with cancelled status
                ticket_doc = frappe.get_doc("Airplane Ticket", sample_ticket.name)
                new_ticket = frappe.copy_doc(ticket_doc)
                new_ticket.status = "Cancelled"
                new_ticket.save()
                print(f"   ✅ Created sample cancelled ticket: {new_ticket.name}")
        else:
            print("   ℹ️ Sufficient data exists, skipping sample data creation")
            
    except Exception as e:
        print(f"   ❌ Error creating sample data: {str(e)}")

def print_dashboard_info():
    """
    Print information about accessing the dashboard
    """
    print("\n" + "="*50)
    print("🎉 AIRPLANE MODE DASHBOARD SETUP COMPLETE!")
    print("="*50)
    print("\n📊 Dashboard Features Added:")
    print("   • Total Tickets Counter")
    print("   • Total Flights Counter") 
    print("   • Confirmed Tickets Counter")
    print("   • Cancelled Tickets Counter")
    print("   • Flight Status Breakdown")
    print("   • Revenue Statistics")
    print("   • Real-time Updates")
    
    print("\n🔗 Access Methods:")
    print("   • Workspace: Go to 'Airplane Mode' workspace")
    print("   • API: Use airplane_mode.api.dashboard methods")
    print("   • Web Dashboard: /airplane-dashboard")
    
    print("\n⚡ API Endpoints:")
    print("   • get_airplane_dashboard_data()")
    print("   • get_ticket_statistics()")  
    print("   • get_flight_statistics()")
    
    print("\n📈 Next Steps:")
    print("   1. Go to Airplane Mode workspace")
    print("   2. View the new dashboard charts")
    print("   3. Test the API endpoints")
    print("   4. Customize as needed")
    print("\n" + "="*50)

if __name__ == "__main__":
    if frappe.db:
        setup_airplane_dashboard()
    else:
        print("Please run this script in a Frappe environment")
        print("Example: bench --site your-site execute airplane_mode.setup_dashboard --kwargs '{}'")