# airplane_mode/config/airplane_mode.py

import frappe
from frappe import _

def get_data():
    return {
        "label": _("Airplane Mode"),
        "icon": "airplane",
        "items": [
            {
                "type": "doctype",
                "name": "Airplane Flight",
                "label": _("Airplane Flight"),
                "description": _("Manage flight schedules and details"),
            },
            {
                "type": "doctype", 
                "name": "Airplane Ticket",
                "label": _("Airplane Ticket"),
                "description": _("Manage passenger tickets and bookings"),
            },
            {
                "type": "doctype",
                "name": "Flight Passenger", 
                "label": _("Flight Passenger"),
                "description": _("Manage passenger information"),
            },
            {
                "type": "doctype",
                "name": "Airplane",
                "label": _("Airplane"),
                "description": _("Manage aircraft details"),
            },
            {
                "type": "doctype",
                "name": "Airline",
                "label": _("Airline"),
                "description": _("Manage airline information"),
            },
            {
                "type": "doctype",
                "name": "Airport",
                "label": _("Airport"),
                "description": _("Manage airport information"),
            },
            {
                "type": "separator"
            },
            {
                "type": "report",
                "name": "Flight Revenue Report",
                "label": _("Flight Revenue Report"),
                "is_query_report": True,
            },
            {
                "type": "report", 
                "name": "Flight Occupancy Report",
                "label": _("Flight Occupancy Report"),
                "is_query_report": True,
            }
        ]
    }