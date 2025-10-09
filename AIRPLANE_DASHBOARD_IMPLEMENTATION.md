# 🛩️ Airplane Mode Dashboard Implementation Guide

This guide provides a comprehensive dashboard system for your Airplane Mode Frappe app with real-time counters and statistics.

## 📊 Dashboard Features

### Main Counters
- **Total Tickets**: Count of all airplane tickets
- **Total Flights**: Count of all flights  
- **Confirmed Tickets**: Booked + Checked-In + Boarded tickets
- **Cancelled Tickets**: Tickets with cancelled status
- **Total Passengers**: Sum of all passengers across flights
- **Revenue Statistics**: Total revenue and average ticket price

### Status Breakdowns
- **Ticket Status**: Booked, Checked-In, Boarded, Cancelled
- **Flight Status**: Scheduled, Completed, Cancelled
- **Occupancy Statistics**: Average flight occupancy percentage

## 🚀 Implementation Steps

### Step 1: Add API Files

Create the dashboard API file:

```bash
# Create the API directory if it doesn't exist
mkdir -p airplane_mode/api

# Create the dashboard API file
touch airplane_mode/api/__init__.py
touch airplane_mode/api/dashboard.py
```

Copy the `dashboard.py` content from the artifacts above.

### Step 2: Add Cancelled Status to Airplane Ticket

You need to manually add "Cancelled" to the Airplane Ticket status field:

1. Go to **Developer Mode** → **DocType** → **Airplane Ticket**
2. Find the **Status** field  
3. Update the **Options** from:
   ```
   Booked
   Checked-In
   Boarded
   ```
   
   To:
   ```
   Booked
   Checked-In
   Boarded
   Cancelled
   ```

4. **Save** the DocType

### Step 3: Add Workspace Configuration

Create the workspace config file:

```bash
# Create config file
touch airplane_mode/config/airplane_mode.py
```

Copy the workspace configuration content from the artifacts.

### Step 4: Add JavaScript Dashboard

Create the JavaScript dashboard file:

```bash
# Create public JS directory
mkdir -p airplane_mode/public/js

# Create dashboard JS file  
touch airplane_mode/public/js/airplane_dashboard.js
```

Copy the JavaScript content from the artifacts.

### Step 5: Add Web Dashboard Page

Create the web dashboard:

```bash
# Create www directory
mkdir -p airplane_mode/www

# Create dashboard HTML file
touch airplane_mode/www/airplane-dashboard.html
```

Copy the HTML content from the artifacts.

### Step 6: Add Patch for Status Update

Create patch directory and file:

```bash
# Create patches directory
mkdir -p airplane_mode/patches/v1_0

# Create patch file
touch airplane_mode/patches/v1_0/add_cancelled_status_to_airplane_ticket.py
```

Copy the patch content from the artifacts.

Update `airplane_mode/patches.txt`:
```
airplane_mode.patches.v1_0.add_cancelled_status_to_airplane_ticket
```

### Step 7: Run Setup Script

Create and run the setup script:

```bash
# Create setup script
touch airplane_mode/setup_dashboard.py
```

Copy the setup script content, then run:

```bash
# Run the setup
bench --site your-site execute airplane_mode.setup_dashboard.setup_airplane_dashboard
```

### Step 8: Update Hooks (Optional)

Add to `airplane_mode/hooks.py`:

```python
# Add these to your existing hooks.py

# Web pages
website_route_rules = [
    {"from_route": "/airplane-dashboard", "to_route": "airplane-dashboard"},
]

# Include JS files
app_include_js = [
    "/assets/airplane_mode/js/airplane_dashboard.js"
]
```

## 🔧 API Usage

### Get Dashboard Data
```python
# Get complete dashboard data
frappe.call({
    method: 'airplane_mode.api.dashboard.get_airplane_dashboard_data',
    callback: function(response) {
        console.log(response.message.data);
    }
});
```

### Get Ticket Statistics
```python
# Get detailed ticket stats
frappe.call({
    method: 'airplane_mode.api.dashboard.get_ticket_statistics', 
    callback: function(response) {
        console.log(response.message.data);
    }
});
```

