# Airport Shop Permission Fix - Installation Guide

## Quick Fix Application

### Step 1: Apply the Permission Fix

The main fix has been applied to the `airport_shop.py` file. To apply this fix to your running system:

1. **Download the updated file**:
   ```bash
   # Navigate to your frappe-bench directory
   cd frappe-bench/apps/airplane_mode
   
   # Backup the current file
   cp airplane_mode/airplane_mode/doctype/airport_shop/airport_shop.py airplane_mode/airplane_mode/doctype/airport_shop/airport_shop.py.backup
   
   # Download the fixed file
   wget -O airplane_mode/airplane_mode/doctype/airport_shop/airport_shop.py https://raw.githubusercontent.com/macrobian88/frappe_ariplane_mode/main/airplane_mode/airplane_mode/doctype/airport_shop/airport_shop.py
   ```

2. **Restart your Frappe application**:
   ```bash
   # From frappe-bench directory
   bench restart
   ```

### Step 2: Test the Fix

1. **Open your Frappe site** in a web browser
2. **Navigate to Shop Lease Contract**: Go to the doctype list or try to create a new Shop Lease Contract
3. **Test the Airport Shop link field**: The dropdown should now work without errors
4. **Verify search functionality**: Search for existing airport shops in the link field

## Alternative: Manual File Update

If you prefer to manually update the file, replace the content of `airplane_mode/airplane_mode/doctype/airport_shop/airport_shop.py` with:

```python
# Copyright (c) 2025, nandhakishore and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirportShop(Document):
	pass


def get_permission_query_conditions(user):
	"""
	Permission query conditions for Airport Shop doctype.
	This function is called when filtering Airport Shop records for links and searches.
	"""
	if not user:
		user = frappe.session.user
	
	# If user is Administrator or System Manager, show all records
	if user == "Administrator" or "System Manager" in frappe.get_roles(user):
		return ""
	
	# For other users, you can add custom conditions here
	# For now, return empty condition to show all records for non-admin users
	# You can modify this logic based on your specific requirements
	
	# Example: Only show shops from specific airport
	# return f"`tabAirport Shop`.airport = '{get_user_airport(user)}'"
	
	# For now, allow all users to see all airport shops
	return ""


def has_permission(doc, user=None, permission_type=None):
	"""
	Permission check for individual Airport Shop documents.
	"""
	if not user:
		user = frappe.session.user
	
	# Administrator and System Manager have full access
	if user == "Administrator" or "System Manager" in frappe.get_roles(user):
		return True
	
	# Add custom permission logic here if needed
	# For example, check if user belongs to specific airport, role, etc.
	
	# For now, allow all users to access airport shop records
	return True
```

## Step 3: Add Sample Data (Optional)

To test the system with sample data:

1. **Download the sample data script**:
   ```bash
   wget -O create_sample_data.py https://raw.githubusercontent.com/macrobian88/frappe_ariplane_mode/main/create_sample_data.py
   ```

2. **Run the sample data creation**:
   ```bash
   bench execute airplane_mode.create_sample_data --site your-site-name
   ```

   Or run it from the Frappe console:
   ```bash
   bench console your-site-name
   ```
   
   Then in the console:
   ```python
   exec(open('create_sample_data.py').read())
   ```

## Step 4: Verification Checklist

After applying the fix, verify the following:

- [ ] ✅ Shop Lease Contract form loads without errors
- [ ] ✅ Airport Shop link field shows available options
- [ ] ✅ Search functionality works in Airport Shop link fields
- [ ] ✅ No AttributeError about `get_permission_query_conditions`
- [ ] ✅ System allows creating new Shop Lease Contracts
- [ ] ✅ Existing Airport Shop records are accessible

## Troubleshooting

### If the error persists:

1. **Clear cache**:
   ```bash
   bench clear-cache
   bench restart
   ```

2. **Check for syntax errors**:
   ```bash
   bench console your-site-name
   ```
   ```python
   import airplane_mode.airplane_mode.doctype.airport_shop.airport_shop
   ```

3. **Verify file permissions**:
   ```bash
   ls -la airplane_mode/airplane_mode/doctype/airport_shop/airport_shop.py
   ```

### If you see import errors:

1. **Ensure frappe is imported**:
   Make sure the first line of imports includes `import frappe`

2. **Check module path**:
   Verify that the file is in the correct location within your app structure

## Advanced Customization

### Custom Permission Logic

To add custom permission filtering, modify the `get_permission_query_conditions` function:

```python
def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    # System users get full access
    if user == "Administrator" or "System Manager" in frappe.get_roles(user):
        return ""
    
    # Example: Filter by user's assigned airport
    user_airport = frappe.db.get_value("User", user, "custom_airport_assignment")
    if user_airport:
        return f"`tabAirport Shop`.airport = '{user_airport}'"
    
    # Example: Filter by active contracts only
    today = frappe.utils.today()
    return f"(`tabAirport Shop`.contract_end_date IS NULL OR `tabAirport Shop`.contract_end_date >= '{today}')"
```

### Role-Based Access

For more complex role-based access:

```python
def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    user_roles = frappe.get_roles(user)
    
    if "Administrator" in user_roles or "System Manager" in user_roles:
        return ""
    elif "Airport Manager" in user_roles:
        # Airport managers see only their managed airports
        managed_airports = frappe.db.get_list(
            "Airport Manager Assignment", 
            filters={"user": user}, 
            fields=["airport"]
        )
        if managed_airports:
            airport_list = "', '".join([a.airport for a in managed_airports])
            return f"`tabAirport Shop`.airport IN ('{airport_list}')"
    elif "Shop Manager" in user_roles:
        # Shop managers see only their assigned shops
        assigned_shops = frappe.db.get_list(
            "Shop Assignment", 
            filters={"user": user}, 
            fields=["shop"]
        )
        if assigned_shops:
            shop_list = "', '".join([s.shop for s in assigned_shops])
            return f"`tabAirport Shop`.name IN ('{shop_list}')"
    
    # Default: no access for undefined roles
    return "1=0"
```

## Support

If you encounter any issues:

1. Check the error logs: `bench logs`
2. Review the [complete documentation](AIRPORT_SHOP_PERMISSION_FIX.md)
3. Ensure all dependencies are properly installed
4. Verify that your Frappe/ERPNext versions are compatible

## Success Indicators

The fix is working correctly when:

- No AttributeError appears in logs or console
- Airport Shop records appear in link field dropdowns
- Shop Lease Contract creation works smoothly
- Search functionality responds normally
- System performance remains stable

---

**Last Updated**: September 16, 2025  
**Compatible With**: Frappe v15.x, ERPNext v15.x  
**Fix Version**: 1.0.0
