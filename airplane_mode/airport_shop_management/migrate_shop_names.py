# Migration utility to populate airport_name and shop_type_name fields
# This should be run after updating the Airport Shop doctype

import frappe

def execute():
    """Populate airport_name and shop_type_name fields for existing Airport Shop records"""
    
    print("Starting Airport Shop field population...")
    
    # Get all Airport Shop records
    shops = frappe.get_all("Airport Shop", 
        fields=["name", "airport", "shop_type", "airport_name", "shop_type_name"]
    )
    
    updated_count = 0
    
    for shop in shops:
        doc = frappe.get_doc("Airport Shop", shop.name)
        needs_update = False
        
        # Populate airport_name if missing
        if shop.airport and not shop.airport_name:
            try:
                airport_doc = frappe.get_doc("Airport", shop.airport)
                doc.airport_name = airport_doc.airport_name
                needs_update = True
                print(f"Updated airport_name for {shop.name}: {airport_doc.airport_name}")
            except Exception as e:
                print(f"Error updating airport_name for {shop.name}: {e}")
        
        # Populate shop_type_name if missing
        if shop.shop_type and not shop.shop_type_name:
            try:
                shop_type_doc = frappe.get_doc("Shop Type", shop.shop_type)
                doc.shop_type_name = shop_type_doc.shop_type_name
                needs_update = True
                print(f"Updated shop_type_name for {shop.name}: {shop_type_doc.shop_type_name}")
            except Exception as e:
                print(f"Error updating shop_type_name for {shop.name}: {e}")
        
        # Save if changes were made
        if needs_update:
            doc.flags.ignore_validate = True  # Skip validation during migration
            doc.save()
            updated_count += 1
    
    frappe.db.commit()
    print(f"Migration completed. Updated {updated_count} records.")

if __name__ == "__main__":
    execute()