### Get Flight Statistics
```python
# Get detailed flight stats
frappe.call({
    method: 'airplane_mode.api.dashboard.get_flight_statistics',
    callback: function(response) {
        console.log(response.message.data);
    }
});
```

## 📱 Access Methods

### 1. Workspace Dashboard
- Go to **Airplane Mode** workspace
- View charts and shortcuts with live counters

### 2. Web Dashboard  
- Navigate to: `https://your-site.com/airplane-dashboard`
- Full-featured dashboard with real-time updates

### 3. API Integration
- Use the API methods in custom scripts
- Integrate with external systems

## 🎨 Customization

### Adding More Counters

To add more counters, modify the `get_airplane_dashboard_data` function:

```python
# Add new counter calculation
new_counter = frappe.db.sql("""
    SELECT COUNT(*) as count 
    FROM `tabYour DocType`
    WHERE your_condition = 'value'
""", as_dict=True)[0]['count']

# Add to return data
'counters': {
    'existing_counters': ...,
    'new_counter': new_counter
}
```

### Styling Changes

Modify the CSS in the HTML file or JavaScript file to customize appearance:

```css
.counter-card {
    background: linear-gradient(135deg, #your-colors);
    /* Your custom styles */
}
```

### Auto-refresh Interval

Change the refresh interval in JavaScript:

```javascript
// Change from 30 seconds to 60 seconds
setInterval(function() {
    self.load_dashboard_data();
}, 60000); // 60 seconds
```

## 🔍 Troubleshooting

### Common Issues

1. **API Method Not Found**
   - Ensure the API file is in the correct location
   - Check that functions are decorated with `@frappe.whitelist()`

2. **Status Field Not Updating**
   - Clear cache: `bench --site your-site clear-cache`
   - Reload DocType: `bench --site your-site reload-doctype "Airplane Ticket"`

3. **Dashboard Not Loading**
   - Check browser console for JavaScript errors
   - Verify API endpoints are accessible
   - Ensure proper permissions are set

4. **Workspace Not Showing**
   - Check if workspace is published
   - Verify user has proper role permissions

### Debug Mode

Enable debug mode to see detailed error messages:

```python
# In dashboard.py, add debug logging
import frappe
frappe.log_error("Debug message", "Dashboard Debug")
```

## 📈 Performance Optimization

### Database Queries

The dashboard uses optimized SQL queries with:
- Indexed fields for fast lookups
- Aggregated queries to reduce data transfer
- Proper WHERE clauses to filter deleted records

### Caching

Consider adding caching for better performance:

```python
@frappe.whitelist()
def get_cached_dashboard_data():
    cache_key = "airplane_dashboard_data"
    cached_data = frappe.cache().get(cache_key)
    
    if not cached_data:
        cached_data = get_airplane_dashboard_data()
        frappe.cache().set(cache_key, cached_data, expires_in_sec=300)  # 5 minutes
    
    return cached_data
```

## 🔒 Security

### Permissions

Ensure proper role-based access:

```python
# Add permission checks
if not frappe.has_permission("Airplane Ticket", "read"):
    frappe.throw("Insufficient permissions")
```

### Data Sanitization

All data is properly sanitized through Frappe's built-in security measures.

## 📝 Testing

### API Testing

Test the API endpoints:

```bash
# Test dashboard API
curl -X POST \
  https://your-site.com/api/method/airplane_mode.api.dashboard.get_airplane_dashboard_data \
  -H 'Content-Type: application/json'
```

### Frontend Testing

Test the dashboard interface:
1. Create sample tickets with different statuses
2. Create sample flights with different statuses  
3. Verify counters update correctly
4. Test auto-refresh functionality

## 🎯 Next Steps

1. **Custom Reports**: Create additional reports based on dashboard data
2. **Email Notifications**: Set up alerts based on counter thresholds
3. **Mobile App**: Use the APIs to create a mobile dashboard
4. **External Integration**: Connect with external airline systems

## 📞 Support

If you encounter issues:

1. Check the Frappe logs: `bench --site your-site logs`
2. Review browser console for JavaScript errors
3. Verify database permissions and data integrity
4. Test API endpoints individually

---

**✈️ Happy Flying with your new Dashboard!** 🛩️