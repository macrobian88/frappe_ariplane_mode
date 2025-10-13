# Copyright (c) 2025, Airplane Mode and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AirportShop(Document):
    def validate(self):
        """Validate shop data and auto-populate fields"""
        self.validate_shop_data()
        self.populate_linked_field_names()
        self.validate_tenant_status()
    
    def validate_shop_data(self):
        """Validate basic shop data"""
        if self.rent_per_month and self.rent_per_month < 0:
            frappe.throw("Rent per month cannot be negative")
        
        if self.area and self.area <= 0:
            frappe.throw("Shop area must be greater than 0")
        
        # Ensure shop number is unique
        if self.shop_number:
            existing = frappe.db.exists("Airport Shop", {
                "shop_number": self.shop_number,
                "name": ["!=", self.name]
            })
            if existing:
                frappe.throw(f"Shop number {self.shop_number} already exists")
    
    def populate_linked_field_names(self):
        """Auto-populate airport_name and shop_type_name from linked fields"""
        try:
            # Populate airport name
            if self.airport and not self.airport_name:
                airport_doc = frappe.get_doc("Airport", self.airport)
                self.airport_name = airport_doc.airport_name
            
            # Populate shop type name
            if self.shop_type and not self.shop_type_name:
                shop_type_doc = frappe.get_doc("Shop Type", self.shop_type)
                self.shop_type_name = shop_type_doc.shop_type_name
                
        except Exception as e:
            frappe.log_error(f"Error populating linked field names: {str(e)}", "Airport Shop Validation")
    
    def validate_tenant_status(self):
        """Validate tenant information based on status"""
        if self.status == "Occupied" and not self.tenant:
            frappe.throw("Tenant name is required when shop status is 'Occupied'")
        
        if self.status == "Available":
            # Clear tenant info when marking as available
            self.tenant = ""
            self.contact_number = ""
    
    def before_save(self):
        """Operations before saving the document"""
        # Auto-generate shop name if not provided
        if not self.shop_name and self.shop_number and self.shop_type_name:
            self.shop_name = f"{self.shop_type_name} Shop {self.shop_number}"
    
    def on_update(self):
        """Operations after updating the document"""
        self.update_lease_contracts()
    
    def update_lease_contracts(self):
        """Update related lease contracts when shop details change"""
        try:
            # Find active lease contracts for this shop
            contracts = frappe.get_all("Shop Lease Contract",
                filters={"contract_shop": self.name, "status": "Active"},
                fields=["name"]
            )
            
            for contract in contracts:
                # Update contract rent amount if shop rent changed
                if self.rent_per_month:
                    frappe.db.set_value("Shop Lease Contract", contract.name, 
                                      "rent_amount", self.rent_per_month)
            
            if contracts:
                frappe.db.commit()
                
        except Exception as e:
            frappe.log_error(f"Error updating lease contracts: {str(e)}", "Airport Shop Update")

# Utility functions for Airport Shop management

@frappe.whitelist()
def get_available_shops(airport=None, shop_type=None):
    """Get list of available shops with optional filters"""
    filters = {"status": "Available"}
    
    if airport:
        filters["airport"] = airport
    if shop_type:
        filters["shop_type"] = shop_type
    
    shops = frappe.get_all("Airport Shop",
        filters=filters,
        fields=["name", "shop_number", "shop_name", "airport_name", 
               "shop_type_name", "area", "rent_per_month", "description"],
        order_by="shop_number asc"
    )
    
    return shops

