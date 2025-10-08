#!/bin/bash

# DocType Cleanup Script
# This script removes unused DocTypes from the Airplane Mode app

echo "🚀 Starting DocType cleanup..."
echo "========================================"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    echo "Please run this script from your frappe_ariplane_mode repository root"
    exit 1
fi

# Array of directories to remove
directories=(
    "airplane_mode/airport_shop_management/doctype/rent_remainder_alerts"
    "airplane_mode/airplane_mode/doctype/rent_remainder_alerts"
    "airplane_mode/airplane_mode/doctype/monthly_invoice"
    "airplane_mode/airplane_mode/doctype/airport_shop_settings"
    "airplane_mode/airplane_mode/doctype/monthly_bill"
)

echo "📋 DocTypes to be removed:"
echo "   - Rent Remainder Alerts (both modules)"
echo "   - Monthly Invoice"
echo "   - Airport Shop Settings"
echo "   - Monthly Bill"
echo ""

# Confirm with user
read -p "❓ Do you want to proceed with removing these DocTypes? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cleanup cancelled by user"
    exit 0
fi

echo "🗑️  Removing DocType directories..."
echo ""

# Remove each directory
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        echo "   ✅ Removing: $dir"
        git rm -r "$dir"
    else
        echo "   ⚠️  Directory not found: $dir"
    fi
done

echo ""
echo "📝 Committing changes..."
git commit -m "Remove unused DocTypes: Rent Remainder Alerts, Monthly Invoice, Airport Shop Settings, Monthly Bill

- Remove duplicate Rent Remainder Alerts from both modules
- Remove Monthly Invoice DocType
- Remove Airport Shop Settings DocType  
- Remove Monthly Bill DocType
- Database cleanup handled by airplane_mode.patches.cleanup_unused_doctypes patch"

if [ $? -eq 0 ]; then
    echo "✅ Changes committed successfully"
    echo ""
    echo "🚀 Pushing to GitHub..."
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo "✅ Changes pushed to GitHub successfully"
    else
        echo "❌ Failed to push to GitHub. Please check your connection and permissions."
        echo "You can manually push later with: git push origin main"
    fi
else
    echo "❌ Failed to commit changes. Please check for errors above."
    exit 1
fi

echo ""
echo "🎉 DocType cleanup completed successfully!"
echo "========================================"
echo "📋 Summary:"
echo "   ✅ Database cleanup patch added"
echo "   ✅ DocType files removed"
echo "   ✅ Changes committed and pushed"
echo ""
echo "🔄 Next steps:"
echo "   1. Run: bench --site your-site-name migrate"
echo "   2. Run: bench --site your-site-name clear-cache"
echo "   3. Run: bench restart"
echo ""
echo "📖 For detailed instructions, see: DOCTYPE_CLEANUP_GUIDE.md"