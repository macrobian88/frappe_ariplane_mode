# Airport Shop Management Workspace

## Overview

This document describes the Airport Shop Management workspace that has been added to the Airplane Mode Frappe app. This workspace provides a comprehensive interface for managing airport shops, tenants, contracts, and related operations.

## Workspace Features

### 📊 Dashboard Cards

The workspace includes several number cards that provide real-time statistics:

1. **Occupied Shops** (Blue) - Count of shops currently occupied
2. **Vacant Shops** (Red) - Count of available shop spaces
3. **Total Monthly Revenue** (Green) - Sum of rent amounts from occupied shops
4. **Active Tenants** (Purple) - Total number of tenants in the system

### 🚀 Quick Shortcuts

The workspace provides quick access to key functions:

- **Airport Shops** (Blue) - Manage all airport shop records
- **Shop Types** (Green) - Configure different types of shops
- **Tenants** (Orange) - Manage tenant information
- **Shop Lease Contracts** (Purple) - Handle lease agreements
- **Occupancy Report** (Grey) - View detailed occupancy analytics
- **Revenue Summary** (Red) - Monitor financial performance
- **Contract Expiry** (Yellow) - Track contracts expiring in next 90 days

### 📋 Quick Lists

Pre-filtered lists for common operations:

- **Available Shops** - Shows all vacant shops ready for lease
- **Expiring Contracts** - Contracts ending within 90 days
- **Active Tenants** - Current tenants with valid contracts

### 🔗 Navigation Links

Organized into logical sections:

**Shop Operations:**
- Airport Shop (Primary DocType)
- Shop Type (Configuration)
- Tenant (Tenant Management)

**Contracts & Leasing:**
- Shop Lease Contract (Primary Contract DocType)
- Shop Contract (Alternative Contract Type)
- Monthly Bill (Billing Management)

**Reports & Analytics:**
- Shop Occupancy Report (Query Report)
- Revenue Summary (Financial Overview)

## Installation & Setup

### Automatic Installation

The workspace is automatically available after installing the Airplane Mode app. No additional setup required.

### Manual Bench Commands

If you need to manually install or refresh the workspace:

```bash
# Navigate to your frappe-bench directory
cd frappe-bench

# Install the workspace
bench --site your-site-name install-app airplane_mode

# Or reload the workspace
bench --site your-site-name reload-doctype "Workspace"

# Clear cache to refresh
bench --site your-site-name clear-cache
```

### Permissions

The workspace is public by default and accessible to all users with appropriate DocType permissions. To restrict access:

1. Navigate to **Workspace** DocType
2. Find "Airport Shop Management" workspace
3. Set `public = 0`
4. Add specific roles in the `roles` field

## Usage Guide

### Getting Started

1. **Access the Workspace**: Click on "Airport Shop Management" in the sidebar
2. **Review Dashboard**: Check the number cards for current status
3. **Quick Actions**: Use shortcuts for common tasks
4. **Detailed Work**: Use navigation links for comprehensive management

### Common Workflows

**Adding a New Shop:**
1. Click "Airport Shops" shortcut
2. Click "New"
3. Fill in shop details (name, number, airport, type, area, rent)
4. Save the shop record

**Creating a Lease Contract:**
1. Click "Shop Lease Contracts" shortcut
2. Click "New"
3. Select the airport shop (now working with the fixed permission error)
4. Add tenant and contract details
5. Save and submit the contract

**Monitoring Occupancy:**
1. Use "Available Shops" quick list to see vacant spaces
2. Check "Occupied Shops" number card for utilization rate
3. Review "Contract Expiry" for upcoming renewals

### Reports & Analytics

**Revenue Tracking:**
- Monitor "Total Monthly Revenue" card
- Access detailed revenue reports via "Revenue Summary"
- Track billing through "Monthly Bill" documents

**Occupancy Analysis:**
- Use "Occupancy Report" for detailed analytics
- Compare "Occupied Shops" vs "Vacant Shops" cards
- Review "Available Shops" list for leasing opportunities

**Contract Management:**
- Monitor "Expiring Contracts" quick list
- Track "Active Tenants" count
- Use "Contract Expiry" filter for renewal planning

## Integration with Demo Data

The workspace is designed to work seamlessly with the demo data that was created:

- **20 Airport Shops** across multiple airports (JFK, LHR, LAX, DXB, SIN, FRA)
- **10+ Shop Types** (Restaurant, Coffee Shop, Duty Free, Electronics, etc.)
- **5 Tenants** with active contracts (Starbucks, McDonald's, Apple, etc.)
- **5 Customers** linked to tenants
- **Realistic Data** with varying rent amounts, contract dates, and occupancy status

## Customization

### Adding Custom Cards

To add new number cards:

1. Edit the workspace JSON file
2. Add new entries to the `number_cards` array
3. Configure filters, colors, and functions
4. Reload the workspace

### Custom Shortcuts

To modify shortcuts:

1. Edit the `shortcuts` array in the JSON
2. Change colors, labels, or target DocTypes
3. Add custom filters using `stats_filter`

### Additional Quick Lists

To add new quick lists:

1. Edit the `quick_lists` array
2. Define custom filters for specific use cases
3. Set descriptive labels

## Troubleshooting

### Workspace Not Appearing

1. Check if the app is properly installed: `bench list-apps`
2. Reload DocTypes: `bench --site your-site reload-doctype "Workspace"`
3. Clear cache: `bench clear-cache`
4. Restart bench: `bench restart`

### Permission Errors

1. Ensure users have access to the required DocTypes
2. Check Role Permissions for Airport Shop, Tenant, etc.
3. Verify the Airport Shop permission fix is applied

### Data Not Loading

1. Confirm demo data was created successfully
2. Check DocType permissions
3. Verify database connectivity
4. Review error logs: `bench logs`

## Technical Details

### File Structure

```
airplane_mode/
├── airplane_mode/
│   └── workspace/
│       └── airport_shop_management/
│           ├── __init__.py
│           └── airport_shop_management.json
```

### JSON Configuration

The workspace is defined in `airport_shop_management.json` with:

- **Content**: Layout and visual components
- **Shortcuts**: Quick access buttons
- **Links**: Navigation menu items
- **Number Cards**: Dashboard statistics
- **Quick Lists**: Pre-filtered views

### Dependencies

- Frappe Framework v15.x
- ERPNext v15.x (for Customer DocType)
- Airplane Mode app with all DocTypes

## Support

For issues or questions:

1. Check the error logs: `bench logs`
2. Review the troubleshooting section above
3. Verify all dependencies are installed
4. Ensure proper permissions are set

---

**Created**: September 16, 2025  
**Version**: 1.0.0  
**Compatible with**: Frappe v15.x, ERPNext v15.x