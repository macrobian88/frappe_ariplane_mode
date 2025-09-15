# Airport Management System 🛩️

A comprehensive Frappe ERPNext application for managing airport operations including flight management, passenger services, crew assignment, and shop management with automated rent collection.

## 🌟 Features

### ✈️ Flight Operations
- **Flight Management**: Complete flight scheduling and management system
- **Crew Assignment**: Automated crew assignment and tracking
- **Gate Management**: Real-time gate allocation and management
- **Passenger Services**: Ticket management and passenger tracking
- **Flight Status**: Real-time flight status updates

### 🏪 Shop Management
- **Shop Registration**: Complete shop registration and management
- **Contract Management**: Automated lease agreements and contracts
- **Rent Collection**: Automated monthly rent collection and invoicing
- **Lead Management**: Lead generation, tracking, and conversion
- **Payment Tracking**: Real-time payment status and reminders

### 📊 Analytics & Reporting
- **Revenue Analytics**: Comprehensive revenue trends and forecasting
- **Occupancy Reports**: Shop occupancy rates by type and location
- **Lead Conversion**: Lead-to-customer conversion tracking
- **Financial Reports**: Monthly, quarterly, and annual financial reports
- **Performance Dashboard**: Real-time KPIs and metrics

### 🌐 Public Portal
- **Shop Availability**: Public portal showing available shops
- **Online Applications**: Streamlined application process for potential lessees
- **Automated Notifications**: Email confirmations and follow-ups
- **Lead Management**: Automated lead capture and processing

## 🚀 Installation

### Prerequisites
- Frappe Framework 14+
- ERPNext (optional, for financial integration)
- Python 3.8+
- Node.js 16+

### Quick Installation

```bash
# Navigate to your bench directory
cd $PATH_TO_YOUR_BENCH

# Get the app
bench get-app https://github.com/macrobian88/frappe_ariplane_mode.git

# Install the app
bench install-app airplane_mode

# Restart bench
bench restart
```

### Development Setup

```bash
# For development mode
bench get-app https://github.com/macrobian88/frappe_ariplane_mode.git --branch main

# Install in development mode
bench install-app airplane_mode

# Start development server
bench start
```

## ⚙️ Configuration

After installation, configure the following:

### 1. Basic Setup
- **Shop Types**: Configure shop categories (Food Court, Duty Free, etc.)
- **Airports**: Set up your airport locations and terminals
- **Email Settings**: Configure SMTP for automated notifications

### 2. Scheduled Jobs
Enable the following background tasks:
- **Daily**: Rent reminder emails, monthly invoice processing
- **Weekly**: Management reports and analytics
- **Monthly**: Performance metrics updates

### 3. Permissions
Set up role-based permissions for:
- Airport Shop management
- Contract Shop administration
- Lead management
- Financial operations

## 🔌 API Reference

### Public APIs (Guest Access)

#### Get Available Shops
```http
GET /api/method/airplane_mode.api.shop_portal.get_available_shops
```

**Response:**
```json
{
  "message": {
    "status": "success",
    "shops": [...],
    "shops_by_type": {...},
    "total_available": 15
  }
}
```

#### Submit Shop Application
```http
POST /api/method/airplane_mode.api.shop_portal.submit_shop_application
Content-Type: application/json

{
  "shop_id": "SHOP-001",
  "lead_data": {
    "lead_name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "business_type": "Restaurant",
    "message": "Interested in opening a coffee shop"
  }
}
```

### Authenticated APIs

#### Dashboard Data
```http
GET /api/method/airplane_mode.api.shop_portal.get_dashboard_data
```

#### Shop Analytics
```http
GET /api/method/airplane_mode.api.analytics.get_shop_analytics?shop_id=SHOP-001&date_range=6m
```

#### Revenue Trends
```http
GET /api/method/airplane_mode.api.analytics.get_revenue_trends
```

#### Financial Summary
```http
GET /api/method/airplane_mode.api.analytics.get_financial_summary
```

## 🏗️ Architecture

### DocTypes

#### Core Flight Management
- **Airplane**: Aircraft details and specifications
- **Airplane Flight**: Flight scheduling and management
- **Airplane Ticket**: Passenger ticket management
- **Crew Member**: Staff assignment and tracking

#### Shop Management
- **Airport Shop**: Shop registration and details
- **Shop Type**: Shop categorization and configuration
- **Contract Shop**: Lease agreements and rental contracts
- **Shop Lead**: Lead generation and tracking system

### Background Jobs

The system includes automated background jobs:

```python
# Daily Tasks
- Send rent reminder emails
- Process monthly invoices
- Update payment statuses

# Weekly Tasks  
- Generate management reports
- Send performance summaries

# Monthly Tasks
- Update analytics metrics
- Generate financial reports
```

