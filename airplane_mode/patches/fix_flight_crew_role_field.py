import frappe

def execute():
    """Fix Flight Crew role field to fetch designation from Employee"""
    
    # Check if the Flight Crew doctype exists
    if not frappe.db.exists("DocType", "Flight Crew"):
        return
    
    # Get the role field from Flight Crew doctype
    role_field = frappe.db.get_value(
        "DocField", 
        {
            "parent": "Flight Crew",
            "fieldname": "role"
        }, 
        ["name", "fetch_from", "fieldtype", "options"]
    )
    
    if not role_field:
        return
    
    field_name = role_field[0]
    current_fetch_from = role_field[1]
    
    # Only update if the field is incorrectly configured
    if current_fetch_from == "crew_member.employee":
        frappe.db.sql("""
            UPDATE `tabDocField` 
            SET 
                fetch_from = 'crew_member.designation',
                fieldtype = 'Data',
                options = NULL
            WHERE name = %s
        """, (field_name,))
        
        # Clear the cache to reload the doctype
        frappe.clear_cache(doctype="Flight Crew")
        
        print("✅ Fixed Flight Crew role field to fetch designation from Employee")
    else:
        print("ℹ️  Flight Crew role field is already correctly configured")
