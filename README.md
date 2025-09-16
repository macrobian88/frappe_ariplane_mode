# 🚁 Airplane Mode - Airport Management System

> ✨ **Latest Update**: Added comprehensive Airport Shop Management workspace with bulk demo data creation for full-scale testing!

A comprehensive Frappe application for managing airport operations including flight management, passenger services, crew assignment, and advanced shop management with automated rent collection and analytics.

## 🌟 New Features & Updates

### 🎯 Enhanced Bulk Data Creation
- **New Script**: `create_bulk_sample_data.py` creates extensive demo data
- **100+ Airport Shops** across 25+ global airports
- **50+ Airplanes** with diverse models and specifications  
- **35+ Flights** with realistic scheduling and routing
- **55+ Passengers** with varied demographics
- **15+ Airlines** from major international carriers
- **20+ Tenants** with major brand partnerships

### 🏪 Airport Shop Management Workspace
- **Real-time Dashboard**: Live occupancy, revenue, and tenant metrics
- **Quick Shortcuts**: Direct access to shops, tenants, contracts, reports
- **Smart Quick Lists**: Pre-filtered views for available shops, expiring contracts
- **Advanced Analytics**: Revenue summaries and occupancy reports

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

# For basic demo data (20-30 records each)
bench --site your-site-name execute airplane_mode.install_demo_data

# For extensive bulk data (100+ records each) - RECOMMENDED for testing
bench --site your-site-name execute airplane_mode.create_bulk_sample_data

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

## 📊 Data Creation Options

### Option 1: Basic Demo Data (`install_demo_data.py`)
- **Perfect for**: Initial setup and basic testing
- **Creates**:
  - 5 Airlines with detailed information
  - 7 Airports with proper IATA codes
  - 8 Airplanes with realistic specifications
  - 20 Airport Shops across major airports
  - 8 Active Tenants with lease agreements
  - 5 Customers and basic contracts

```bash
bench --site your-site-name execute airplane_mode.install_demo_data
```

