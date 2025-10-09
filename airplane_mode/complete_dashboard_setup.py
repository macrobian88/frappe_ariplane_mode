#!/usr/bin/env python3
"""
Complete Airplane Mode Dashboard Setup Script
This script ensures all dashboard components are properly configured
"""

import frappe
import json
import os

def setup_complete_dashboard():
    """
    Complete dashboard setup with all counters and workspace configuration
    """
    print("🚀 Setting up Complete Airplane Mode Dashboard...")
    
    try:
        # 1. Update Airplane Ticket status options
        update_airplane_ticket_status()
        
        # 2. Install/Update workspace with counters
        setup_workspace_with_counters()
        
        # 3. Create dashboard charts
        setup_dashboard_charts()
        
        # 4. Test API endpoints
        test_dashboard_apis()
        
        # 5. Create sample cancelled tickets
        create_sample_data()
        
        print("✅ Complete dashboard setup finished successfully!")
        print_dashboard_access_info()
        
    except Exception as e:
        print(f"❌ Error during dashboard setup: {str(e)}")
        frappe.log_error(f"Complete dashboard setup error: {str(e)}")

def update_airplane_ticket_status():
    """Update Airplane Ticket DocType to include Cancelled status"""
    print("🔧 Updating Airplane Ticket status options...")
    
    try:
        # Get the DocType
        if not frappe.db.exists("DocType", "Airplane Ticket"):
            print("⚠️ Airplane Ticket DocType not found")
            return
            
        doctype_doc = frappe.get_doc("DocType", "Airplane Ticket")
        
        # Find status field
        status_field = None
        for field in doctype_doc.fields:
            if field.fieldname == "status":
                status_field = field
                break
        
        if status_field:
            current_options = status_field.options or ""
            if "Cancelled" not in current_options:
                status_field.options = "Booked\nChecked-In\nBoarded\nCancelled"
                doctype_doc.save()
                frappe.clear_cache(doctype="Airplane Ticket")
                frappe.reload_doctype("Airplane Ticket")
                print("   ✅ Added 'Cancelled' status successfully")
            else:
                print("   ℹ️ 'Cancelled' status already exists")
        else:
            print("   ⚠️ Status field not found")
            
    except Exception as e:
        print(f"   ❌ Error updating status: {str(e)}")