@frappe.whitelist()
def get_shop_statistics():
    """Get overall shop statistics"""
    try:
        stats = {}
        
        # Total shops
        stats["total_shops"] = frappe.db.count("Airport Shop")
        
        # Status breakdown
        stats["available"] = frappe.db.count("Airport Shop", {"status": "Available"})
        stats["occupied"] = frappe.db.count("Airport Shop", {"status": "Occupied"})
        stats["maintenance"] = frappe.db.count("Airport Shop", {"status": "Maintenance"})
        
        # Occupancy rate
        if stats["total_shops"] > 0:
            stats["occupancy_rate"] = round((stats["occupied"] / stats["total_shops"]) * 100, 1)
        else:
            stats["occupancy_rate"] = 0
        
        # Average rent
        avg_rent = frappe.db.sql("""
            SELECT AVG(rent_per_month) as avg_rent 
            FROM `tabAirport Shop` 
            WHERE rent_per_month > 0
        """, as_dict=1)
        
        stats["average_rent"] = avg_rent[0]["avg_rent"] if avg_rent and avg_rent[0]["avg_rent"] else 0
        
        # Revenue potential
        total_rent = frappe.db.sql("""
            SELECT SUM(rent_per_month) as total_rent 
            FROM `tabAirport Shop` 
            WHERE status = 'Occupied' AND rent_per_month > 0
        """, as_dict=1)
        
        stats["monthly_revenue"] = total_rent[0]["total_rent"] if total_rent and total_rent[0]["total_rent"] else 0
        
        return stats
        
    except Exception as e:
        frappe.log_error(f"Error getting shop statistics: {str(e)}", "Airport Shop Statistics")
        return {}

@frappe.whitelist()
def mark_shop_status(shop_name, new_status, tenant_name=None, reason=None):
    """Update shop status with optional tenant assignment"""
    try:
        if not frappe.has_permission("Airport Shop", "write"):
            frappe.throw("Not permitted to update shop status")
        
        shop = frappe.get_doc("Airport Shop", shop_name)
        
        # Update status
        shop.status = new_status
        
        # Handle tenant assignment
        if new_status == "Occupied" and tenant_name:
            shop.tenant = tenant_name
        elif new_status == "Available":
            shop.tenant = ""
            shop.contact_number = ""
        
        # Handle maintenance reason
        if new_status == "Maintenance" and reason:
            shop.description = reason
        
        shop.save()
        frappe.db.commit()
        
        return {"success": True, "message": f"Shop {shop_name} marked as {new_status}"}
        
    except Exception as e:
        frappe.log_error(f"Error updating shop status: {str(e)}", "Airport Shop Status Update")
        return {"success": False, "message": str(e)}

@frappe.whitelist()
def get_shops_by_airport(airport):
    """Get all shops for a specific airport with detailed information"""
    try:
        shops = frappe.get_all("Airport Shop",
            filters={"airport": airport},
            fields=["name", "shop_number", "shop_name", "shop_type_name", 
                   "status", "area", "rent_per_month", "tenant", "contact_number"],
            order_by="shop_number asc"
        )
        
        # Add status summary
        summary = {
            "total": len(shops),
            "available": len([s for s in shops if s.status == "Available"]),
            "occupied": len([s for s in shops if s.status == "Occupied"]),
            "maintenance": len([s for s in shops if s.status == "Maintenance"])
        }
        
        return {
            "shops": shops,
            "summary": summary
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting shops by airport: {str(e)}", "Airport Shop Query")
        return {"shops": [], "summary": {}}

@frappe.whitelist()
def create_bulk_shops(airport, shop_type, count, start_number=1, base_rent=0):
    """Create multiple shops in bulk for an airport"""
    try:
        if not frappe.has_permission("Airport Shop", "create"):
            frappe.throw("Not permitted to create shops")
        
        created_shops = []
        
        for i in range(int(count)):
            shop_number = f"{start_number + i:03d}"
            
            # Check if shop number already exists
            if frappe.db.exists("Airport Shop", {"shop_number": shop_number}):
                continue
            
            shop = frappe.new_doc("Airport Shop")
            shop.shop_number = shop_number
            shop.airport = airport
            shop.shop_type = shop_type
            shop.status = "Available"
            
            if float(base_rent) > 0:
                shop.rent_per_month = float(base_rent)
            
            shop.save()
            created_shops.append(shop.name)
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": f"Created {len(created_shops)} shops",
            "shops": created_shops
        }
        
    except Exception as e:
        frappe.log_error(f"Error creating bulk shops: {str(e)}", "Airport Shop Bulk Creation")
        return {"success": False, "message": str(e)}