### Option 2: Bulk Sample Data (`create_bulk_sample_data.py`) - RECOMMENDED
- **Perfect for**: Full-scale testing and demonstrations
- **Creates**:
  - **15+ Airlines**: Major international carriers with headquarters info
  - **25+ Airports**: Global airports with proper codes (JFK, LHR, DXB, SIN, etc.)
  - **55+ Airplanes**: Diverse fleet with Boeing/Airbus models
  - **120+ Airport Shops**: Realistic shops with major brands (Starbucks, Apple, McDonald's)
  - **55+ Passengers**: Varied demographics and nationalities
  - **35+ Flights**: Complex routing with realistic schedules
  - **30+ Tenants**: Major brand partnerships with contract details

```bash
bench --site your-site-name execute airplane_mode.create_bulk_sample_data
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

## 🗄️ Comprehensive Data Package

The bulk data creation script provides enterprise-level sample data:

### Airlines & Aircraft Fleet
- **15 Global Airlines**: 
  - Sky Airways International (USA) - Seattle, WA
  - Global Wings Express (Canada) - Toronto, ON
  - Ocean Air Pacific (Australia) - Sydney, NSW
  - Mountain Express Airlines (India) - Mumbai, MH
  - Eagle Airlines Europe (UK) - London, UK
  - Phoenix Airways (Germany) - Frankfurt, DE
  - And 9 more international carriers...

- **55+ Aircraft**: 
  - Boeing: 737-800, 737-900, 787-8/9/10, 777-200ER/300ER, 747-8
  - Airbus: A320, A321, A330-300, A340-600, A350-900/1000, A380
  - Regional: Embraer E175, Bombardier CRJ-900, ATR 72-600
  - Realistic capacity ranges from 78 to 615 passengers

### Global Airport Network
- **25+ International Airports**:
  - Americas: JFK, LAX, YYZ, GRU, MEX, MIA
  - Europe: LHR, CDG, FRA, AMS, ZUR, FCO, MAD
  - Asia-Pacific: DXB, SIN, HND, PEK, ICN, SYD, BOM, DEL, HKG, BKK
  - Africa & Middle East: IST, DOH, CPT

### Extensive Shop Ecosystem
- **120+ Airport Shops** with major brands:
  - **Food & Dining**: McDonald's, Burger King, Starbucks, Costa Coffee, Pizza Hut, Subway
  - **Retail**: Apple Store, Samsung Experience, Hudson News, WHSmith, Duty Free
  - **Fashion**: Hugo Boss, Gucci, Ray-Ban, Victoria's Secret
  - **Services**: Hertz, Avis, Boots Pharmacy, 7-Eleven
  - **Specialty**: Sephora, Fossil, Lego Store, and more

- **18 Shop Categories**: From premium restaurants to car rental services
- **Realistic Financials**: Rent ranges from $5,000 to $80,000 monthly based on location and type
- **70% Occupancy Rate**: Mix of occupied and vacant shops for realistic testing

### Flight Operations
- **35+ Active Flights**: 
  - Realistic routing between major hubs
  - Proper scheduling with departure/arrival times
  - Mixed status: Scheduled, Boarding, Departed, Arrived, Delayed
  - Duration-based routing (1-16 hours)

### Passenger Services
- **55+ Passengers**: 
  - Diverse demographics and nationalities
  - Age ranges from 18-80 years
  - Global representation from 18+ countries
  - Realistic name combinations

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

## 🧪 Testing Your Installation

After installation, verify the system with bulk data:

### 1. Access Workspaces
- **Airport Operations**: Navigate to "Airplane Mode" workspace
- **Shop Management**: Navigate to "Airport Shop Management" workspace
- **Verify Counts**: Dashboard should show 100+ shops, 50+ airplanes, 15+ airlines

### 2. Test Data Integrity
```bash
# Check bulk data installation
bench --site your-site-name console
```

In console:
```python
import frappe

# Verify bulk data counts
print("=== BULK DATA VERIFICATION ===")
print(f"Airlines: {frappe.db.count('Airline')}")
print(f"Airports: {frappe.db.count('Airport')}")
print(f"Airplanes: {frappe.db.count('Airplane')}")
print(f"Airport Shops: {frappe.db.count('Airport Shop')}")
print(f"Shop Types: {frappe.db.count('Shop Type')}")
print(f"Passengers: {frappe.db.count('Passenger')}")
print(f"Flights: {frappe.db.count('Airplane Flight')}")
print(f"Tenants: {frappe.db.count('Tenant')}")
print(f"Customers: {frappe.db.count('Customer')}")

# Occupancy statistics
occupied = frappe.db.count('Airport Shop', {'is_occupied': 1})
vacant = frappe.db.count('Airport Shop', {'is_occupied': 0})
total_shops = occupied + vacant
occupancy_rate = (occupied / total_shops * 100) if total_shops > 0 else 0

print(f"\n=== OCCUPANCY ANALYTICS ===")
print(f"Occupied Shops: {occupied}")
print(f"Vacant Shops: {vacant}")
print(f"Occupancy Rate: {occupancy_rate:.1f}%")
```

Expected output with bulk data:
- Airlines: 15+
- Airports: 25+
- Airplanes: 55+
- Airport Shops: 120+
- Occupancy Rate: ~70%

### 3. Performance Testing
```bash
# Test search performance with large datasets
# Navigate to Airport Shop list
# Apply filters and verify quick response
# Test link field searches in contracts
```

## 📚 Documentation

### Installation & Setup
- [🚀 **Complete Setup Guide**](COMPLETE_SETUP_GUIDE.md) - Comprehensive installation and configuration
- [🏪 **Workspace Setup**](AIRPORT_SHOP_WORKSPACE_SETUP.md) - Workspace configuration details
- [💾 **Demo Data Script**](install_demo_data.py) - Basic demo data installation
- [🎯 **Bulk Data Script**](create_bulk_sample_data.py) - Comprehensive bulk data creation
- [🔧 **Installation Troubleshooting**](INSTALLATION_TROUBLESHOOTING.md) - Common issues and solutions

### Advanced Usage
- API documentation for shop portal integration
- Permission configuration guides
- Custom report creation tutorials
- Background job setup instructions
- Performance optimization guides

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

#### Large Data Set Performance
```bash
# Add database indexes for better performance with bulk data
bench --site your-site-name console
```

```python
# Run in console for performance optimization
import frappe

# Add indexes for better search performance
frappe.db.sql("""
    CREATE INDEX IF NOT EXISTS idx_airport_shop_occupied 
    ON `tabAirport Shop`(is_occupied);
""")

frappe.db.sql("""
    CREATE INDEX IF NOT EXISTS idx_airport_shop_airport 
    ON `tabAirport Shop`(airport);
""")

frappe.db.sql("""
    CREATE INDEX IF NOT EXISTS idx_airplane_flight_status 
    ON `tabAirplane Flight`(status);
""")

frappe.db.commit()
print("Performance indexes added successfully!")
```

#### Memory Issues with Bulk Data
```bash
# Increase memory limits if needed
# In your site_config.json, add:
{
    "db_query_timeout": 300,
    "max_file_size": 50000000
}
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Test with bulk data: `bench --site your-site-name execute airplane_mode.create_bulk_sample_data`
4. Make changes and add tests
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Submit pull request

### Code Standards
- Follow Frappe coding conventions
- Test with both basic and bulk demo data
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
- Bulk demo data creation (120+ shops, 55+ aircraft)
- Performance-optimized large dataset handling
- Custom workspaces with dashboards

### Upcoming Features 🔄
- **Mobile App**: React Native application for shop management
- **API Extensions**: RESTful APIs for third-party integrations
- **Advanced Analytics**: Machine learning-based occupancy predictions
- **Multi-airport Support**: Enhanced multi-location management
- **Data Import Tools**: Excel/CSV import for bulk operations
- **Email Automation**: Contract renewal and payment reminders

## 📊 Project Stats

- **Total DocTypes**: 15+ core business entities
- **Workspaces**: 2 specialized workspaces (Airport Operations, Shop Management)
- **Demo Records**: 300+ realistic data entries across all modules
- **Custom Reports**: 5+ analytics reports and dashboards
- **Permission Roles**: 4+ user role configurations
- **Performance**: Optimized for 1000+ records per DocType

---

### 🎉 Get Started Today!

Transform your airport operations with this comprehensive management solution. Use the bulk data creation script to have a fully populated system running in minutes!

```bash
# Quick start with full dataset
git clone https://github.com/macrobian88/frappe_ariplane_mode.git
bench get-app ./frappe_ariplane_mode
bench --site your-site-name install-app airplane_mode
bench --site your-site-name execute airplane_mode.create_bulk_sample_data
```

**Latest Version**: 2.2.0 (with Bulk Data Creation)  
**Repository**: https://github.com/macrobian88/frappe_ariplane_mode  
**Last Updated**: September 16, 2025  
**Compatible With**: Frappe v15.x, ERPNext v15.x

---

*Built with ❤️ using Frappe Framework for the aviation industry*
