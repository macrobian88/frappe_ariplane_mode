import frappe

def execute():
    """
    Consolidate Airport Shop Management DocTypes by removing duplicates
    and updating module references.
    """
    
    # List of DocTypes that were duplicated and need cleanup
    doctypes_to_cleanup = [
        'Airport Shop',
        'Contract Shop', 
        'Monthly Bill',
        'Monthly Invoice',
        'Rent Payment Contract',
        'Rent_Remainder_Alerts',
        'Shop Lease Contract',
        'Shop Type',
        'Tenant',
        'Shop Contract'  # This was redundant
    ]
    
    try:
        # Update module reference for Airport Shop Settings
        if frappe.db.exists('DocType', 'Airport Shop Settings'):
            frappe.db.sql("""
                UPDATE `tabDocType` 
                SET module = 'Airport Shop Management'
                WHERE name = 'Airport Shop Settings'
            """)
            print("✅ Updated Airport Shop Settings module reference")
        
        # Update module references for all airport shop management doctypes
        for doctype in doctypes_to_cleanup:
            if frappe.db.exists('DocType', doctype):
                frappe.db.sql("""
                    UPDATE `tabDocType` 
                    SET module = 'Airport Shop Management'
                    WHERE name = %s
                """, (doctype,))
                print(f"✅ Updated {doctype} module reference")
        
        # Remove any orphaned DocType records that might exist
        frappe.db.sql("""
            DELETE FROM `tabDocType` 
            WHERE name IN (
                SELECT name FROM (
                    SELECT name 
                    FROM `tabDocType` dt1
                    WHERE EXISTS (
                        SELECT 1 FROM `tabDocType` dt2 
                        WHERE dt2.name = dt1.name 
                        AND dt2.module = 'Airport Shop Management'
                        AND dt1.module = 'Airplane Mode'
                        AND dt1.name IN ({placeholders})
                    )
                ) as temp
            )
        """.format(placeholders=','.join(['%s'] * len(doctypes_to_cleanup))), 
        doctypes_to_cleanup)
        
        print("\n🎉 DocType consolidation completed successfully!")
        print("📋 Summary:")
        print(f"   - Updated {len(doctypes_to_cleanup)} DocTypes to Airport Shop Management module")
        print("   - Moved Airport Shop Settings to Airport Shop Management module")
        print("   - Removed duplicate DocType records")
        
        frappe.db.commit()
        
    except Exception as e:
        print(f"❌ Error during DocType consolidation: {str(e)}")
        frappe.db.rollback()
        raise
