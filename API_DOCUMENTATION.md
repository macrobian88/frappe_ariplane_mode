# Airplane Mode - REST API Documentation

## 🚀 Overview

This document provides comprehensive information about the REST APIs available in the Airplane Mode application for managing airport shops, flights, and related operations.

## 🔐 Authentication

All API endpoints require authentication using API Key and Secret:

```
Authorization: token {api_key}:{api_secret}
```

### How to get API credentials:
1. Login to your Frappe instance
2. Go to User Profile → API Access
3. Generate new API Key and Secret
4. Use them in the Authorization header

## 📡 Base URLs

- **Local Development**: `http://localhost:8000`
- **Frappe Cloud**: `https://airplane-mode.m.frappe.cloud`

## 🏪 Shop Management APIs

### 1. Get All Shops
**Endpoint**: `GET /api/method/airplane_mode.api.shop_api.get_shops_list`

Returns list of all shops with complete details.

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "name": "SHOP-001",
      "shop_number": "S001",
      "shop_name": "Coffee Corner",
      "shop_type": "Food Court",
      "area_sqft": 150,
      "rent_amount": 12000,
      "is_occupied": 1,
      "tenant": "Starbucks Corp",
      "airport": "Mumbai International",
      "location_description": "Terminal 2, Gate A15",
      "status": "Occupied"
    }
  ],
  "count": 25
}
```

### 2. Create New Shop
**Endpoint**: `POST /api/method/airplane_mode.api.shop_api.create_shop`

**Required Parameters**:
- `shop_number`: Unique shop identifier
- `shop_name`: Display name of the shop
- `shop_type`: Type from Shop Type master
- `area_sqft`: Shop area in square feet
- `airport`: Airport location

**Optional Parameters**:
- `rent_amount`: Monthly rent
- `location_description`: Physical location details
- `tenant`: Tenant name if occupied

**Example Request**:
```json
{
  "shop_number": "SHOP-101",
  "shop_name": "Electronics Hub",
  "shop_type": "Normal",
  "area_sqft": 300,
  "airport": "Mumbai International Airport",
  "rent_amount": 25000,
  "location_description": "Terminal 1, Level 2"
}
```

### 3. Get Shop Details
**Endpoint**: `GET /api/method/airplane_mode.api.shop_api.get_shop_details?shop_id=SHOP-001`

Returns detailed shop information including contract history.

### 4. Get Shop Types
**Endpoint**: `GET /api/method/airplane_mode.api.shop_api.get_shop_types`

Returns all enabled shop types:
- Stall
- Walk-through  
- Normal
- Food Court
- Duty Free

### 5. Get Airport Analytics
**Endpoint**: `GET /api/method/airplane_mode.api.shop_api.get_airport_analytics?airport=Mumbai`

Returns occupancy statistics and analytics.

## ✈️ Standard Frappe REST APIs

### Airport Shop Resource
- **GET** `/api/resource/Airport Shop` - List all shops
- **POST** `/api/resource/Airport Shop` - Create new shop
- **GET** `/api/resource/Airport Shop/{name}` - Get specific shop
- **PUT** `/api/resource/Airport Shop/{name}` - Update shop
- **DELETE** `/api/resource/Airport Shop/{name}` - Delete shop

### Flight Passenger Resource  
- **GET** `/api/resource/Flight Passenger` - List passengers
- **POST** `/api/resource/Flight Passenger` - Create passenger

### Airplane Ticket Resource
- **GET** `/api/resource/Airplane Ticket` - List tickets
- **POST** `/api/resource/Airplane Ticket` - Create ticket

## 🛠️ Testing with Bruno

1. **Download Bruno**: [https://www.usebruno.com/](https://www.usebruno.com/)
2. **Import Collection**: Load `bruno_api_collection/airplane_mode_api.json`
3. **Set Environment Variables**:
   - `base_url`: Your Frappe instance URL
   - `api_key`: Your API key
   - `api_secret`: Your API secret

### Example Bruno Environment:
```json
{
  "name": "Airplane Mode Demo",
  "variables": [
    {
      "name": "base_url",
      "value": "https://airplane-mode.m.frappe.cloud"
    },
    {
      "name": "api_key", 
      "value": "your_api_key_here"
    },
    {
      "name": "api_secret",
      "value": "your_api_secret_here"  
    }
  ]
}
```

## 📊 Response Formats

### Success Response:
```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully"
}
```

### Error Response:
```json
{
  "success": false,
  "error": "Detailed error message",
  "exc_type": "ValidationError"
}
```

## 🔍 Filtering and Pagination

Standard Frappe APIs support filtering:

```
GET /api/resource/Airport Shop?filters=[["is_occupied", "=", 1]]
GET /api/resource/Airport Shop?fields=["shop_number", "shop_name", "rent_amount"]
GET /api/resource/Airport Shop?limit_start=20&limit_page_length=10
```

## 🛡️ Security Best Practices

1. **Always use HTTPS** in production
2. **Store API credentials securely**
3. **Rotate API keys regularly**
4. **Implement rate limiting**
5. **Validate all input parameters**
6. **Log API usage for monitoring**

## 🚦 Rate Limits

- **Standard APIs**: 100 requests per minute per user
- **Custom APIs**: 50 requests per minute per user
- **Bulk operations**: 10 requests per minute per user

## 📝 Error Codes

- **400**: Bad Request - Invalid parameters
- **401**: Unauthorized - Invalid credentials
- **403**: Forbidden - Insufficient permissions
- **404**: Not Found - Resource doesn't exist
- **429**: Rate Limited - Too many requests
- **500**: Internal Server Error - System error

## 🔗 Related Resources

- [Frappe REST API Documentation](https://frappeframework.com/docs/v13/user/en/api/rest)
- [Frappe Authentication Guide](https://frappeframework.com/docs/v13/user/en/api/rest#authentication)
- [Bruno API Client](https://www.usebruno.com/)

---

**For support or questions, contact the development team or raise an issue on GitHub.**
