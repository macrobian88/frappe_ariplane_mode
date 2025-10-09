# 🔄 Import Reference Updates

## Overview
After consolidating DocTypes to the Airport Shop Management module, any import statements in your code that reference the old module paths need to be updated.

## 📝 Required Import Updates

### Before (OLD - airplane_mode module)
```python
# OLD imports from airplane_mode module
from airplane_mode.airplane_mode.doctype.airport_shop.airport_shop import AirportShop
from airplane_mode.airplane_mode.doctype.tenant.tenant import Tenant
from airplane_mode.airplane_mode.doctype.shop_type.shop_type import ShopType
from airplane_mode.airplane_mode.doctype.monthly_bill.monthly_bill import MonthlyBill
from airplane_mode.airplane_mode.doctype.rent_payment_contract.rent_payment_contract import RentPaymentContract
```

### After (NEW - airport_shop_management module)
```python
# NEW imports from airport_shop_management module
from airplane_mode.airport_shop_management.doctype.airport_shop.airport_shop import AirportShop
from airplane_mode.airport_shop_management.doctype.tenant.tenant import Tenant
from airplane_mode.airport_shop_management.doctype.shop_type.shop_type import ShopType
from airplane_mode.airport_shop_management.doctype.monthly_bill.monthly_bill import MonthlyBill
from airplane_mode.airport_shop_management.doctype.rent_payment_contract.rent_payment_contract import RentPaymentContract
```

## 🔍 Files to Check for Import Updates

1. **Python Files (.py)**
   - `airplane_mode/hooks.py`
   - `airplane_mode/notifications.py`
   - `airplane_mode/utils.py`
   - Any custom scripts or server scripts
   - API files in `airplane_mode/api/`

2. **JavaScript Files (.js)**
   - Client scripts in DocType folders
   - Custom scripts in `airplane_mode/public/js/`

3. **Configuration Files**
   - `airplane_mode/modules.txt`
   - Workspace JSON files
   - Dashboard configurations

## 🚀 Automated Search & Replace

### Find Import References
```bash
# Search for old import paths
grep -r "airplane_mode.airplane_mode.doctype.airport_shop" airplane_mode/
grep -r "airplane_mode.airplane_mode.doctype.tenant" airplane_mode/
grep -r "airplane_mode.airplane_mode.doctype.shop_type" airplane_mode/
grep -r "airplane_mode.airplane_mode.doctype.monthly_bill" airplane_mode/
grep -r "airplane_mode.airplane_mode.doctype.rent_payment_contract" airplane_mode/
```

### Replace Import Paths (use with caution)
```bash
# Example: Replace airport_shop imports
find airplane_mode/ -name "*.py" -exec sed -i 's/airplane_mode\.airplane_mode\.doctype\.airport_shop/airplane_mode.airport_shop_management.doctype.airport_shop/g' {} +
```

## ⚠️ Important Considerations

1. **Backup First**: Always backup your code before running bulk replacements
2. **Test Thoroughly**: Test all affected functionality after updates
3. **Check Dependencies**: Look for any external apps that might import these DocTypes
4. **Review Carefully**: Manually review each change to ensure correctness

## 🎯 Validation Steps

1. **Syntax Check**
   ```bash
   python -m py_compile airplane_mode/hooks.py
   ```

2. **Import Test**
   ```python
   # Test in bench console
   from airplane_mode.airport_shop_management.doctype.airport_shop.airport_shop import AirportShop
   ```

3. **Functionality Test**
   - Create a new Airport Shop
   - Test rent payment workflows
   - Verify all forms load correctly

## 📋 Checklist

- [ ] Updated import statements in Python files
- [ ] Updated import statements in JavaScript files  
- [ ] Updated configuration references
- [ ] Tested all affected functionality
- [ ] Verified no broken imports remain
- [ ] All tests pass
- [ ] Documentation updated

## 🆘 Troubleshooting

If you encounter import errors after the consolidation:

1. Check the exact error message
2. Verify the DocType exists in the new module location
3. Clear Python cache: `find . -name "*.pyc" -delete`
4. Restart bench: `bench restart`
5. Clear browser cache

---
*This consolidation improves code organization and eliminates duplicate DocTypes for better maintainability.*
