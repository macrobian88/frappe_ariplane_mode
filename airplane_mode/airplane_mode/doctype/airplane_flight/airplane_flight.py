# import frappe
# from frappe.website.website_generator import WebsiteGenerator
# from datetime import datetime


# class AirplaneFlight(WebsiteGenerator):
#     """Tracks a single flight and exposes it as a web page."""
    
#     def autoname(self):
#         today = datetime.today()
#         date_part = today.strftime("%m-%Y")
#         count = frappe.db.count("Airplane Flight") + 1
#         prefix = frappe.get_value("Airplane", self.airplane, "airline").upper()
#         self.name = f"{prefix}-{date_part}-{str(count).zfill(5)}"

#     def on_submit(self):
#         self.db_set("status", "Completed")


# def sync_gate_to_tickets(doc, method=None):
#     if not doc.gate_number:
#         return
#     frappe.enqueue(
#         'airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_gate_number_for_flight',
#         flight_name=doc.name,
#         gate_number=doc.gate_number,
#         queue='default'
#     )

# @frappe.whitelist()
# def update_gate_number_for_flight(flight_name, gate_number, batch_size=100):
#     offset = 0
#     while True:
#         tickets = frappe.db.get_list(
#             "Airplane Ticket",
#             filters={"flight": flight_name, "docstatus": 1},
#             fields=["name"],
#             limit=batch_size,
#             offset=offset
#         )
#         if not tickets:
#             break
#         ticket_names = [t.name for t in tickets]
#         frappe.db.bulk_update(
#             "Airplane Ticket",
#             [{"name": name, "gate_number": gate_number} for name in ticket_names],
#             update_modified=False,
#         )
#         frappe.db.commit()  # release locks per batch
#         offset += batch_size
import frappe
from frappe.website.website_generator import WebsiteGenerator
from datetime import datetime

class AirplaneFlight(WebsiteGenerator):

    def autoname(self):
            today = datetime.today()
            date_part = today.strftime("%m-%Y")
            count = frappe.db.count("Airplane Flight") + 1
            prefix = frappe.get_value("Airplane", self.airplane, "airline").upper()
            self.name = f"{prefix}-{date_part}-{str(count).zfill(5)}"

    def on_submit(self):
            self.db_set("status", "Completed")

    # def sync_gate_to_tickets(doc, method=None):
    #     """Update all tickets (draft + submitted) when flight's gate changes."""
    #     if not doc.gate_number:
    #         return
    #     frappe.enqueue(
    #         "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_gate_number_for_flight",
    #         flight_name=doc.name,
    #         gate_number=doc.gate_number,
    #         update_drafts=True,   # include draft tickets too
    #         queue="default"
    #     )
    def on_update(self):
        """
        Automatically enqueue ticket gate number updates when the flight gate changes.
        Works for both Draft and Submitted flights.
        """
        # frappe.enqueue(
        #     "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_gate_number_for_flight",
        #     flight_name=doc.name,
        #     gate_number=doc.gate_number,
        #     update_drafts=(doc.docstatus == 0),  # Allow draft tickets if flight is draft
        #     queue="default",  # can be "long" if tickets are many
        #     timeout=300
        # )
        update_gate_number_for_flight(self.name,self.gate_number,self.docstatus == 0)
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
    while True:
        print("test")
        tickets = frappe.db.get_list(
            "Airplane Ticket",
            filters={
                "flight": flight_name,
                "docstatus": ("in", docstatus_filter),
                "status": ("!=", "Boarded")
            },
            fields=["name"],
            start=start,
            page_length=batch_size
        )

        if not tickets:
            break

        # Correct format for bulk_update → {name: {"field": value}}
        update_map = {t.name: {"gate_number": gate_number} for t in tickets}
        frappe.db.bulk_update("Airplane Ticket", update_map, update_modified=False)
        frappe.db.commit()

        start += batch_size

    frappe.logger().info(f"[GateSync] Completed update for flight={flight_name}")
