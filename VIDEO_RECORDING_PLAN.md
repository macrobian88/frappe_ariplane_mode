# 🎥 VIDEO RECORDING PLAN - Final Assignment Demo

## 📋 Overview
This document provides a detailed step-by-step plan for recording the demo video showcasing all implemented features for the Frappe Framework Final Assignment.

**Estimated Total Duration**: 15-20 minutes

---

## 🎬 Recording Structure

### **INTRO (1-2 minutes)**

**Script**: 
> "Hi! Welcome to my Airplane Mode app demo for the Frappe Framework certification final assignment. I'm going to walk you through all the implemented features including flight operations, airport shop management, web portals, and REST APIs. Let's get started!"

**What to show**:
- Open the Frappe instance
- Navigate to the Airplane Mode app
- Show the main dashboard/workspace

---

## 🔥 **PART 1: Core Flight Features (3-4 minutes)**

### **1.1 Crew Member Tracking (1 minute)**

**What to demonstrate**:
- Navigate to **Airplane Flight** doctype
- Create/Edit a flight and show **Flight Crew** table
- Add crew members from Employee master
- Show how crew roles are tracked

**Script**:
> "First, let's look at crew member tracking. In our Airplane Flight doctype, I have a Flight Crew table where I can assign crew members to each flight. Let me create a new flight and add some crew members..."

**Steps**:
1. Go to Airplane Flight → New
2. Fill basic flight details (airplane, airports, dates)
3. Click on Flight Crew table → Add Row
4. Select crew members from Employee dropdown
5. Show the crew member details getting fetched
6. Save the flight

### **1.2 Gate Number in Tickets (1 minute)**

**What to demonstrate**:
- Create an Airplane Ticket 
- Show gate_number field in the ticket
- Edit flight gate number
- Show background job updating all related tickets

**Script**:
> "Now let's see gate number tracking in tickets. When I create a ticket, it automatically gets the gate number from the flight. And here's the cool part - when I change the flight's gate number, it automatically updates all related tickets in the background..."

**Steps**:
1. Create Airplane Ticket for the flight
2. Show gate_number field populated from flight
3. Go back to flight and change gate_number
4. Save flight
5. Go back to ticket → Refresh → Show updated gate number
6. Mention background job functionality

### **1.3 Background Job Demo (1-2 minutes)**

**What to demonstrate**:
- Show the background job code in airplane_flight.py
- Explain the sync_gate_to_tickets function
- Show job queue or logs if possible

**Script**:
> "Let me show you how the background job works. When a flight's gate number changes, it triggers this sync_gate_to_tickets function that runs in the background and updates all associated tickets..."

**Steps**:
1. Open VS Code/browser → Show airplane_flight.py
2. Explain the sync_gate_to_tickets function
3. Show the background job queue functionality
4. Explain batch processing and error handling

---

## 🏪 **PART 2: Airport Shop Management Module (4-5 minutes)**

### **2.1 Module Overview (30 seconds)**

**What to show**:
- Navigate to Airport Shop Management module
- Show all related doctypes

**Script**:
> "Now let's explore the Airport Shop Management module. This comprehensive module helps airports track shops, manage leases, collect rent, and handle tenant relationships..."

### **2.2 Core Shop Management (1.5 minutes)**

**What to demonstrate**:
- **Airport Shop** doctype with all fields
- **Tenant** information
- **Shop Type** linking and filtering
- **Contract details** and rent management

**Steps**:
1. Go to Airport Shop → Show list view
2. Create/Edit shop → Show all fields:
   - Shop number, name
   - Shop type (link field)
   - Area, rent amount
   - Tenant information
   - Physical properties
3. Show Shop Type doctype
4. Show enabled/disabled filtering in Shop form

### **2.3 Rent Payment & Receipts (1 minute)**

**What to demonstrate**:
- Monthly rent tracking
- Payment collection process
- Print format for rent receipts

**Script**:
> "The system automatically tracks monthly rent payments and generates professional receipts. Let me show you how rent collection works..."

