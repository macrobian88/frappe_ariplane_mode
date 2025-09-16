# 🚁 Airplane Mode - Airport Management System

> ✨ **Latest Update**: Added comprehensive Airport Shop Management workspace with demo data and enhanced permissions system!

A comprehensive Frappe application for managing airport operations including flight management, passenger services, crew assignment, and advanced shop management with automated rent collection and analytics.

## 🌟 New Features & Updates

### 🏪 Airport Shop Management Workspace
- **Real-time Dashboard**: Live occupancy, revenue, and tenant metrics
- **Quick Shortcuts**: Direct access to shops, tenants, contracts, reports
- **Smart Quick Lists**: Pre-filtered views for available shops, expiring contracts
- **Advanced Analytics**: Revenue summaries and occupancy reports

### 📊 Comprehensive Demo Data
- **20 Airport Shops** across multiple global airports (JFK, LHR, LAX, DXB, SIN, FRA)
- **10 Airlines** with realistic aircraft fleets and specifications
- **12 Shop Types** from restaurants to duty-free stores
- **8 Active Tenants** with major brands like Starbucks, McDonald's, Apple Store
- **Realistic Contracts** with varied lease terms and financial data

### ⚡ Critical Fixes
- ✅ **Airport Shop Search Error**: Fixed `AttributeError` in permission queries
- ✅ **Link Field Issues**: Resolved search functionality in contracts
- ✅ **Enhanced Permissions**: Robust role-based access control
- ✅ **Installation Issues**: ERPNext dependency now optional

## 🚀 Quick Installation

### Standard Installation
```bash
# Clone the repository
git clone https://github.com/macrobian88/frappe_ariplane_mode.git
cd frappe_ariplane_mode

# Install the app
bench get-app . --branch main
bench --site your-site-name install-app airplane_mode

# Install demo data (recommended)
bench --site your-site-name execute airplane_mode.install_demo_data

# Clear cache and restart
bench clear-cache
bench restart
```

### Alternative Installation
```bash
# Direct installation from GitHub
bench get-app https://github.com/macrobian88/frappe_ariplane_mode.git
bench --site your-site-name install-app airplane_mode
bench --site your-site-name migrate
```

## 📱 Workspaces

### 1. Airplane Mode Workspace
- ✈️ Airlines management and aircraft fleet
- 🎫 Flight operations and passenger services
- 👥 Crew assignment and tracking
- 📊 Flight analytics and reporting

### 2. 🏪 Airport Shop Management Workspace (NEW!)
#### Dashboard Cards
- **Occupied Shops** (Blue) - Real-time occupied shop count
- **Vacant Shops** (Red) - Available shop spaces
- **Total Monthly Revenue** (Green) - Sum of all rent amounts
- **Active Tenants** (Purple) - Current tenant count

#### Quick Shortcuts
- **Airport Shops** - Manage shop inventory and details
- **Shop Types** - Configure shop categories and settings
- **Tenants** - Handle tenant registration and profiles
- **Shop Lease Contracts** - Create and manage lease agreements
- **Occupancy Report** - Detailed analytics and utilization
- **Revenue Summary** - Financial performance tracking
- **Contract Expiry** - Track contracts ending soon

#### Smart Quick Lists
- **Available Shops** - Vacant shops ready for lease
- **Expiring Contracts** - Contracts ending within 90 days
- **Active Tenants** - Current tenants with valid contracts

## 🗄️ Demo Data Package

The system now includes comprehensive demo data for immediate testing:

### Airlines & Aircraft
- **10 Airlines**: American Airlines, Delta, United, Emirates, British Airways, Lufthansa, Air India, Sky Airways, Global Wings, Ocean Air
- **15+ Aircraft**: Boeing 737-800, 777-300ER, 787-9, Airbus A320, A350-900, A380-800, and more
- **Realistic Specifications**: Proper capacity, audit status, and airline assignments

### Airports & Infrastructure
- **10 Global Airports**: JFK (New York), LHR (London), LAX (Los Angeles), DXB (Dubai), SIN (Singapore), FRA (Frankfurt), and more
- **Airport Codes**: Proper IATA codes and city/country information
- **Geographic Coverage**: US, UK, UAE, Singapore, Germany representation

### Shop Management
- **20 Airport Shops**: Realistic shops across multiple terminals
  - JFK: Starbucks, McDonald's, Apple Store, Hudson News, Duty Free
  - LHR: Costa Coffee, Boots Pharmacy, Harrods, Pret A Manger
  - LAX: In-N-Out Burger, Blue Bottle Coffee, Best Buy Express
  - DXB/SIN/FRA: Premium duty-free and local specialties

