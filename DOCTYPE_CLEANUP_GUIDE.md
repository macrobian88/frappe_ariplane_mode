# DocType Cleanup Script

## Overview
This script removes unused DocTypes from the Airplane Mode app as requested:
- Rent_Remainder_Alerts  
- Monthly Invoice
- Airport Shop Settings
- Monthly Bill

## Files to be Removed

### 1. Rent Remainder Alerts (Airport Shop Management Module)
```
airplane_mode/airport_shop_management/doctype/rent_remainder_alerts/
├── __init__.py
├── rent_remainder_alerts.js
├── rent_remainder_alerts.json
├── rent_remainder_alerts.py
└── test_rent_remainder_alerts.py
```

### 2. Rent Remainder Alerts (Airplane Mode Module) 
```
airplane_mode/airplane_mode/doctype/rent_remainder_alerts/
├── __init__.py
├── rent_remainder_alerts.js
├── rent_remainder_alerts.json
├── rent_remainder_alerts.py
└── test_rent_remainder_alerts.py
```

### 3. Monthly Invoice
```
airplane_mode/airplane_mode/doctype/monthly_invoice/
├── __init__.py
├── monthly_invoice.js
├── monthly_invoice.json
├── monthly_invoice.py
└── test_monthly_invoice.py
```

### 4. Airport Shop Settings
```
airplane_mode/airplane_mode/doctype/airport_shop_settings/
├── __init__.py
├── airport_shop_settings.js
├── airport_shop_settings.json
├── airport_shop_settings.py
└── test_airport_shop_settings.py
```

### 5. Monthly Bill
```
airplane_mode/airplane_mode/doctype/monthly_bill/
├── __init__.py
├── monthly_bill.js
├── monthly_bill.json
├── monthly_bill.py
└── test_monthly_bill.py
```

## Removal Methods

### Method 1: Manual Git Commands (Recommended)
```bash
# Navigate to your repository
cd /path/to/frappe_ariplane_mode

# Remove the directories
git rm -r airplane_mode/airport_shop_management/doctype/rent_remainder_alerts
git rm -r airplane_mode/airplane_mode/doctype/rent_remainder_alerts  
git rm -r airplane_mode/airplane_mode/doctype/monthly_invoice
git rm -r airplane_mode/airplane_mode/doctype/airport_shop_settings
git rm -r airplane_mode/airplane_mode/doctype/monthly_bill

# Commit the changes
git commit -m "Remove unused DocTypes: Rent Remainder Alerts, Monthly Invoice, Airport Shop Settings, Monthly Bill"

# Push to GitHub
git push origin main
```

### Method 2: Using Shell Script
Create a file called `cleanup_doctypes.sh`:

```bash
#!/bin/bash

echo "Starting DocType cleanup..."

# Array of directories to remove
directories=(
    "airplane_mode/airport_shop_management/doctype/rent_remainder_alerts"
    "airplane_mode/airplane_mode/doctype/rent_remainder_alerts"
    "airplane_mode/airplane_mode/doctype/monthly_invoice"
    "airplane_mode/airplane_mode/doctype/airport_shop_settings"
    "airplane_mode/airplane_mode/doctype/monthly_bill"
)

# Remove each directory
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        echo "Removing directory: $dir"
        git rm -r "$dir"
    else
        echo "Directory not found: $dir"
    fi
done

echo "DocType cleanup completed"
echo "Don't forget to commit and push the changes:"
echo "git commit -m 'Remove unused DocTypes'"
echo "git push origin main"
```

### Method 3: Python Script for GitHub API
Create a file called `cleanup_doctypes.py`:

```python
import os
import subprocess

def remove_doctype_directories():
    directories = [
        "airplane_mode/airport_shop_management/doctype/rent_remainder_alerts",
        "airplane_mode/airplane_mode/doctype/rent_remainder_alerts",
        "airplane_mode/airplane_mode/doctype/monthly_invoice", 
        "airplane_mode/airplane_mode/doctype/airport_shop_settings",
        "airplane_mode/airplane_mode/doctype/monthly_bill"
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"Removing directory: {directory}")
            subprocess.run(["git", "rm", "-r", directory])
        else:
            print(f"Directory not found: {directory}")
    
    print("All specified directories removed")
    print("Run: git commit -m 'Remove unused DocTypes' && git push origin main")

if __name__ == "__main__":
    remove_doctype_directories()
```

## Database Cleanup

The database cleanup is handled automatically by the patch:
`airplane_mode.patches.cleanup_unused_doctypes`

This patch will:
- Remove all data from the DocType tables
- Remove DocType definitions
- Clean up related records (Custom Fields, Property Setters, etc.)
- Clear cache

## Migration Steps

1. **Pull latest changes** (includes the database cleanup patch)
2. **Remove the DocType files** using one of the methods above
3. **Run migration** to execute the cleanup patch
4. **Clear cache** and restart

```bash
# Step 1: Pull latest changes
git pull origin main

# Step 2: Remove files (choose one method above)
git rm -r airplane_mode/airport_shop_management/doctype/rent_remainder_alerts
git rm -r airplane_mode/airplane_mode/doctype/rent_remainder_alerts
git rm -r airplane_mode/airplane_mode/doctype/monthly_invoice
git rm -r airplane_mode/airplane_mode/doctype/airport_shop_settings
git rm -r airplane_mode/airplane_mode/doctype/monthly_bill

# Step 3: Commit and push
git commit -m "Remove unused DocTypes: Rent Remainder Alerts, Monthly Invoice, Airport Shop Settings, Monthly Bill"
git push origin main

# Step 4: Run migration
bench --site your-site-name migrate

# Step 5: Clear cache and restart
bench --site your-site-name clear-cache
bench restart
```

## Verification

After cleanup, verify:
1. ✅ Removed DocTypes no longer appear in DocType list
2. ✅ No database tables exist for removed DocTypes  
3. ✅ No errors in error log
4. ✅ Migration completes successfully
5. ✅ Remaining DocTypes (Airport Shop, Shop Type, Tenant, etc.) work correctly

## Rollback Plan

If you need to restore any DocType:
1. Revert the commit that removed the files
2. Run migration to restore database structure
3. Restore any backed-up data

## Notes

- The cleanup patch is idempotent and safe to run multiple times
- Database cleanup happens automatically during migration
- File system cleanup must be done manually or via script
- Always backup your database before major changes like this