**Steps**:
1. Go to Monthly Invoice or Payment Entry
2. Show rent collection workflow
3. Generate and show rent receipt print format
4. Highlight Print Designer usage

### **2.4 Analytics & Reporting (1 minute)**

**What to demonstrate**:
- Shop occupancy tracking
- Available vs occupied shops
- Airport-wise analytics

**Steps**:
1. Show shop analytics dashboard/report
2. Navigate to Reports section
3. Show occupancy statistics
4. Demonstrate airport-wise shop distribution

### **2.5 Scheduled Rent Reminders (1 minute)**

**What to demonstrate**:
- Scheduler configuration in hooks.py
- Email reminder functionality
- Global settings for rent reminders

**Script**:
> "The system automatically sends rent reminder emails every month using Frappe's scheduler. Let me show you the configuration..."

**Steps**:
1. Open hooks.py → Show scheduler_events
2. Show rent_reminder.py file
3. Show global settings for enabling/disabling reminders
4. Show email template if available

---

## 🌐 **PART 3: Web Portal (3-4 minutes)**

### **3.1 Shop List Page (1 minute)**

**What to demonstrate**:
- Navigate to public web portal
- Show shops listing page
- Custom CSS styling (not inherited from base template)

**Script**:
> "Now let's look at the public web portal. I've created a complete shop management portal that doesn't inherit from Frappe's base template and uses custom CSS..."

**Steps**:
1. Open new browser tab → Go to public URL
2. Navigate to `/shops` or `/shop-portal`
3. Show list of available shops
4. Highlight custom styling

### **3.2 Shop Details Pages (1 minute)**

**What to demonstrate**:
- Click on individual shops
- Show detailed shop information
- Shop lead web form integration

**Steps**:
1. Click on a shop from the list
2. Show detailed shop information page
3. Point out the "Apply for this shop" button/form
4. Show web form for collecting shop leads

### **3.3 Shop Lead Collection (1-2 minutes)**

**What to demonstrate**:
- Fill out the web form
- Show lead creation in backend
- Email notifications

**Script**:
> "When someone is interested in renting a shop, they can fill out this lead form. Let me show you how this works..."

**Steps**:
1. Fill out the shop lead web form
2. Submit the form
3. Go to backend → Show created Shop Lead document
4. Show email notification if configured
5. Explain lead nurturing process

---

## 🔧 **PART 4: Shop Types & Configuration (2 minutes)**

### **4.1 Shop Type DocType (1 minute)**

**What to demonstrate**:
- Shop Type doctype with Enabled checkbox
- Out-of-box shop types (fixtures)
- Link field filtering

**Script**:
> "The system comes with predefined shop types and smart filtering. Let me show you how shop types work..."

**Steps**:
1. Go to Shop Type doctype
2. Show existing types: Stall, Walk-through, Normal, Food Court, Duty Free
3. Show Enabled checkbox functionality
4. Go to Shop form → Show filtered shop types in dropdown

### **4.2 Global Settings (1 minute)**

**What to demonstrate**:
- Airport Shop Settings (single doctype)
- Default rent configuration
- Rent reminder enable/disable

**Steps**:
1. Go to Airport Shop Settings
2. Show default rent amount setting
3. Show rent reminder enable/disable toggle
4. Explain how these settings are used across the system

---

## 📡 **PART 5: REST API Demo with Bruno (3-4 minutes)**

### **5.1 Bruno Setup (30 seconds)**

**What to show**:
- Bruno application open
- Import API collection
- Show environment variables setup

**Script**:
> "Now for the REST API demo using Bruno. I've prepared a comprehensive API collection that demonstrates both custom APIs and standard Frappe REST APIs..."

### **5.2 Authentication Setup (30 seconds)**

**What to demonstrate**:
- Show API key generation in Frappe
- Configure authentication in Bruno
- Explain token-based auth

**Steps**:
1. In Frappe: User Profile → API Access → Generate API Key
2. In Bruno: Show environment variables
3. Explain Authorization header format

