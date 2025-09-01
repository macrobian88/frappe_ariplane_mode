
# import random
# import string
# import frappe
# from frappe.model.document import Document


# class AirplaneTicket(Document):
# 	"""A passenger’s ticket for a given Airplane Flight."""

# 	# ────────────────────────────────────────────────────────────
# 	# VALIDATE: runs every time the document is saved
# 	# ────────────────────────────────────────────────────────────
# 	def validate(self):
# 		self._deduplicate_add_ons()
# 		self._set_total_amount()

# 		# make sure a seat exists (covers Save after Web Form too)
# 		if not self.seat:
# 			self.seat = self._random_seat()

# 		# NEW: block if flight is already full
# 		self._check_capacity()

# 		gate_number = frappe.db.get_value("Airplane Flight", self.flight, "gate_number")
# 		if gate_number:
# 			frappe.enqueue(
# 				'airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_gate_number_for_flight',
# 				flight_name=self.flight,
# 				gate_number=gate_number,
# 				queue='default'
# 			)


# 	# ────────────────────────────────────────────────────────────
# 	# BEFORE INSERT: runs only the very first time the doc is saved
# 	# ────────────────────────────────────────────────────────────
# 	def before_insert(self):
# 		if not self.seat:                        # brand‑new doc → pick seat
# 			self.seat = self._random_seat()

# 	# ────────────────────────────────────────────────────────────
# 	# BEFORE SUBMIT: block submission unless already “Boarded”
# 	# ────────────────────────────────────────────────────────────
# 	def before_submit(self):
# 		if self.status != "Boarded":
# 			frappe.throw("Cannot submit ticket unless Status = Boarded")

# 	# ===========================================================
# 	# HELPER METHODS
# 	# ===========================================================
# 	def _deduplicate_add_ons(self):
# 		"""Remove duplicate ‘Item’ rows inside child table add_ons."""
# 		seen, unique_rows = set(), []
# 		for row in self.add_ons:
# 			if row.item not in seen:
# 				seen.add(row.item)
# 				unique_rows.append(row)
# 		self.add_ons = unique_rows

# 	def _set_total_amount(self):
# 		"""Flight Price + Σ(add‑on amounts)."""
# 		add_on_sum = sum(d.amount or 0 for d in self.add_ons)
# 		self.total_amount = (self.flight_price or 0) + add_on_sum

# 	def _random_seat(self) -> str:
# 		"""Return something like ‘23B’ (1‑99 + A‑E)."""
# 		number = random.randint(1, 99)
# 		letter = random.choice(list("ABCDE"))
# 		return f"{number}{letter}"

# 	def _check_capacity(self):
# 		"""
# 		Block creation if total submitted tickets for this flight
# 		already equals or exceeds Airplane Flight.capacity.
# 		"""
# 		if not self.flight:
# 			return  # safety

# 		flight = frappe.get_doc("Airplane Flight", self.flight)
# 		capacity = flight.capacity or 0
# 		if capacity == 0:
# 			return  # treat 0 as “unlimited”

# 		# count submitted tickets (docstatus = 1) for this flight
# 		current_tickets = frappe.db.count("Airplane Ticket", {
# 			"flight": self.flight,
# 			"docstatus": 1
# 		})

# 		# when validating a draft (docstatus 0) we must include this one
# 		if current_tickets + 1 > capacity:
# 			frappe.throw(
# 				f"Cannot book ticket: flight {self.flight} is already full "
# 				f"({capacity} seats)."
# 			)

import random
import frappe
from frappe.model.document import Document

class AirplaneTicket(Document):

    def validate(self):
        self._deduplicate_add_ons()
        self._set_total_amount()
        if not self.seat:
            self.seat = self._random_seat()
        self._check_capacity()

    def before_insert(self):
        if not self.seat:
            self.seat = self._random_seat()

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw("Cannot submit ticket unless Status = Boarded")

    def on_submit(self):
        """When ticket is submitted, enqueue background job to sync gate number."""
        gate_number = frappe.db.get_value("Airplane Flight", self.flight, "gate_number")
        if gate_number:
            frappe.enqueue(
                "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_gate_number_for_flight",
                flight_name=self.flight,
                gate_number=gate_number,
                update_drafts=False,   # only submitted tickets
                queue="default"
            )

    def _deduplicate_add_ons(self):
        seen, unique_rows = set(), []
        for row in self.add_ons:
            if row.item not in seen:
                seen.add(row.item)
                unique_rows.append(row)
        self.add_ons = unique_rows

    def _set_total_amount(self):
        add_on_sum = sum(d.amount or 0 for d in self.add_ons)
        self.total_amount = (self.flight_price or 0) + add_on_sum

    def _random_seat(self) -> str:
        number = random.randint(1, 99)
        letter = random.choice(list("ABCDE"))
        return f"{number}{letter}"

    def _check_capacity(self):
        if not self.flight:
            return
        flight = frappe.get_doc("Airplane Flight", self.flight)
        capacity = flight.capacity or 0
        if capacity == 0:
            return
        current_tickets = frappe.db.count("Airplane Ticket", {
            "flight": self.flight,
            "docstatus": 1
        })
        if current_tickets + 1 > capacity:
            frappe.throw(
                f"Cannot book ticket: flight {self.flight} is already full ({capacity} seats)."
            )