def setup_workspace_with_counters():
    """Setup or update the Airplane Mode workspace with proper counters"""
    print("🔧 Setting up Airplane Mode workspace with counters...")
    
    try:
        # Workspace configuration
        workspace_data = {
            "doctype": "Workspace",
            "name": "Airplane Mode",
            "title": "Airplane Mode",
            "category": "Modules",
            "icon": "airplane",
            "is_standard": 1,
            "module": "Airplane Mode", 
            "label": "Airplane Mode",
            "public": 1,
            "extends_another_page": 0,
            "is_hidden": 0,
            "content": json.dumps([
                {"id": "dashboard_counters", "type": "number_card", "data": {"number_card_name": "Dashboard Counters", "col": 12}},
                {"id": "flight_operations", "type": "card", "data": {"card_name": "Flight Operations", "col": 6}},
                {"id": "passenger_management", "type": "card", "data": {"card_name": "Passenger Management", "col": 6}},
                {"id": "aircraft_management", "type": "card", "data": {"card_name": "Aircraft Management", "col": 6}},
                {"id": "reports_analytics", "type": "card", "data": {"card_name": "Reports & Analytics", "col": 6}}
            ])
        }
        
        # Counter configurations
        number_cards = [
            {
                "label": "Total Tickets",
                "document_type": "Airplane Ticket",
                "function": "Count",
                "color": "#FF5858",
                "filters_json": "[]"
            },
            {
                "label": "Total Flights", 
                "document_type": "Airplane Flight",
                "function": "Count",
                "color": "#29CD42",
                "filters_json": "[]"
            },
            {
                "label": "Confirmed Tickets",
                "document_type": "Airplane Ticket",
                "function": "Count",
                "color": "#5E64FF", 
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
                "label": "Completed Flights",
                "document_type": "Airplane Flight", 
                "function": "Count",
                "color": "#28A745",
                "filters_json": "[[\"Airplane Flight\",\"status\",\"=\",\"Completed\"]]"
            },
            {
                "label": "Scheduled Flights",
                "document_type": "Airplane Flight",
                "function": "Count",
                "color": "#17A2B8",
                "filters_json": "[[\"Airplane Flight\",\"status\",\"=\",\"Scheduled\"]]"
            },
            {
                "label": "Total Revenue",
                "document_type": "Airplane Ticket",
                "function": "Sum",
                "aggregate_function_based_on": "total_price",
                "color": "#FFC107",
                "filters_json": "[[\"Airplane Ticket\",\"status\",\"!=\",\"Cancelled\"]]"
            },
            {
                "label": "Total Passengers",
                "document_type": "Airplane Flight",
                "function": "Sum",
                "aggregate_function_based_on": "occupancy_count", 
                "color": "#6F42C1",
                "filters_json": "[]"
            }
        ]
        
        # Links configuration
        links = [
            {"label": "Airplane Flight", "link_to": "Airplane Flight", "link_type": "DocType"},
            {"label": "Airplane Ticket", "link_to": "Airplane Ticket", "link_type": "DocType"},
            {"label": "Flight Passenger", "link_to": "Flight Passenger", "link_type": "DocType"},
            {"label": "Airplane", "link_to": "Airplane", "link_type": "DocType"},
            {"label": "Airline", "link_to": "Airline", "link_type": "DocType"},
            {"label": "Airport", "link_to": "Airport", "link_type": "DocType"}
        ]
        
        # Shortcuts configuration
        shortcuts = [
            {
                "label": "Airplane Flight",
                "link_to": "Airplane Flight", 
                "type": "DocType",
                "color": "Grey",
                "stats_filter": "{\"status\":[\"=\",\"Scheduled\"]}",
                "format": "{} Scheduled"
            },
            {
                "label": "Airplane Ticket",
                "link_to": "Airplane Ticket",
                "type": "DocType",
                "color": "Grey",
                "stats_filter": "{\"status\":[\"!=\",\"Cancelled\"]}",
                "format": "{} Active"
            }
        ]
        
        # Create or update workspace
        if frappe.db.exists("Workspace", "Airplane Mode"):
            workspace = frappe.get_doc("Workspace", "Airplane Mode")
            workspace.update(workspace_data)
        else:
            workspace = frappe.get_doc(workspace_data)
        
        # Clear existing data
        workspace.number_cards = []
        workspace.links = []
        workspace.shortcuts = []
        
        # Add number cards
        for card_config in number_cards:
            workspace.append("number_cards", {
                "label": card_config["label"],
                "document_type": card_config["document_type"],
                "function": card_config["function"],
                "aggregate_function_based_on": card_config.get("aggregate_function_based_on", ""),
                "color": card_config["color"],
                "filters_json": card_config["filters_json"],
                "is_public": 1,
                "show_percentage_stats": 1,
                "stats_time_interval": "Daily"
            })
        
        # Add links
        for link_config in links:
            workspace.append("links", {
                "label": link_config["label"],
                "link_to": link_config["link_to"],
                "link_type": link_config["link_type"],
                "is_query_report": 0,
                "hidden": 0
            })
            
        # Add shortcuts
        for shortcut_config in shortcuts:
            workspace.append("shortcuts", shortcut_config)
        
        workspace.save()
        print("   ✅ Workspace with counters created/updated successfully")
        
    except Exception as e:
        print(f"   ❌ Error setting up workspace: {str(e)}")

def setup_dashboard_charts():
    """Setup dashboard charts"""
    print("🔧 Setting up dashboard charts...")
    
    try:
        charts = [
            {
                "name": "Flight Status Overview",
                "chart_name": "Flight Status Overview",
                "chart_type": "Donut",
                "doctype": "Dashboard Chart",
                "document_type": "Airplane Flight",
                "based_on": "status",
                "is_public": 1,
                "module": "Airplane Mode"
            },
            {
                "name": "Ticket Status Overview",
                "chart_name": "Ticket Status Overview", 
                "chart_type": "Donut",
                "doctype": "Dashboard Chart",
                "document_type": "Airplane Ticket",
                "based_on": "status",
                "is_public": 1,
                "module": "Airplane Mode"
            }
        ]
        
        for chart_config in charts:
            if not frappe.db.exists("Dashboard Chart", chart_config["name"]):
                chart = frappe.get_doc(chart_config)
                chart.insert()
                print(f"   ✅ Created chart: {chart_config['name']}")
            else:
                print(f"   ℹ️ Chart already exists: {chart_config['name']}")
                
    except Exception as e:
        print(f"   ❌ Error setting up charts: {str(e)}")

