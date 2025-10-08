# Copyright (c) 2024, macrobian88 and contributors
# For license information, please see license.txt

import frappe


def execute():
    """Remove unused DocTypes and their data safely"""
    
    frappe.logger().info("Starting cleanup of unused DocTypes")
    
    # List of DocTypes to remove
    doctypes_to_remove = [
        "Rent Remainder Alerts",
        "Monthly Invoice", 
        "Airport Shop Settings",
        "Monthly Bill"
    ]
    
    for doctype_name in doctypes_to_remove:
        try:
            frappe.logger().info(f"Processing DocType: {doctype_name}")
            
            # Check if DocType exists
            if not frappe.db.exists("DocType", doctype_name):
                frappe.logger().info(f"DocType {doctype_name} does not exist, skipping")
                continue
                
            # Check if table exists
            table_name = f"tab{doctype_name}"
            if frappe.db.table_exists(table_name):
                # Get count of records
                count = frappe.db.count(doctype_name)
                frappe.logger().info(f"Found {count} records in {doctype_name}")
                
                if count > 0:
                    frappe.logger().info(f"Deleting {count} records from {doctype_name}")
                    # Delete all records first
                    frappe.db.sql(f"DELETE FROM `{table_name}`")
            
            # Remove from DocType table
            frappe.logger().info(f"Removing DocType definition: {doctype_name}")
            frappe.db.sql("DELETE FROM `tabDocType` WHERE name = %s", (doctype_name,))
            
            # Remove any custom fields related to this DocType
            frappe.db.sql("DELETE FROM `tabCustom Field` WHERE dt = %s", (doctype_name,))
            
            # Remove any property setters
            frappe.db.sql("DELETE FROM `tabProperty Setter` WHERE doc_type = %s", (doctype_name,))
            
            # Remove any client scripts
            frappe.db.sql("DELETE FROM `tabClient Script` WHERE dt = %s", (doctype_name,))
            
            # Remove any server scripts
            frappe.db.sql("DELETE FROM `tabServer Script` WHERE document_type = %s", (doctype_name,))
            
            # Remove any print formats
            frappe.db.sql("DELETE FROM `tabPrint Format` WHERE doc_type = %s", (doctype_name,))
            
            # Remove any reports
            frappe.db.sql("DELETE FROM `tabReport` WHERE ref_doctype = %s", (doctype_name,))
            
            # Remove any web forms
            frappe.db.sql("DELETE FROM `tabWeb Form` WHERE doc_type = %s", (doctype_name,))
            
            # Remove any dashboard charts
            frappe.db.sql("DELETE FROM `tabDashboard Chart` WHERE document_type = %s", (doctype_name,))
            
            # Remove any notification logs
            frappe.db.sql("DELETE FROM `tabNotification Log` WHERE document_type = %s", (doctype_name,))
            
            # Remove any email queue entries
            frappe.db.sql("DELETE FROM `tabEmail Queue` WHERE reference_doctype = %s", (doctype_name,))
            
            frappe.logger().info(f"Successfully removed DocType: {doctype_name}")
            
        except Exception as e:
            frappe.logger().error(f"Error removing DocType {doctype_name}: {str(e)}")
            # Log the error but continue with other DocTypes
            frappe.log_error(f"DocType Removal Error: {str(e)}", f"cleanup_unused_doctypes_{doctype_name}")
    
    # Commit all changes
    frappe.db.commit()
    frappe.logger().info("Completed cleanup of unused DocTypes")
    
    # Clear cache to ensure changes take effect
    frappe.clear_cache()
    frappe.logger().info("Cache cleared after DocType cleanup")