### **5.3 Get Shop List API (1 minute)**

**What to demonstrate**:
- Execute GET request for shop list
- Show complete response with all fields
- Explain custom vs standard API differences

**Steps**:
1. Execute: GET /api/method/airplane_mode.api.shop_api.get_shops_list
2. Show response JSON with shop details
3. Explain data structure and fields returned

### **5.4 Create Shop via API (1.5 minutes)**

**What to demonstrate**:
- Execute POST request to create new shop
- Show request payload
- Validate creation in Frappe backend

**Script**:
> "Now let me create a new shop using the API. I'll send a POST request with all the required shop details..."

**Steps**:
1. Show POST request body in Bruno
2. Execute: POST /api/method/airplane_mode.api.shop_api.create_shop
3. Show successful response
4. Go to Frappe → Verify shop was created
5. Show all populated fields

### **5.5 Standard Frappe APIs (30 seconds)**

**What to demonstrate**:
- Show standard GET /api/resource/Airport Shop
- Compare with custom API response
- Mention filtering capabilities

**Steps**:
1. Execute standard Frappe API
2. Show response format difference
3. Mention standard API features

---

## 🎯 **CLOSING & SUMMARY (1-2 minutes)**

### **Summary Checklist**

**Script**:
> "Let me quickly summarize everything we've covered in this demo..."

**Go through each requirement**:

✅ **Part 1 - Core Features**:
- ✅ Crew member tracking in flights  
- ✅ Gate number tracking in tickets
- ✅ Background job for gate synchronization

✅ **Part 2 - Shop Management Module**:
- ✅ Complete shop tracking system
- ✅ Tenant and contract management
- ✅ Rent payment collection & receipts
- ✅ Shop analytics and occupancy tracking
- ✅ Automated rent reminders via scheduler
- ✅ Global configurations for defaults and settings

✅ **Part 3 - Web Portal**:
- ✅ Public shop listing pages
- ✅ Individual shop detail pages  
- ✅ Shop lead collection web forms
- ✅ Custom CSS styling (non-inherited)

✅ **Part 4 - Shop Types**:
- ✅ Shop Type doctype with Enabled field
- ✅ Out-of-box shop types via fixtures
- ✅ Filtered link fields using set_query

✅ **Part 5 - REST APIs**:
- ✅ Bruno API client usage
- ✅ Custom shop management APIs
- ✅ Standard Frappe REST APIs
- ✅ Proper authentication implementation

**Final Script**:
> "That completes our comprehensive demo of the Airplane Mode app! We've covered all the assignment requirements including flight operations, shop management, web portals, and REST APIs. The system is production-ready with proper error handling, background jobs, email automation, and comprehensive API coverage. Thank you for watching!"

---

## 🎥 **Recording Tips**

### **Technical Setup**:
- **Screen Resolution**: 1920x1080 minimum
- **Recording Software**: OBS Studio, Loom, or built-in screen recorder
- **Audio**: Clear microphone, no background noise
- **Browser**: Chrome/Firefox with good zoom level (125%)

### **Presentation Tips**:
1. **Speak clearly and at moderate pace**
2. **Explain each action before performing it**
3. **Use cursor highlighting/zoom if available**
4. **Keep transitions smooth between sections**
5. **Have backup data ready in case of errors**
6. **Test all functionality before recording**

### **Pre-Recording Checklist**:
- [ ] All doctypes and data are properly set up
- [ ] Web portal is accessible and styled
- [ ] Bruno API collection is imported and working  
- [ ] API credentials are configured
- [ ] Email settings are configured for notifications
- [ ] Scheduler is enabled for background jobs
- [ ] Print formats are configured for receipts
- [ ] Demo data includes diverse examples

### **File Organization**:
- Save recording in MP4 format
- Keep file size under 500MB if possible
- Name file: `airplane_mode_final_assignment_demo.mp4`
- Include timestamp in filename for versioning

---

**This plan ensures comprehensive coverage of all assignment requirements while maintaining a logical flow and professional presentation style.**
