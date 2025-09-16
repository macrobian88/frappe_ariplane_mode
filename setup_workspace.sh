#!/bin/bash

# Airport Shop Management Workspace Setup Script
# This script sets up the complete workspace and demo data for the Airport Management System

echo "🚁 Airport Mode - Workspace Setup Script"
echo "==========================================="
echo ""

# Check if we're in a Frappe bench environment
if [ ! -f "sites/common_site_config.json" ]; then
    echo "❌ Error: This script must be run from the frappe-bench directory"
    echo "Please cd to your frappe-bench directory and run this script again"
    exit 1
fi

# Get site name from user if not provided
if [ -z "$1" ]; then
    echo "📝 Please enter your site name:"
    read -r SITE_NAME
else
    SITE_NAME=$1
fi

echo "🔧 Setting up Airport Shop Management for site: $SITE_NAME"
echo ""

# Step 1: Install the app if not already installed
echo "📦 Step 1: Installing Airplane Mode app..."
if bench --site "$SITE_NAME" list-apps | grep -q "airplane_mode"; then
    echo "✅ Airplane Mode app is already installed"
else
    echo "⬇️  Installing Airplane Mode app..."
    bench get-app https://github.com/macrobian88/frappe_ariplane_mode.git
    bench --site "$SITE_NAME" install-app airplane_mode
    echo "✅ App installed successfully"
fi

echo ""

# Step 2: Run database migrations
echo "🗄️  Step 2: Running database migrations..."
bench --site "$SITE_NAME" migrate
echo "✅ Migrations completed"

echo ""

# Step 3: Install demo data
echo "📊 Step 3: Installing comprehensive demo data..."
echo "This will create:"
echo "  - 10 Airlines with aircraft fleets"
echo "  - 10 Global airports (JFK, LHR, LAX, etc.)"
echo "  - 20 Airport shops across multiple terminals"
echo "  - 8 Active tenants with major brands"
echo "  - 12 Shop types and categories"
echo "  - Realistic contracts and financial data"
echo ""

read -p "Install demo data? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "⏳ Installing demo data..."
    bench --site "$SITE_NAME" execute airplane_mode.install_demo_data
    echo "✅ Demo data installed successfully"
else
    echo "⏭️  Skipping demo data installation"
fi

echo ""

# Step 4: Reload workspaces
echo "🏢 Step 4: Setting up Airport Shop Management workspace..."
bench --site "$SITE_NAME" reload-doctype "Workspace"
echo "✅ Workspace configuration loaded"

echo ""

# Step 5: Clear cache and restart
echo "🔄 Step 5: Clearing cache and restarting services..."
bench clear-cache
bench restart
echo "✅ System refreshed"

echo ""

# Step 6: Verify installation
echo "🔍 Step 6: Verifying installation..."

# Check if DocTypes exist
AIRPORT_SHOPS=$(bench --site "$SITE_NAME" execute "import frappe; print(frappe.db.count('Airport Shop'))")
TENANTS=$(bench --site "$SITE_NAME" execute "import frappe; print(frappe.db.count('Tenant'))")
AIRLINES=$(bench --site "$SITE_NAME" execute "import frappe; print(frappe.db.count('Airline'))")

echo "📊 Installation Summary:"
echo "  - Airport Shops: $AIRPORT_SHOPS"
echo "  - Tenants: $TENANTS"
echo "  - Airlines: $AIRLINES"

if [ "$AIRPORT_SHOPS" -gt 0 ] && [ "$TENANTS" -gt 0 ] && [ "$AIRLINES" -gt 0 ]; then
    echo "✅ Installation verified successfully!"
else
    echo "⚠️  Installation may be incomplete. Please check the logs."
fi

echo ""

# Step 7: Provide next steps
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "🌐 Next Steps:"
echo "1. Open your Frappe site: http://your-site-domain"
echo "2. Navigate to 'Airport Shop Management' workspace"
echo "3. Explore the dashboard cards and metrics"
echo "4. Test creating a Shop Lease Contract"
echo "5. Review the occupancy and revenue reports"
echo ""

echo "📱 Available Workspaces:"
echo "• Airplane Mode - Flight operations and aircraft management"
echo "• Airport Shop Management - Shop leasing and tenant management"
echo ""

echo "🛠️  Test the Installation:"
echo "1. Go to 'Airport Shop Management' workspace"
echo "2. Click 'Shop Lease Contracts' → 'New'"
echo "3. Select an Airport Shop (should work without errors)"
echo "4. Fill in tenant details and save"
echo ""

echo "📚 Documentation:"
echo "• Complete Setup Guide: COMPLETE_SETUP_GUIDE.md"
echo "• Workspace Setup: AIRPORT_SHOP_WORKSPACE_SETUP.md"
echo "• Troubleshooting: Check 'bench logs' for any issues"
echo ""

echo "🆘 Need Help?"
echo "• GitHub Issues: https://github.com/macrobian88/frappe_ariplane_mode/issues"
echo "• Email Support: nandhakishore2165@gmail.com"
echo ""

echo "✨ Thank you for using Airport Mode - Airport Management System!"
echo "Built with ❤️  using Frappe Framework"
