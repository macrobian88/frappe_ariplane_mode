import frappe
from frappe.website.website_generator import WebsiteGenerator
from datetime import datetime

class AirplaneFlight(WebsiteGenerator):
    """Tracks a single flight and exposes it as a web page."""

    def autoname(self):
        today = datetime.today()
        date_part = today.strftime("%m-%Y")
        count = frappe.db.count("Airplane Flight") + 1
        prefix = frappe.get_value("Airplane", self.airplane, "airline").upper()
        self.name = f"{prefix}-{date_part}-{str(count).zfill(5)}"

    def on_submit(self):
        self.db_set("status", "Completed")

    def after_insert(self):
        """Calculate occupancy after insertion."""
        self.calculate_occupancy()

    def on_update(self):
        """
        Automatically update ticket gate numbers when the flight gate changes.
        Works for both Draft and Submitted flights.
        Also recalculate occupancy on update.
        """
        # Calculate occupancy
        self.calculate_occupancy()
        
        if hasattr(self, '_previous_gate_number'):
            # Only update if gate number actually changed
            if self._previous_gate_number != self.gate_number:
                self.sync_gate_to_tickets()
        else:
            # First time or when gate number is set
            if self.gate_number:
                self.sync_gate_to_tickets()

    def calculate_occupancy(self):
        """Calculate current occupancy based on booked tickets."""
        if not self.name:
            return
        
        # Count tickets for this flight
        booked_tickets = frappe.db.count(
            "Airplane Ticket",
            filters={
                "flight": self.name,
                "docstatus": ["!=", 2]  # Don't count cancelled tickets
            }
        )
        
        # Calculate occupancy percentage
        occupancy_count = booked_tickets
        occupancy_percentage = 0
        
        if self.capacity and self.capacity > 0:
            occupancy_percentage = round((booked_tickets / self.capacity) * 100, 2)
        
        # Update the document directly in database to avoid recursion
        frappe.db.set_value("Airplane Flight", self.name, {
            "occupancy_count": occupancy_count,
            "occupancy_percentage": occupancy_percentage
        }, update_modified=False)

    def sync_gate_to_tickets(self):
        """Update all tickets when flight's gate changes."""
        if not self.gate_number:
            return
        
        # Use background job for better performance with many tickets
        frappe.enqueue(
            "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_gate_number_for_flight",
            flight_name=self.name,
            gate_number=self.gate_number,
            update_drafts=(self.docstatus == 0),  # Allow draft tickets if flight is draft
            queue="default",
            timeout=300
        )

@frappe.whitelist()
def update_gate_number_for_flight(flight_name, gate_number, batch_size=100, update_drafts=False):
    """
    Background job to update gate_number for all tickets in a given flight.
    Respects boarded status and optionally updates Draft tickets.
    """
    frappe.logger().info(
        f"[GateSync] Starting update for flight={flight_name}, gate={gate_number}, update_drafts={update_drafts}"
    )

    docstatus_filter = [1]  # Submitted tickets
    if update_drafts:
        docstatus_filter.append(0)  # Include Draft tickets

    start = 0
    total_updated = 0
    
    while True:
        tickets = frappe.db.get_list(
            "Airplane Ticket",
            filters={
                "flight": flight_name,
                "docstatus": ("in", docstatus_filter),
                "status": ("!=", "Boarded")  # Don't update boarded passengers
            },
            fields=["name"],
            start=start,
            page_length=batch_size
        )

        if not tickets:
            break

        # Update tickets in batch
        ticket_names = [t.name for t in tickets]
        for ticket_name in ticket_names:
            frappe.db.set_value("Airplane Ticket", ticket_name, "gate_number", gate_number, update_modified=False)
        
        frappe.db.commit()
        total_updated += len(tickets)
        start += batch_size

        # Log progress for large batches
        if total_updated % (batch_size * 5) == 0:
            frappe.logger().info(f"[GateSync] Updated {total_updated} tickets so far...")

    frappe.logger().info(f"[GateSync] Completed update for flight={flight_name}. Total tickets updated: {total_updated}")

@frappe.whitelist()
def recalculate_all_flight_occupancy():
    """
    Utility function to recalculate occupancy for all flights.
    Can be called manually when needed.
    """
    flights = frappe.get_all("Airplane Flight", fields=["name"])
    
    for flight in flights:
        flight_doc = frappe.get_doc("Airplane Flight", flight.name)
        flight_doc.calculate_occupancy()
    
    frappe.db.commit()
    return f"Updated occupancy for {len(flights)} flights"

def sync_gate_to_tickets(doc, method=None):
    """
    Hook function called from doc_events in hooks.py
    This is the function that was missing and causing the error.
    """
    if not hasattr(doc, 'gate_number') or not doc.gate_number:
        return
    
    # Store previous gate number to detect changes
    if method == "on_update" and hasattr(doc, '_doc_before_save'):
        previous_gate = getattr(doc._doc_before_save, 'gate_number', None)
        if previous_gate == doc.gate_number:
            return  # No change, skip update
    
    # Use background job for better performance
    frappe.enqueue(
        "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_gate_number_for_flight",
        flight_name=doc.name,
        gate_number=doc.gate_number,
        update_drafts=(doc.docstatus == 0),
        queue="default",
        timeout=300
    )

def update_flight_occupancy(doc, method=None):
    """
    Hook function to update flight occupancy when tickets are created/updated/cancelled.
    This should be called from Airplane Ticket hooks.
    """
    if hasattr(doc, 'flight') and doc.flight:
        try:
            flight_doc = frappe.get_doc("Airplane Flight", doc.flight)
            flight_doc.calculate_occupancy()
        except Exception as e:
            frappe.log_error(f"Error updating flight occupancy: {e}")
