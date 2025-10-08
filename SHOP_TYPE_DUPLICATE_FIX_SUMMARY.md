# Shop Type Duplicate Fix Summary

## Issue
Migration was failing with the error:
```
pymysql.err.IntegrityError: (1062, "Duplicate entry 'Duty Free' for key 'type_name'")
frappe.exceptions.ValidationError: type_name field cannot be set as unique in tabShop Type, as there are non-unique existing values
```

## Root Cause
The `Shop Type` DocType had a `type_name` field marked with `"unique": 1`, but duplicate entries existed in the database (specifically "Duty Free" appeared multiple times).

## Solution Implemented

### 1. Database Patch
- **File**: `airplane_mode/patches/remove_duplicate_shop_types.py`
- **Purpose**: Removes duplicate Shop Type entries before migration
- **Logic**: 
  - Identifies all duplicate `type_name` entries
  - Keeps the first (oldest) record
  - Deletes all duplicate records
  - Includes comprehensive logging and error handling

### 2. DocType Schema Update
- **File**: `airplane_mode/airport_shop_management/doctype/shop_type/shop_type.json`
- **Change**: Removed `"unique": 1` from the `type_name` field
- **Reason**: Prevents database-level unique constraint conflicts during migration

### 3. Application-Level Validation
- **File**: `airplane_mode/airport_shop_management/doctype/shop_type/shop_type.py`
- **Existing**: Already has `validate_type_name()` method that prevents duplicates
- **Advantage**: Provides user-friendly error messages and allows more flexible validation

### 4. Patch Registration
- **File**: `airplane_mode/patches.txt`
- **Added**: `airplane_mode.patches.remove_duplicate_shop_types`
- **Order**: Runs before schema updates to ensure clean data

## Migration Order
1. **Patch runs first**: Removes duplicate entries
2. **Schema update runs**: Updates DocType without unique constraint conflict
3. **Application validation**: Prevents future duplicates through Python validation

## Benefits
- ✅ Fixes immediate migration error
- ✅ Preserves data integrity through application validation
- ✅ Provides better error messages to users
- ✅ Allows for more complex validation rules in the future
- ✅ Comprehensive logging for troubleshooting

## Commands to Apply Fix
```bash
# Pull latest changes
git pull origin main

# Run migration
bench --site your-site-name migrate

# Clear cache
bench --site your-site-name clear-cache

# Restart
bench restart
```

## Verification
After migration, verify:
1. No duplicate Shop Type entries exist
2. Shop Type form validates duplicates properly
3. All existing Shop Types are still accessible
4. New Shop Types can be created without issues

## Rollback Plan
If issues occur:
1. The patch is idempotent and safe to re-run
2. The old unique constraint can be re-added after data cleanup
3. All changes are logged for debugging
