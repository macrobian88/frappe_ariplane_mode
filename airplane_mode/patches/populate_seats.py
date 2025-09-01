import random
import string
import frappe

def execute():
    letters = ["A", "B", "C", "D", "E", "F"]

    tickets = frappe.get_all("Airplane Ticket", filters={"seat": ""}, fields=["name", "flight"])

    for ticket in tickets:
        existing = frappe.get_all(
            "Airplane Ticket",
            filters={"flight": ticket.flight, "docstatus": ["<", 2]},
            pluck="seat"
        )

        occupied = {s for s in existing if s}
        row = 1
        while True:
            for letter in letters:
                seat = f"{row}{letter}"
                if seat not in occupied:
                    frappe.db.set_value("Airplane Ticket", ticket.name, "seat", seat)
                    occupied.add(seat)
                    break
            else:
                row += 1
                continue
            break
