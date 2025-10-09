#!/bin/bash

# 🧹 Airport Shop Management DocType Consolidation Script
# This script consolidates all airport shop management DocTypes into the dedicated module

set -e  # Exit on any error

echo "🚀 Starting Airport Shop Management DocType Consolidation..."
echo "================================================="

# Confirm before proceeding
read -p "⚠️  This will remove duplicate DocTypes from airplane_mode module. Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Operation cancelled."
    exit 1
fi

# Define DocTypes to remove from airplane_mode module
DOCTYPES_TO_REMOVE=(
    "airport_shop"
    "contract_shop"
    "monthly_bill"
    "monthly_invoice"
    "rent_payment_contract"
    "rent_remainder_alerts"
    "shop_lease_contract"
    "shop_type"
    "tenant"
    "shop_contract"
)

# Move airport_shop_settings to airport_shop_management module
echo "📦 Moving Airport Shop Settings to Airport Shop Management module..."
if [ -d "airplane_mode/airplane_mode/doctype/airport_shop_settings" ]; then
    mv "airplane_mode/airplane_mode/doctype/airport_shop_settings" "airplane_mode/airport_shop_management/doctype/"
    echo "✅ Moved Airport Shop Settings"
else
    echo "ℹ️  Airport Shop Settings not found in airplane_mode module"
fi

# Remove duplicate DocTypes from airplane_mode module
echo "\n🗑️  Removing duplicate DocTypes from airplane_mode module..."
for doctype in "${DOCTYPES_TO_REMOVE[@]}"; do
    if [ -d "airplane_mode/airplane_mode/doctype/$doctype" ]; then
        rm -rf "airplane_mode/airplane_mode/doctype/$doctype"
        echo "✅ Removed duplicate: $doctype"
    else
        echo "ℹ️  DocType not found: $doctype"
    fi
done

# Clean up any __pycache__ directories
echo "\n🧹 Cleaning up cache directories..."
find airplane_mode/ -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find airplane_mode/ -name "*.pyc" -delete 2>/dev/null || true

echo "\n✅ File consolidation completed!"
echo "================================================="
echo "📋 Summary:"
echo "   - Moved Airport Shop Settings to Airport Shop Management module"
echo "   - Removed ${#DOCTYPES_TO_REMOVE[@]} duplicate DocTypes from Airplane Mode module"
echo "   - Cleaned up cache files"
echo ""
echo "🔄 Next Steps:"
echo "   1. Run: bench --site your-site-name migrate"
echo "   2. Run: bench --site your-site-name clear-cache"
echo "   3. Run: bench restart"
echo ""
echo "🎉 Airport Shop Management consolidation ready!"
