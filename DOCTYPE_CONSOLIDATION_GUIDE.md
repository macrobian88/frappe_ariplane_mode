# 📋 Airport Shop Management DocType Consolidation Guide

## 🎯 Objective
Consolidate all airport shop management related DocTypes into the dedicated `Airport Shop Management` module and remove duplicates from the main `Airplane Mode` module.

## 📊 Current State Analysis

### ✅ DocTypes to Keep in Airport Shop Management Module
- `airport_shop` ✅
- `contract_shop` ✅
- `monthly_bill` ✅
- `monthly_invoice` ✅
- `rent_payment_contract` ✅
- `rent_remainder_alerts` ✅
- `shop_lease_contract` ✅
- `shop_type` ✅
- `tenant` ✅

### 🔄 DocTypes to Move to Airport Shop Management
- `airport_shop_settings` (currently in airplane_mode module)

### ❌ DocTypes to Remove from Airplane Mode Module
- `airport_shop` (duplicate)
- `contract_shop` (duplicate)
- `monthly_bill` (duplicate)
- `monthly_invoice` (duplicate)
- `rent_payment_contract` (duplicate)
- `rent_remainder_alerts` (duplicate)
- `shop_lease_contract` (duplicate)
- `shop_type` (duplicate)
- `tenant` (duplicate)
- `shop_contract` (redundant with shop_lease_contract)

## 🚀 Implementation Steps

### Step 1: Database Cleanup Patch
Run the database cleanup patch to remove duplicate DocType entries:

```bash
bench --site your-site-name migrate
```

### Step 2: Remove Duplicate DocType Folders
Execute the automated cleanup script:

```bash
./consolidate_airport_shop_doctypes.sh
```

### Step 3: Update Import References
Update any import statements that reference the old module paths.

### Step 4: Clear Cache and Restart
```bash
bench --site your-site-name clear-cache
bench restart
```

## 📁 Final Module Structure

### Airport Shop Management Module
```
airplane_mode/airport_shop_management/doctype/
├── airport_shop/
├── airport_shop_settings/           # Moved from airplane_mode
├── contract_shop/
├── monthly_bill/
├── monthly_invoice/
├── rent_payment_contract/
├── rent_remainder_alerts/
├── shop_lease_contract/
├── shop_type/
└── tenant/
```

### Airplane Mode Module (Clean)
```
airplane_mode/airplane_mode/doctype/
├── airline/
├── airplane/
├── airplane_flight/
├── airplane_ticket/
├── airplane_ticket_add_on_item/
├── airplane_ticket_add_on_type/
├── airport/
├── flight_crew/
└── flight_passenger/
```

## ⚠️ Important Notes

1. **Backup First**: Always backup your site before running migration
2. **Test Environment**: Run this in a test environment first
3. **Dependencies**: Check for any custom code that imports from old paths
4. **Links**: Verify all document links continue to work after consolidation

## 🎉 Expected Benefits

- ✅ Clean separation of concerns
- ✅ No more duplicate DocTypes
- ✅ Faster migrations
- ✅ Better maintainability
- ✅ Clearer module organization