### Email Templates

Pre-configured email templates for:
- Shop lead welcome emails with beautiful HTML design
- Rent reminder notifications with payment details
- Contract renewal notices
- Invoice notifications with payment links

## 🌐 Web Portal

### Shop Portal Features
- **Responsive Design**: Works on all devices
- **Advanced Filtering**: Filter by shop type, size, location
- **Real-time Search**: Instant search functionality
- **Detailed Shop Views**: Comprehensive shop information
- **Online Applications**: Streamlined application process
- **Beautiful UI**: Modern Bootstrap 5 design

### Portal URLs
- **Main Portal**: `/shop-portal`
- **Shop Availability**: `/shop-availability`
- **Application Form**: `/apply-shop`

## 🎨 Customization

### Adding Custom Fields

```python
# Example: Add custom fields to Airport Shop
frappe.get_doc({
    "doctype": "Custom Field",
    "dt": "Airport Shop",
    "fieldname": "custom_wifi_available",
    "label": "WiFi Available",
    "fieldtype": "Check"
}).insert()
```

### Custom Business Logic

```python
# Example: Custom validation for Contract Shop
def validate_contract(doc, method):
    if doc.end_date <= doc.start_date:
        frappe.throw("End date must be after start date")
```

### Custom Reports

Create custom reports using Frappe's Report Builder:

```python
# Example: Custom Revenue Report
def execute(filters=None):
    columns = [
        {"fieldname": "shop", "label": "Shop", "fieldtype": "Link", "options": "Airport Shop"},
        {"fieldname": "revenue", "label": "Revenue", "fieldtype": "Currency"}
    ]
    
    data = frappe.db.sql("""
        SELECT shop, SUM(monthly_rent) as revenue
        FROM `tabContract Shop`
        WHERE docstatus = 1
        GROUP BY shop
    """, as_dict=True)
    
    return columns, data
```

## 🧪 Testing

Run tests using:

```bash
# Run all tests
bench run-tests --app airplane_mode

# Run specific test
bench run-tests --app airplane_mode --module airplane_mode.tests.test_shop_portal

# Run with coverage
bench run-tests --app airplane_mode --coverage
```

## 📈 Performance

### Database Optimization
- Indexed fields for faster queries
- Optimized database schema
- Efficient background job processing

### Caching
- API response caching for better performance
- Static asset optimization
- Efficient query patterns

## 🔒 Security

### Data Protection
- GDPR compliant data handling
- User data encryption
- Secure API endpoints
- Role-based access control

### Privacy Features
- Data retention policies (90 days for leads, 1 year for contracts)
- User consent management
- Automated data cleanup

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Submit a pull request

### Code Style

This project uses:
- **Python**: PEP 8 style guide with Black formatting
- **JavaScript**: ESLint configuration with Prettier
- **Pre-commit hooks**: Automated code formatting

```bash
# Install pre-commit hooks
cd apps/airplane_mode
pre-commit install
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [User Guide](docs/user-guide.md)
- [Administrator Guide](docs/admin-guide.md)
- [API Documentation](docs/api.md)
- [Troubleshooting](docs/troubleshooting.md)

### Community Support
- 📧 Email: nandhakishore2165@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/macrobian88/frappe_ariplane_mode/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/macrobian88/frappe_ariplane_mode/discussions)

### Commercial Support
For enterprise support, custom development, and consultation services, please contact us at nandhakishore2165@gmail.com.

## 🙏 Acknowledgments

- Built with ❤️ using [Frappe Framework](https://frappeframework.com)
- Inspired by modern airport management needs
- Community feedback and contributions
- Bootstrap 5 for beautiful UI components
- Font Awesome for icons

## 📊 Project Status

- ✅ Core flight management
- ✅ Shop management system  
- ✅ Automated rent collection
- ✅ Public web portal
- ✅ Analytics dashboard
- ✅ Email notification system
- ✅ Lead management system
- ✅ Beautiful responsive UI
- 🔄 Mobile app (planned)
- 🔄 Advanced reporting (planned)
- 🔄 Multi-airport support (planned)

## 🚀 Recent Updates

### Version 1.0.0 (Latest)
- **New**: Complete shop management system
- **New**: Automated rent collection with invoicing
- **New**: Public shop portal with online applications
- **New**: Beautiful email notifications with HTML templates
- **New**: Comprehensive analytics and reporting
- **New**: Modern responsive web design
- **Enhanced**: Background job automation
- **Enhanced**: API endpoints for shop management
- **Fixed**: Various performance improvements

---

**Made with ❤️ for the aviation industry**

*Transform your airport operations with this comprehensive management solution.*