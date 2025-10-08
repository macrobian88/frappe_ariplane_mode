# Copyright (c) 2024, macrobian88 and contributors
# For license information, please see license.txt

import frappe


def execute():
    """Remove duplicate Shop Type entries before applying unique constraint"""
    
    frappe.logger().info("Starting removal of duplicate Shop Type entries")
    
    # Check if Shop Type table exists
    if not frappe.db.table_exists("tabShop Type"):
        frappe.logger().info("Shop Type table does not exist, skipping patch")
        return
    
    try:
        # Get all Shop Type records grouped by type_name
        duplicates = frappe.db.sql("""
            SELECT type_name, COUNT(*) as count, GROUP_CONCAT(name) as names
            FROM `tabShop Type`
            WHERE type_name IS NOT NULL AND type_name != ''
            GROUP BY type_name
            HAVING COUNT(*) > 1
        """, as_dict=True)
        
        if not duplicates:
            frappe.logger().info("No duplicate Shop Type entries found")
            return
            
        frappe.logger().info(f"Found {len(duplicates)} duplicate type_name entries")
        
        for duplicate in duplicates:
            type_name = duplicate.type_name
            names = duplicate.names.split(',')
            
            frappe.logger().info(f"Processing duplicates for type_name: {type_name}")
            frappe.logger().info(f"Found {len(names)} records: {names}")
            
            # Keep the first record (usually the oldest) and delete the rest
            records_to_keep = names[0]  # Keep the first one
            records_to_delete = names[1:]  # Delete the rest
            
            frappe.logger().info(f"Keeping record: {records_to_keep}")
            frappe.logger().info(f"Deleting records: {records_to_delete}")
            
            for record_name in records_to_delete:
                try:
                    # Delete the duplicate record
                    frappe.db.sql("""
                        DELETE FROM `tabShop Type` 
                        WHERE name = %s
                    """, (record_name.strip(),))
                    
                    frappe.logger().info(f"Deleted duplicate Shop Type record: {record_name.strip()}")
                    
                except Exception as e:
                    frappe.logger().error(f"Error deleting Shop Type record {record_name}: {str(e)}")
                    # Continue with other records
        
        # Commit the changes
        frappe.db.commit()
        frappe.logger().info("Successfully removed duplicate Shop Type entries")
        
        # Verify no more duplicates exist
        remaining_duplicates = frappe.db.sql("""
            SELECT type_name, COUNT(*) as count
            FROM `tabShop Type`
            WHERE type_name IS NOT NULL AND type_name != ''
            GROUP BY type_name
            HAVING COUNT(*) > 1
        """)
        
        if remaining_duplicates:
            frappe.logger().warning(f"Warning: {len(remaining_duplicates)} duplicates still remain")
        else:
            frappe.logger().info("Verification complete: No duplicate Shop Type entries remain")
            
    except Exception as e:
        frappe.logger().error(f"Error in remove_duplicate_shop_types patch: {str(e)}")
        # Don't raise the exception to avoid breaking the migration
        # The unique constraint will fail later and can be addressed manually
        frappe.log_error(f"Patch Error: {str(e)}", "remove_duplicate_shop_types")
