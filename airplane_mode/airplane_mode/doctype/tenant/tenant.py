# Copyright (c) 2025, nandhakishore and contributors
# For license information, please see license.txt

# import frappe
# apps/airplane_mode/airplane_mode/doctype/tenant/tenant.py
import frappe
from frappe.model.document import Document

class Tenant(Document):
    def after_insert(self):
        self._set_shop_occupied(True)

    def on_trash(self):
        self._set_shop_occupied(False)

    def _set_shop_occupied(self, value: bool):
        if self.shop:
            frappe.db.set_value("Airport Shop", self.shop, "is_occupied", value)