- **12 Shop Types**: Restaurant, Coffee Shop, Duty Free, Electronics, Bookstore, Pharmacy, Fashion, Convenience Store, Car Rental, and more

- **8 Active Tenants**: Starbucks Corporation, McDonald's USA LLC, Apple Inc., Hudson Group, Duty Free Americas, and others with realistic contract terms

### Financial Data
- **Varied Rent Amounts**: $8,000 - $60,000 monthly rent based on location and type
- **Realistic Contracts**: Mix of contract terms from 6 months to 3 years
- **Occupancy Mix**: Both occupied and vacant shops for testing
- **Revenue Analytics**: Immediate data for financial reporting

## 🏗️ System Architecture

### Core DocTypes

#### Flight Operations
- **Airline** - Airline company information and contact details
- **Airport** - Airport details, codes, and location information
- **Airplane** - Aircraft registration, models, and specifications
- **Airplane Flight** - Flight scheduling, crew, and route management

#### Shop Management
- **Airport Shop** - Shop inventory, details, and rental information
- **Shop Type** - Shop categorization and configuration
- **Tenant** - Tenant profiles, contacts, and contract information
- **Shop Lease Contract** - Lease agreements and rental contracts
- **Monthly Bill** - Automated billing and payment tracking

### Enhanced Features
- **Permission System**: Role-based access with proper query conditions
- **Search Functionality**: Advanced link field search with resolved permissions
- **Data Validation**: Comprehensive input validation and error handling
- **Workflow Support**: Approval processes for contracts and agreements
- **Report Generation**: Custom query reports and real-time analytics

## 🛠️ Technical Specifications

### Requirements
- **Frappe Framework**: v15.x or higher
- **ERPNext**: v15.x (optional, for enhanced financial features)
- **Python**: 3.8+
- **Database**: MariaDB 10.3+ or PostgreSQL 12+
- **Node.js**: 16+ (for frontend development)

### Compatibility
- ✅ Frappe Cloud hosting
- ✅ Self-hosted Frappe installations
- ✅ ERPNext integration (optional)
- ✅ Custom domain deployment
- ✅ Multi-tenant environments

## 📚 Documentation

### Installation & Setup
- [🚀 **Complete Setup Guide**](COMPLETE_SETUP_GUIDE.md) - Comprehensive installation and configuration
- [🏪 **Workspace Setup**](AIRPORT_SHOP_WORKSPACE_SETUP.md) - Workspace configuration details
- [💾 **Demo Data Script**](install_demo_data.py) - Automated demo data installation
- [🔧 **Installation Troubleshooting**](INSTALLATION_TROUBLESHOOTING.md) - Common issues and solutions

### Quick References
- API documentation for shop portal integration
- Permission configuration guides
- Custom report creation tutorials
- Background job setup instructions

## 🌟 Key Features

### ✈️ Flight Operations
- **Flight Management**: Complete scheduling and route management
- **Crew Assignment**: Automated crew assignment and tracking
- **Gate Management**: Real-time gate allocation and management
- **Passenger Services**: Ticket management and passenger tracking

### 🏪 Shop Management
- **Shop Operations**: Comprehensive inventory and management system
- **Tenant Management**: Complete tenant lifecycle management
- **Lease Contracts**: Automated contract creation and tracking
- **Revenue Tracking**: Real-time rent collection and financial reporting
- **Occupancy Analytics**: Live utilization metrics and forecasting

### 📊 Analytics & Reporting
- **Real-time Dashboards**: Live metrics and KPIs
- **Revenue Analytics**: Comprehensive financial trends and forecasting
- **Occupancy Reports**: Shop utilization by type, location, and time
- **Contract Management**: Renewal tracking and expiry notifications
- **Performance Metrics**: Operational efficiency measurements

### 🌐 Public Portal
- **Shop Availability**: Public portal for available shop spaces
- **Online Applications**: Streamlined application process for lessees
- **Automated Notifications**: Email confirmations and follow-ups
- **Lead Management**: Automated lead capture and conversion tracking

## 🧪 Testing Your Installation

After installation, verify the system works correctly:

### 1. Access Workspaces
- **Airport Operations**: Navigate to "Airplane Mode" workspace
- **Shop Management**: Navigate to "Airport Shop Management" workspace
- **Verify Cards**: Check that dashboard cards show demo data

### 2. Test Core Functionality
```bash
# Create a new shop lease contract
1. Go to "Shop Lease Contracts" in workspace
2. Click "New"
3. Select an Airport Shop (should work without errors)
4. Fill tenant and contract details
5. Save successfully
```

