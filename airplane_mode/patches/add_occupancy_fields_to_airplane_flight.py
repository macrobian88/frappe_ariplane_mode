import frappe
from frappe.model.utils.rename_field import rename_field
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    """
    Patch to add occupancy fields to Airplane Flight DocType
    and calculate occupancy for existing flights.
    """
    frappe.logger().info("Starting occupancy fields migration for Airplane Flight")
    
    try:
        # Add custom fields if they don't exist
        add_occupancy_fields()
        
        # Recalculate occupancy for all existing flights
        recalculate_all_flight_occupancy()
        
        frappe.logger().info("Successfully completed occupancy fields migration")
        
    except Exception as e:
        frappe.logger().error(f"Error in occupancy fields migration: {e}")
        raise


def add_occupancy_fields():
    """Add occupancy fields to Airplane Flight DocType."""
    frappe.logger().info("Adding occupancy fields to Airplane Flight DocType")
    
    # Check if fields already exist
    if frappe.db.exists("DocField", {"parent": "Airplane Flight", "fieldname": "occupancy_count"}):
        frappe.logger().info("Occupancy fields already exist, skipping creation")
        return
    
    # Define custom fields
    custom_fields = {
        "Airplane Flight": [
            {
                "fieldname": "occupancy_section",
                "fieldtype": "Section Break",
                "label": "Flight Occupancy",
                "insert_after": "capacity"
            },
            {
                "fieldname": "occupancy_count",
                "fieldtype": "Int",
                "label": "Booked Passengers",
                "default": 0,
                "non_negative": 1,
                "read_only": 1,
                "in_list_view": 1,
                "insert_after": "occupancy_section"
            },
            {
                "fieldname": "occupancy_percentage",
                "fieldtype": "Percent",
                "label": "Occupancy %",
                "default": 0,
                "precision": 2,
                "read_only": 1,
                "in_list_view": 1,
                "insert_after": "occupancy_count"
            },
            {
                "fieldname": "column_break_occupancy",
                "fieldtype": "Column Break",
                "insert_after": "occupancy_percentage"
            }
        ]
    }
    
    # Create the custom fields
    create_custom_fields(custom_fields, update=True)
    frappe.logger().info("Occupancy custom fields created successfully")


def recalculate_all_flight_occupancy():
    """Recalculate occupancy for all existing flights."""
    frappe.logger().info("Recalculating occupancy for all flights")
    
    # Get all flights
    flights = frappe.get_all("Airplane Flight", fields=["name", "capacity"])
    
    for flight in flights:
        try:
            calculate_flight_occupancy(flight.name, flight.capacity)
        except Exception as e:
            frappe.logger().error(f"Error calculating occupancy for flight {flight.name}: {e}")
    
    frappe.db.commit()
    frappe.logger().info(f"Recalculated occupancy for {len(flights)} flights")


def calculate_flight_occupancy(flight_name, capacity):
    """Calculate occupancy for a specific flight."""
    # Count tickets for this flight (excluding cancelled tickets)
    booked_tickets = frappe.db.count(
        "Airplane Ticket",
        filters={
            "flight": flight_name,
            "docstatus": ["!=", 2]  # Don't count cancelled tickets
        }
    )
    
    # Calculate occupancy percentage
    occupancy_count = booked_tickets
    occupancy_percentage = 0
    
    if capacity and capacity > 0:
        occupancy_percentage = round((booked_tickets / capacity) * 100, 2)
    
    # Update the flight document
    frappe.db.set_value("Airplane Flight", flight_name, {
        "occupancy_count": occupancy_count,
        "occupancy_percentage": occupancy_percentage
    }, update_modified=False)
    
    frappe.logger().debug(f"Flight {flight_name}: {occupancy_count}/{capacity} ({occupancy_percentage}%)")