def test_dashboard_apis():
    """Test dashboard API endpoints"""
    print("🔧 Testing dashboard API endpoints...")
    
    try:
        # Test main dashboard API
        from airplane_mode.api.dashboard import get_airplane_dashboard_data
        result = get_airplane_dashboard_data()
        
        if result.get('success'):
            data = result.get('data', {})
            counters = data.get('counters', {})
            print(f"   ✅ API working - Total Tickets: {counters.get('total_tickets', 0)}")
            print(f"   ✅ API working - Total Flights: {counters.get('total_flights', 0)}")
            print(f"   ✅ API working - Confirmed Tickets: {counters.get('confirmed_tickets', 0)}")
        else:
            print(f"   ⚠️ API test failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"   ❌ Error testing APIs: {str(e)}")

def create_sample_data():
    """Create sample cancelled tickets for demonstration"""
    print("🔧 Creating sample data...")
    
    try:
        # Check if we need sample cancelled tickets
        cancelled_count = frappe.db.count("Airplane Ticket", {"status": "Cancelled"})
        
        if cancelled_count == 0:
            # Get existing tickets
            existing_tickets = frappe.get_list("Airplane Ticket", 
                                             filters={"status": ["!=", "Cancelled"]}, 
                                             limit=1)
            
            if existing_tickets:
                original_ticket = frappe.get_doc("Airplane Ticket", existing_tickets[0].name)
                new_ticket = frappe.copy_doc(original_ticket)
                new_ticket.status = "Cancelled"
                new_ticket.insert()
                print(f"   ✅ Created sample cancelled ticket: {new_ticket.name}")
            else:
                print("   ℹ️ No existing tickets to copy for cancelled sample")
        else:
            print(f"   ℹ️ {cancelled_count} cancelled ticket(s) already exist")
            
    except Exception as e:
        print(f"   ❌ Error creating sample data: {str(e)}")

def print_dashboard_access_info():
    """Print information about accessing the dashboard"""
    print("\n" + "="*60)
    print("🎉 AIRPLANE MODE DASHBOARD SETUP COMPLETE!")
    print("="*60)
    
    print("\n📊 Dashboard Features:")
    print("   • Total Tickets Counter")
    print("   • Total Flights Counter")
    print("   • Confirmed Tickets Counter") 
    print("   • Cancelled Tickets Counter")
    print("   • Completed Flights Counter")
    print("   • Scheduled Flights Counter")
    print("   • Total Revenue Counter")
    print("   • Total Passengers Counter")
    
    print("\n🌐 Access Your Dashboard:")
    print("   • Go to: Airplane Mode workspace")
    print("   • URL: https://airplane-mode.m.frappe.cloud/app/airplane-mode")
    print("   • You should now see 8 colorful counter cards!")
    
    print("\n⚡ API Endpoints Available:")
    print("   • airplane_mode.api.dashboard.get_airplane_dashboard_data")
    print("   • airplane_mode.api.dashboard.get_ticket_statistics")
    print("   • airplane_mode.api.dashboard.get_flight_statistics")
    
    print("\n🔄 If Counters Don't Show:")
    print("   1. Refresh your browser page") 
    print("   2. Clear browser cache")
    print("   3. Check if 'Cancelled' status was added to Airplane Ticket")
    print("   4. Wait 1-2 minutes for workspace to update")
    
    print("\n📱 Expected Results:")
    print("   • 8 colorful counter cards in the workspace")
    print("   • Real-time statistics")
    print("   • Working API endpoints")
    print("   • Charts showing status breakdowns")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    if frappe.db:
        setup_complete_dashboard()
    else:
        print("Please run this script in a Frappe environment")
        print("Example: bench --site your-site execute airplane_mode.complete_dashboard_setup.setup_complete_dashboard")