### 3. Verify Demo Data
```bash
# Check demo data installation
bench --site your-site-name console
```

In console:
```python
import frappe
print(f"Airport Shops: {frappe.db.count('Airport Shop')}")
print(f"Tenants: {frappe.db.count('Tenant')}")
print(f"Airlines: {frappe.db.count('Airline')}")
print(f"Airports: {frappe.db.count('Airport')}")
```

Expected output: 20+ shops, 8+ tenants, 10+ airlines, 10+ airports

## 🐛 Troubleshooting

### Common Issues

#### Installation Problems
```bash
# Clear cache and restart
bench clear-cache
bench restart

# Reload critical DocTypes
bench --site your-site-name reload-doctype "Airport Shop"
bench --site your-site-name reload-doctype "Workspace"
```

#### Permission Errors
- Ensure user has System Manager role or appropriate permissions
- Check that Airport Shop permission fix is applied
- Verify DocType permissions are properly configured

#### Demo Data Issues
```bash
# Reinstall demo data
bench --site your-site-name execute airplane_mode.install_demo_data

# Clean up and reinstall (if needed)
bench --site your-site-name execute airplane_mode.install_demo_data --args "--cleanup"
```

### Getting Help
1. **Check Logs**: `bench logs` for detailed error information
2. **Documentation**: Review the comprehensive guides in this repository
3. **GitHub Issues**: Create an issue for bugs or feature requests
4. **Community**: Join Frappe community for general questions

## 🔧 Advanced Configuration

### Custom Workspace Modifications
1. Navigate to **Workspace** DocType
2. Find "Airport Shop Management" record
3. Modify dashboard cards, shortcuts, or layout
4. Save and refresh to apply changes

### Performance Optimization
```sql
-- Add database indexes for better performance
CREATE INDEX idx_airport_shop_occupied ON `tabAirport Shop`(is_occupied);
CREATE INDEX idx_airport_shop_airport ON `tabAirport Shop`(airport);
CREATE INDEX idx_tenant_contract_end ON `tabTenant`(contract_end_date);
```

### Security Configuration
- Configure role-based permissions
- Set up data retention policies
- Enable audit trails for financial transactions
- Implement workflow approvals for contracts

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and add tests
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Submit pull request

### Code Standards
- Follow Frappe coding conventions
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation for changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation & Guides
- [Complete Setup Guide](COMPLETE_SETUP_GUIDE.md) - Step-by-step installation
- [Workspace Setup](AIRPORT_SHOP_WORKSPACE_SETUP.md) - Workspace configuration
- [Installation Troubleshooting](INSTALLATION_TROUBLESHOOTING.md) - Common issues

### Community Support
- 📧 **Email**: nandhakishore2165@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/macrobian88/frappe_ariplane_mode/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/macrobian88/frappe_ariplane_mode/discussions)

### Commercial Support
For enterprise support, custom development, and consultation services, contact nandhakishore2165@gmail.com.

## 🎯 Roadmap

### Current Features ✅
- Complete flight and airport operations management
- Advanced shop management with tenant tracking
- Automated rent collection and billing
- Real-time analytics and reporting
- Public portal for shop applications
- Comprehensive demo data package
- Custom workspaces with dashboards

### Upcoming Features 🔄
- **Mobile App**: React Native application for shop management
- **API Extensions**: RESTful APIs for third-party integrations
- **Advanced Analytics**: Machine learning-based occupancy predictions
- **Multi-airport Support**: Enhanced multi-location management
- **Automated Billing**: Advanced recurring invoice generation
- **Email Automation**: Contract renewal and payment reminders

## 📊 Project Stats

- **Total DocTypes**: 15+ core business entities
- **Workspaces**: 2 specialized workspaces (Airport Operations, Shop Management)
- **Demo Records**: 80+ realistic data entries across all modules
- **Custom Reports**: 5+ analytics reports and dashboards
- **Permission Roles**: 4+ user role configurations
- **GitHub Stars**: Growing community support

---

### 🎉 Get Started Today!

Transform your airport operations with this comprehensive management solution. Follow the [Complete Setup Guide](COMPLETE_SETUP_GUIDE.md) to have a fully functional system with demo data running in minutes!

**Latest Version**: 2.1.0 (with Airport Shop Management Workspace)  
**Repository**: https://github.com/macrobian88/frappe_ariplane_mode  
**Last Updated**: September 16, 2025  
**Compatible With**: Frappe v15.x, ERPNext v15.x

---

*Built with ❤️ using Frappe Framework for the aviation industry*
