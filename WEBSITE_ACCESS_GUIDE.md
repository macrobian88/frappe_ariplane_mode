# 🌐 Website Access Guide - Airport Management System

## How to Access the Website

Your Airport Management System now has a fully functional website interface! Here's how to access all the different parts:

### 🏠 **Main Homepage**
```
https://airplane-mode.m.frappe.cloud/
```
- **Features**: Hero section with statistics, navigation cards, featured shops
- **Displays**: Total shops, available shops, active flights, shop types
- **Navigation**: Links to all major sections

### ✈️ **Flight Information**
```
https://airplane-mode.m.frappe.cloud/flights
```
- **Purpose**: View flight schedules, gates, and status updates
- **Content**: Real-time flight information and airport operations

### 🏪 **Shop Portal** (Main Shop Management)
```
https://airplane-mode.m.frappe.cloud/shop-portal
```
- **Purpose**: Complete shop management interface
- **Features**: Shop listings, management tools, tenant portal

### 🔍 **Browse Available Shops**
```
https://airplane-mode.m.frappe.cloud/shop-availability
```
- **Features**:
  - Filter by shop type, area, rent price
  - Professional shop cards with images and details
  - Statistics dashboard
  - "Apply Now" buttons for each shop

### 📝 **Apply for Shop Rental**
```
https://airplane-mode.m.frappe.cloud/apply-shop
```
- **Features**:
  - Comprehensive application form
  - Personal and business information collection
  - Shop preferences selection
  - Automatic Shop Lead creation

### 🏬 **Individual Shop Pages**
```
https://airplane-mode.m.frappe.cloud/shops
https://airplane-mode.m.frappe.cloud/shop/[shop-id]
```
- **Purpose**: Detailed information about specific shops

## 🔐 **User Access Levels**

### **Guest/Public Users**
- ✅ Homepage browsing
- ✅ Flight information
- ✅ Available shops listing
- ✅ Shop applications
- ✅ Basic shop portal viewing

### **Logged-in Users (Role-based)**
- **Airport Manager**: Full access to all features
- **Shop Manager**: Shop operations and lead management  
- **Tenant**: Personal contracts and payment history
- **Ground Staff**: Read-only access to operations

## 🚀 **Getting Started Steps**

### 1. **Deploy and Migrate**
```bash
# Make sure latest code is deployed
git pull origin main

# Run migration
bench --site airplane-mode.m.frappe.cloud migrate

# Clear cache
bench --site airplane-mode.m.frappe.cloud clear-cache
```

### 2. **Access the Website**
Navigate to: `https://airplane-mode.m.frappe.cloud/`

### 3. **Test Key Features**
- Browse available shops
- Submit a shop application  
- Check flight information
- Use the shop portal

### 4. **Admin Setup (Optional)**
- Create user roles (Airport Manager, Shop Manager, Tenant)
- Set up email configurations for notifications
- Add shop types and shop data
- Configure portal permissions

## 📱 **Mobile Responsive**
All pages are fully responsive and work on:
- 📱 Mobile devices
- 📊 Tablets  
- 💻 Desktop computers

## 🎨 **Features Highlights**

### **Homepage**
- Modern gradient hero section
- Real-time statistics display
- Feature navigation cards
- Featured available shops
- User welcome section (when logged in)

### **Shop Availability**
- Advanced filtering system
- Professional shop cards
- High-quality image support
- Clear pricing and details
- Direct application links

### **Application System**
- Multi-step form design
- Real-time validation
- Pre-selection from shop listings
- Professional business information collection
- Automatic lead processing

## 🔧 **Customization Options**

### **Styling**
- Bootstrap 5 framework
- Custom CSS for airport theme
- Professional color scheme
- Hover effects and animations

### **Content**
- Fully translatable (uses Frappe's `_()` function)
- Configurable through DocTypes
- Dynamic content from database
- SEO-friendly URLs

## 📞 **Support & Troubleshooting**

### **Common Issues**
1. **Page not loading**: Check migration status and clear cache
2. **Images not showing**: Verify file paths and permissions
3. **Forms not submitting**: Check DocType permissions and field validations

### **Debugging**
```bash
# Check logs
tail -f logs/web.log

# Restart services
bench restart

# Check site status  
bench --site airplane-mode.m.frappe.cloud doctor
```

## 🌟 **Next Steps**

1. **Content Setup**: Add shop types, shops, and flight data
2. **User Management**: Create roles and assign permissions
3. **Email Configuration**: Set up SMTP for notifications
4. **Branding**: Customize logo, favicon, and colors
5. **Analytics**: Monitor usage and performance

## 📋 **URL Summary**

| Page | URL | Purpose |
|------|-----|---------|
| Homepage | `/` | Landing page with overview |
| Flights | `/flights` | Flight schedules and info |
| Shop Portal | `/shop-portal` | Main shop management |
| Browse Shops | `/shop-availability` | Available shop listings |
| Apply | `/apply-shop` | Shop rental applications |
| Individual Shop | `/shop/[id]` | Specific shop details |
| All Shops | `/shops` | Complete shop directory |

Your Airport Management System is now ready for public access with a professional, modern website interface! 🎉
