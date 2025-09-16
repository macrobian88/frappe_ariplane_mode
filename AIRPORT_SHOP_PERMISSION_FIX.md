# Airport Shop Permission Query Fix

## Issue Description

The following error was occurring when trying to create a new Shop Lease Contract or when searching for Airport Shop records in link fields:

```
AttributeError: module 'airplane_mode.airplane_mode.doctype.airport_shop.airport_shop' has no attribute 'get_permission_query_conditions'
```

### Error Details
- **Route**: `Form/Shop Lease Contract/new-shop-lease-contract-ccrlppxsjd`
- **Traceback**: The error occurred in the search link functionality when trying to search for Airport Shop records
- **Root Cause**: Missing `get_permission_query_conditions` function in the Airport Shop doctype module

## Solution

Added the missing `get_permission_query_conditions` function to the `airport_shop.py` file. This function is required by Frappe when a doctype has permission restrictions and is being used in link fields or search operations.

### Changes Made

1. **Added `get_permission_query_conditions(user)` function**:
   - Handles permission filtering when Airport Shop records are searched in link fields
   - Allows System Managers and Administrators full access
   - Can be customized for user-specific filtering rules

2. **Added `has_permission(doc, user, permission_type)` function**:
   - Provides document-level permission checking
   - Complements the query-level permissions
   - Follows the same access pattern as the query function

### Function Implementation

```python
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
```

## Why This Function is Required

When Frappe encounters a doctype with permission rules defined (as seen in the Airport Shop's JSON configuration), it automatically looks for a `get_permission_query_conditions` function to apply proper filtering during search operations. If this function is missing, the AttributeError occurs.

## Testing the Fix

After applying this fix:

1. **Shop Lease Contract Form**: Should now load without errors
2. **Airport Shop Link Field**: Should show available airport shops in the dropdown/search
3. **Search Functionality**: Should work properly for Airport Shop records

## Customization Options

The current implementation allows all users to see all Airport Shop records. You can customize the permission logic by modifying the `get_permission_query_conditions` function to:

- Filter shops by specific airport based on user location
- Restrict access based on user roles
- Apply date-based filtering (e.g., only active contracts)
- Add territory or branch-based restrictions

### Example Customizations

```python
# Filter by user's assigned airport
def get_permission_query_conditions(user):
    user_airport = frappe.db.get_value("User", user, "custom_airport")
    if user_airport:
        return f"`tabAirport Shop`.airport = '{user_airport}'"
    return ""

# Filter by role-based permissions
def get_permission_query_conditions(user):
    if "Airport Manager" in frappe.get_roles(user):
        # Airport managers see only their airport's shops
        managed_airport = frappe.db.get_value("User", user, "custom_managed_airport")
        if managed_airport:
            return f"`tabAirport Shop`.airport = '{managed_airport}'"
    return ""
```

## Files Modified

- `airplane_mode/airplane_mode/doctype/airport_shop/airport_shop.py`

## Compatibility

This fix is compatible with:
- Frappe Framework v15.x
- ERPNext v15.x
- All existing Airport Shop records and configurations

## Related Documentation

- [Frappe Permission System](https://frappeframework.com/docs/user/en/basics/users-and-permissions)
- [Custom Permissions in Frappe](https://frappeframework.com/docs/user/en/guides/app-development/custom-permissions)
