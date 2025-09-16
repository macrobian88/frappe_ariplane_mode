#!/usr/bin/env python3
"""
Bulk Sample Data Generator for Airplane Mode App
This script creates comprehensive bulk sample data for a fully populated Airport Management System
"""

import frappe
import json
from datetime import datetime, timedelta
import random
import string


def create_bulk_sample_data():
    """Create comprehensive bulk sample data for the Airplane Mode app"""
    
    print("🚀 Starting bulk sample data creation for Airplane Mode app...")
    print("=" * 70)
    
    try:
        # Create data in proper dependency order
        create_bulk_airlines()
        create_bulk_airports()
        create_bulk_airplanes()
        create_bulk_shop_types()
        create_bulk_airport_shops()
        create_bulk_passengers()
        create_bulk_flights()
        create_bulk_tenants()
        create_bulk_customers()
        
        # Commit all changes
        frappe.db.commit()
        
        print("=" * 70)
        print("🎉 Bulk sample data creation completed successfully!")
        print("\n📊 Final Summary:")
        print_comprehensive_summary()
        
        print("\n✅ Your Airplane Mode workspace is now fully populated!")
        print("🔍 Check the dashboard to see all the new data counts.")
        
    except Exception as e:
        frappe.db.rollback()
        print(f"❌ Error creating bulk sample data: {str(e)}")
        print("🔄 Rolling back all changes...")
        raise


def create_bulk_airlines():
    """Create a comprehensive list of airlines"""
    print("✈️  Creating Bulk Airlines (Target: 15+ airlines)...")
    
    airlines = [
        {"airline_name": "Sky Airways International", "website": "https://skyairways.com", "country": "United States", "headquarters": "Seattle, WA"},
        {"airline_name": "Global Wings Express", "website": "https://globalwings.com", "country": "Canada", "headquarters": "Toronto, ON"},
        {"airline_name": "Ocean Air Pacific", "website": "https://oceanair.com", "country": "Australia", "headquarters": "Sydney, NSW"},
        {"airline_name": "Mountain Express Airlines", "website": "https://mountainexpress.com", "country": "India", "headquarters": "Mumbai, MH"},
        {"airline_name": "Eagle Airlines Europe", "website": "https://eagleair.eu", "country": "United Kingdom", "headquarters": "London, UK"},
        {"airline_name": "Phoenix Airways", "website": "https://phoenixair.com", "country": "Germany", "headquarters": "Frankfurt, DE"},
        {"airline_name": "Dragon Flight Services", "website": "https://dragonfly.com", "country": "Singapore", "headquarters": "Singapore, SG"},
        {"airline_name": "Falcon International", "website": "https://falconintl.com", "country": "UAE", "headquarters": "Dubai, UAE"},
        {"airline_name": "Swift Air Transport", "website": "https://swiftair.com", "country": "Japan", "headquarters": "Tokyo, JP"},
        {"airline_name": "Horizon Airlines", "website": "https://horizonair.com", "country": "France", "headquarters": "Paris, FR"},
        {"airline_name": "Summit Airways", "website": "https://summitair.com", "country": "Switzerland", "headquarters": "Zurich, CH"},
        {"airline_name": "Thunder Airlines", "website": "https://thunderair.com", "country": "Brazil", "headquarters": "São Paulo, BR"},
        {"airline_name": "Lightning Express", "website": "https://lightningexp.com", "country": "South Korea", "headquarters": "Seoul, KR"},
        {"airline_name": "Storm Air Services", "website": "https://stormair.com", "country": "Netherlands", "headquarters": "Amsterdam, NL"},
        {"airline_name": "Breeze Airlines", "website": "https://breezeair.com", "country": "Italy", "headquarters": "Rome, IT"},
        {"airline_name": "Velocity Air", "website": "https://velocityair.com", "country": "Spain", "headquarters": "Madrid, ES"},
    ]
    
    created_count = 0
    for airline_data in airlines:
        if not frappe.db.exists("Airline", airline_data["airline_name"]):
            airline = frappe.get_doc({
                "doctype": "Airline",
                **airline_data
            })
            airline.insert()
            created_count += 1
            print(f"   ✓ Created airline: {airline_data['airline_name']}")
    
    print(f"   📊 Total airlines created: {created_count}")


def create_bulk_airports():
    """Create a comprehensive list of international airports"""
    print("🏢 Creating Bulk Airports (Target: 25+ airports)...")
    
    airports = [
        # Major International Hubs
        {"airport_name": "Dubai International Airport", "city": "Dubai", "country": "UAE", "code": "DXB"},
        {"airport_name": "Singapore Changi Airport", "city": "Singapore", "country": "Singapore", "code": "SIN"},
        {"airport_name": "Tokyo Haneda Airport", "city": "Tokyo", "country": "Japan", "code": "HND"},
        {"airport_name": "London Heathrow Airport", "city": "London", "country": "United Kingdom", "code": "LHR"},
        {"airport_name": "Frankfurt Airport", "city": "Frankfurt", "country": "Germany", "code": "FRA"},
        
        # Americas
        {"airport_name": "John F. Kennedy International Airport", "city": "New York", "country": "United States", "code": "JFK"},
        {"airport_name": "Los Angeles International Airport", "city": "Los Angeles", "country": "United States", "code": "LAX"},
        {"airport_name": "Toronto Pearson International Airport", "city": "Toronto", "country": "Canada", "code": "YYZ"},
        {"airport_name": "São Paulo–Guarulhos International Airport", "city": "São Paulo", "country": "Brazil", "code": "GRU"},
        {"airport_name": "Mexico City International Airport", "city": "Mexico City", "country": "Mexico", "code": "MEX"},
        
        # Europe
        {"airport_name": "Charles de Gaulle Airport", "city": "Paris", "country": "France", "code": "CDG"},
        {"airport_name": "Amsterdam Airport Schiphol", "city": "Amsterdam", "country": "Netherlands", "code": "AMS"},
        {"airport_name": "Zurich Airport", "city": "Zurich", "country": "Switzerland", "code": "ZUR"},
        {"airport_name": "Rome Fiumicino Airport", "city": "Rome", "country": "Italy", "code": "FCO"},
        {"airport_name": "Madrid–Barajas Airport", "city": "Madrid", "country": "Spain", "code": "MAD"},
        
        # Asia Pacific
        {"airport_name": "Beijing Capital International Airport", "city": "Beijing", "country": "China", "code": "PEK"},
        {"airport_name": "Incheon International Airport", "city": "Seoul", "country": "South Korea", "code": "ICN"},
        {"airport_name": "Sydney Kingsford Smith Airport", "city": "Sydney", "country": "Australia", "code": "SYD"},
        {"airport_name": "Mumbai Chhatrapati Shivaji Airport", "city": "Mumbai", "country": "India", "code": "BOM"},
        {"airport_name": "Indira Gandhi International Airport", "city": "New Delhi", "country": "India", "code": "DEL"},
        
        # Additional Major Airports
        {"airport_name": "Hong Kong International Airport", "city": "Hong Kong", "country": "Hong Kong", "code": "HKG"},
        {"airport_name": "Bangkok Suvarnabhumi Airport", "city": "Bangkok", "country": "Thailand", "code": "BKK"},
        {"airport_name": "Istanbul Airport", "city": "Istanbul", "country": "Turkey", "code": "IST"},
        {"airport_name": "Doha Hamad International Airport", "city": "Doha", "country": "Qatar", "code": "DOH"},
        {"airport_name": "Cape Town International Airport", "city": "Cape Town", "country": "South Africa", "code": "CPT"},
        {"airport_name": "Miami International Airport", "city": "Miami", "country": "United States", "code": "MIA"},
    ]
    
    created_count = 0
    for airport_data in airports:
        # Check if airport exists by name or code
        if not frappe.db.exists("Airport", {"airport_name": airport_data["airport_name"]}) and \
           not frappe.db.exists("Airport", {"code": airport_data["code"]}):
            airport = frappe.get_doc({
                "doctype": "Airport",
                **airport_data
            })
            airport.insert()
            created_count += 1
            print(f"   ✓ Created airport: {airport_data['airport_name']} ({airport_data['code']})")
    
    print(f"   📊 Total airports created: {created_count}")


def create_bulk_airplanes():
    """Create a large fleet of airplanes"""
    print("✈️  Creating Bulk Airplanes (Target: 50+ airplanes)...")
    
    # Get all airlines
    airlines = frappe.get_all("Airline", fields=["name"])
    if not airlines:
        print("   ⚠️  No airlines found. Skipping airplane creation.")
        return
    
    airplane_models = [
        {"model": "Boeing 737-800", "capacity": 162},
        {"model": "Boeing 737-900", "capacity": 180},
        {"model": "Airbus A320", "capacity": 150},
        {"model": "Airbus A321", "capacity": 185},
        {"model": "Boeing 787-8", "capacity": 242},
        {"model": "Boeing 787-9", "capacity": 290},
        {"model": "Boeing 787-10", "capacity": 330},
        {"model": "Airbus A350-900", "capacity": 315},
        {"model": "Airbus A350-1000", "capacity": 366},
        {"model": "Boeing 777-200ER", "capacity": 314},
        {"model": "Boeing 777-300ER", "capacity": 396},
        {"model": "Boeing 747-8", "capacity": 467},
        {"model": "Airbus A380", "capacity": 525},
        {"model": "Boeing 767-300ER", "capacity": 218},
        {"model": "Airbus A330-300", "capacity": 295},
        {"model": "Airbus A340-600", "capacity": 380},
        {"model": "Embraer E175", "capacity": 88},
        {"model": "Bombardier CRJ-900", "capacity": 90},
        {"model": "ATR 72-600", "capacity": 78},
        {"model": "Boeing 757-200", "capacity": 200},
    ]
    
    created_count = 0
    target_count = 55  # Create 55 airplanes
    
    for i in range(target_count):
        # Select random airline and model
        airline = random.choice(airlines)["name"]
        model_data = random.choice(airplane_models)
        
        # Generate unique airplane identifier
        airplane_id = f"{airline[:3].upper()}-{random.randint(1000, 9999)}"
        
        # Check if airplane already exists
        if not frappe.db.exists("Airplane", airplane_id):
            airplane = frappe.get_doc({
                "doctype": "Airplane",
                "airplane": airplane_id,
                "airline": airline,
                "model": model_data["model"],
                "capacity": model_data["capacity"]
            })
            airplane.insert()
            created_count += 1
            if created_count <= 10:  # Show first 10 for brevity
                print(f"   ✓ Created airplane: {airplane_id} ({model_data['model']})")
            elif created_count == 11:
                print(f"   ... creating more airplanes ...")
    
    print(f"   📊 Total airplanes created: {created_count}")


def create_bulk_shop_types():
    """Create comprehensive shop type categories"""
    print("🏪 Creating Bulk Shop Types...")
    
    shop_types = [
        {"type_name": "Premium Restaurant", "enabled": 1},
        {"type_name": "Fast Food Chain", "enabled": 1},
        {"type_name": "Coffee & Beverages", "enabled": 1},
        {"type_name": "Luxury Duty Free", "enabled": 1},
        {"type_name": "Electronics & Technology", "enabled": 1},
        {"type_name": "Books & Magazines", "enabled": 1},
        {"type_name": "Health & Pharmacy", "enabled": 1},
        {"type_name": "Fashion & Accessories", "enabled": 1},
        {"type_name": "Convenience Store", "enabled": 1},
        {"type_name": "Car Rental Services", "enabled": 1},
        {"type_name": "Jewelry & Watches", "enabled": 1},
        {"type_name": "Perfume & Cosmetics", "enabled": 1},
        {"type_name": "Souvenir Shop", "enabled": 1},
        {"type_name": "Currency Exchange", "enabled": 1},
        {"type_name": "Travel Accessories", "enabled": 1},
        {"type_name": "Sporting Goods", "enabled": 1},
        {"type_name": "Art Gallery", "enabled": 1},
        {"type_name": "Mobile Phone Services", "enabled": 1},
    ]
    
    created_count = 0
    for shop_type_data in shop_types:
        if not frappe.db.exists("Shop Type", {"type_name": shop_type_data["type_name"]}):
            shop_type = frappe.get_doc({
                "doctype": "Shop Type",
                **shop_type_data
            })
            shop_type.insert()
            created_count += 1
            print(f"   ✓ Created shop type: {shop_type_data['type_name']}")
    
    print(f"   📊 Total shop types created: {created_count}")


def create_bulk_airport_shops():
    """Create a large number of airport shops"""
    print("🛍️  Creating Bulk Airport Shops (Target: 100+ shops)...")
    
    # Get existing data
    airports = frappe.get_all("Airport", fields=["name", "airport_name", "code"])
    shop_types = frappe.get_all("Shop Type", fields=["name", "type_name"])
    
    if not airports or not shop_types:
        print("   ⚠️  Missing airports or shop types. Skipping shop creation.")
        return
    
    # Extended shop templates
    shop_brands = [
        # Restaurants & Food
        {"name": "McDonald's", "type_hint": "Fast Food", "area_range": (800, 1500), "rent_range": (20000, 35000)},
        {"name": "Burger King", "type_hint": "Fast Food", "area_range": (700, 1200), "rent_range": (18000, 30000)},
        {"name": "Starbucks", "type_hint": "Coffee", "area_range": (500, 900), "rent_range": (15000, 25000)},
        {"name": "Costa Coffee", "type_hint": "Coffee", "area_range": (400, 800), "rent_range": (12000, 20000)},
        {"name": "Pizza Hut", "type_hint": "Restaurant", "area_range": (900, 1400), "rent_range": (22000, 32000)},
        {"name": "Subway", "type_hint": "Fast Food", "area_range": (600, 1000), "rent_range": (14000, 24000)},
        
        # Retail & Shopping
        {"name": "Apple Store", "type_hint": "Electronics", "area_range": (1200, 2000), "rent_range": (35000, 55000)},
        {"name": "Samsung Experience", "type_hint": "Electronics", "area_range": (1000, 1800), "rent_range": (30000, 50000)},
        {"name": "WHSmith", "type_hint": "Books", "area_range": (500, 800), "rent_range": (10000, 18000)},
        {"name": "Hudson News", "type_hint": "Books", "area_range": (400, 700), "rent_range": (8000, 15000)},
        {"name": "Duty Free Shoppers", "type_hint": "Duty Free", "area_range": (2000, 4000), "rent_range": (40000, 80000)},
        {"name": "World Duty Free", "type_hint": "Duty Free", "area_range": (1800, 3500), "rent_range": (35000, 70000)},
        
        # Fashion & Accessories
        {"name": "Hugo Boss", "type_hint": "Fashion", "area_range": (800, 1500), "rent_range": (25000, 40000)},
        {"name": "Gucci", "type_hint": "Fashion", "area_range": (1000, 1800), "rent_range": (35000, 60000)},
        {"name": "Ray-Ban", "type_hint": "Accessories", "area_range": (300, 600), "rent_range": (12000, 22000)},
        {"name": "Swatch", "type_hint": "Jewelry", "area_range": (250, 500), "rent_range": (10000, 18000)},
        
        # Services
        {"name": "Hertz", "type_hint": "Car Rental", "area_range": (200, 500), "rent_range": (5000, 12000)},
        {"name": "Avis", "type_hint": "Car Rental", "area_range": (200, 500), "rent_range": (5000, 12000)},
        {"name": "Boots Pharmacy", "type_hint": "Pharmacy", "area_range": (600, 1200), "rent_range": (15000, 28000)},
        {"name": "7-Eleven", "type_hint": "Convenience", "area_range": (300, 800), "rent_range": (8000, 18000)},
        
        # Specialty Stores
        {"name": "Fossil", "type_hint": "Jewelry", "area_range": (400, 800), "rent_range": (15000, 25000)},
        {"name": "Sephora", "type_hint": "Cosmetics", "area_range": (800, 1500), "rent_range": (20000, 35000)},
        {"name": "Lego Store", "type_hint": "Souvenir", "area_range": (600, 1000), "rent_range": (18000, 28000)},
        {"name": "Victoria's Secret", "type_hint": "Fashion", "area_range": (700, 1300), "rent_range": (22000, 38000)},
    ]
    
    created_count = 0
    target_count = 120
    
    # Create shops across airports
    for airport in airports:
        shops_per_airport = random.randint(3, 8)  # 3-8 shops per airport
        
        for i in range(shops_per_airport):
            if created_count >= target_count:
                break
                
            # Select random shop brand
            brand = random.choice(shop_brands)
            
            # Find appropriate shop type
            shop_type = None
            for st in shop_types:
                if brand["type_hint"].lower() in st["type_name"].lower():
                    shop_type = st["name"]
                    break
            
            if not shop_type:
                shop_type = random.choice(shop_types)["name"]
            
            # Generate shop data
            terminal = random.choice(['T1', 'T2', 'T3', 'A', 'B', 'C'])
            gate_area = random.choice(['North', 'South', 'East', 'West', 'Central'])
            shop_number = f"{terminal}-{gate_area}-{random.randint(1, 99):02d}"
            
            # Calculate area and rent
            min_area, max_area = brand["area_range"]
            area = random.randint(min_area, max_area)
            
            min_rent, max_rent = brand["rent_range"]
            base_rent = random.randint(min_rent, max_rent)
            
            # Add location premium for major airports
            if airport["code"] in ["DXB", "LHR", "JFK", "LAX", "SIN"]:
                base_rent = int(base_rent * 1.3)
            
            # Generate contract dates
            start_date = datetime.now() - timedelta(days=random.randint(1, 730))
            end_date = start_date + timedelta(days=random.randint(365, 1460))
            
            shop_name = f"{brand['name']} {airport['code']}"
            
            # Ensure unique shop names
            counter = 1
            original_name = shop_name
            while frappe.db.exists("Airport Shop", {"shop_name": shop_name}):
                shop_name = f"{original_name} #{counter}"
                counter += 1
            
            airport_shop = frappe.get_doc({
                "doctype": "Airport Shop",
                "shop_name": shop_name,
                "shop_number": shop_number,
                "airport": airport["name"],
                "shop_type": shop_type,
                "area_sq_feet": area,
                "rent_amount": base_rent,
                "contract_end_date": end_date.strftime("%Y-%m-%d"),
                "is_occupied": random.choices([0, 1], weights=[30, 70])[0]  # 70% occupancy
            })
            airport_shop.insert()
            created_count += 1
            
            if created_count <= 15:  # Show first 15 for brevity
                print(f"   ✓ Created shop: {shop_name}")
            elif created_count == 16:
                print(f"   ... creating more shops ...")
        
        if created_count >= target_count:
            break
    
    print(f"   📊 Total airport shops created: {created_count}")


def create_bulk_passengers():
    """Create passenger records"""
    print("👥 Creating Bulk Passengers (Target: 50+ passengers)...")
    
    first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Lisa", 
                   "James", "Maria", "William", "Jennifer", "Richard", "Patricia", "Charles",
                   "Linda", "Joseph", "Barbara", "Thomas", "Susan", "Christopher", "Jessica",
                   "Daniel", "Margaret", "Matthew", "Dorothy", "Anthony", "Nancy", "Donald",
                   "Helen", "Mark", "Betty", "Paul", "Ruth", "Steven", "Sharon", "Andrew"]
    
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
                  "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", 
                  "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
                  "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", 
                  "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King"]
    
    countries = ["United States", "United Kingdom", "Canada", "Australia", "Germany", 
                "France", "Japan", "South Korea", "Singapore", "Netherlands", "Switzerland",
                "Italy", "Spain", "India", "Brazil", "Mexico", "UAE", "South Africa"]
    
    created_count = 0
    target_count = 55
    
    for i in range(target_count):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        full_name = f"{first_name} {last_name}"
        
        # Generate date of birth (18-80 years old)
        birth_year = datetime.now().year - random.randint(18, 80)
        birth_date = datetime(birth_year, random.randint(1, 12), random.randint(1, 28))
        
        passenger_data = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": birth_date.strftime("%Y-%m-%d"),
            "nationality": random.choice(countries)
        }
        
        # Check if passenger already exists
        if not frappe.db.exists("Passenger", {"first_name": first_name, "last_name": last_name}):
            passenger = frappe.get_doc({
                "doctype": "Passenger",
                **passenger_data
            })
            passenger.insert()
            created_count += 1
            
            if created_count <= 10:  # Show first 10 for brevity
                print(f"   ✓ Created passenger: {full_name}")
            elif created_count == 11:
                print(f"   ... creating more passengers ...")
    
    print(f"   📊 Total passengers created: {created_count}")


def create_bulk_flights():
    """Create flight schedules"""
    print("✈️  Creating Bulk Flights (Target: 30+ flights)...")
    
    # Get existing data
    airlines = frappe.get_all("Airline", fields=["name"])
    airports = frappe.get_all("Airport", fields=["name", "code"])
    airplanes = frappe.get_all("Airplane", fields=["name"])
    
    if not airlines or not airports or not airplanes:
        print("   ⚠️  Missing required data for flights. Skipping flight creation.")
        return
    
    created_count = 0
    target_count = 35
    
    for i in range(target_count):
        # Select random source and destination (ensure they're different)
        source = random.choice(airports)
        destination = random.choice([a for a in airports if a["name"] != source["name"]])
        
        airline = random.choice(airlines)["name"]
        airplane = random.choice(airplanes)["name"]
        
        # Generate flight number
        airline_code = airline[:2].upper()
        flight_number = f"{airline_code}{random.randint(100, 9999)}"
        
        # Generate flight times
        departure_date = datetime.now() + timedelta(days=random.randint(-30, 90))
        departure_time = departure_date.replace(
            hour=random.randint(0, 23), 
            minute=random.choice([0, 15, 30, 45]),
            second=0,
            microsecond=0
        )
        
        # Flight duration based on rough distance estimation
        duration_hours = random.randint(1, 16)
        arrival_time = departure_time + timedelta(hours=duration_hours)
        
        status_options = ["Scheduled", "Boarding", "Departed", "Arrived", "Delayed", "Cancelled"]
        weights = [40, 10, 25, 20, 4, 1]  # Weighted probability
        status = random.choices(status_options, weights=weights)[0]
        
        # Check if flight already exists
        if not frappe.db.exists("Airplane Flight", flight_number):
            flight = frappe.get_doc({
                "doctype": "Airplane Flight",
                "flight": flight_number,
                "airline": airline,
                "airplane": airplane,
                "source_airport": source["name"],
                "destination_airport": destination["name"],
                "departure_date": departure_date.strftime("%Y-%m-%d"),
                "departure_time": departure_time.strftime("%H:%M:%S"),
                "arrival_time": arrival_time.strftime("%H:%M:%S"),
                "status": status
            })
            flight.insert()
            created_count += 1
            
            if created_count <= 10:  # Show first 10 for brevity
                print(f"   ✓ Created flight: {flight_number} ({source['code']} → {destination['code']})")
            elif created_count == 11:
                print(f"   ... creating more flights ...")
    
    print(f"   📊 Total flights created: {created_count}")


def create_bulk_tenants():
    """Create tenant records for occupied shops"""
    print("🏢 Creating Bulk Tenants...")
    
    # Get occupied shops
    occupied_shops = frappe.get_all("Airport Shop", 
                                  filters={"is_occupied": 1}, 
                                  fields=["name", "shop_name"],
                                  limit=30)
    
    if not occupied_shops:
        print("   ⚠️  No occupied shops found. Skipping tenant creation.")
        return
    
    tenant_companies = [
        "Starbucks Corporation", "McDonald's Corp", "Apple Retail Inc", "Samsung Electronics",
        "Hugo Boss AG", "Gucci Group", "L'Oréal Group", "Sephora", "Ray-Ban", "Fossil Group",
        "Hertz Corporation", "Avis Budget Group", "WHSmith PLC", "Hudson Group",
        "Duty Free Shoppers", "Walgreens Boots Alliance", "7-Eleven Inc", "Subway",
        "Burger King Corporation", "Pizza Hut LLC", "Costa Coffee", "Victoria's Secret"
    ]
    
    created_count = 0
    for i, shop in enumerate(occupied_shops):
        if i >= len(tenant_companies):
            break
            
        company = tenant_companies[i]
        
        # Generate realistic tenant data
        email_domain = company.lower().replace(" ", "").replace("corp", "").replace("inc", "").replace("llc", "").replace("plc", "").replace("ag", "").replace("group", "")[:10]
        email = f"leasing@{email_domain}.com"
        
        # Generate contract dates
        start_date = datetime.now() - timedelta(days=random.randint(30, 1000))
        end_date = start_date + timedelta(days=random.randint(365, 1825))  # 1-5 year contracts
        
        if not frappe.db.exists("Tenant", {"shop": shop["name"]}):
            tenant = frappe.get_doc({
                "doctype": "Tenant",
                "shop": shop["name"],
                "email": email,
                "customer": company,
                "contract_start_date": start_date.strftime("%Y-%m-%d"),
                "contract_end_date": end_date.strftime("%Y-%m-%d")
            })
            tenant.insert()
            created_count += 1
            print(f"   ✓ Created tenant: {company} for {shop['shop_name']}")
    
    print(f"   📊 Total tenants created: {created_count}")


def create_bulk_customers():
    """Create customer records"""
    print("👥 Creating Bulk Customers...")
    
    customers = [
        {"customer_name": "Starbucks Corporation", "customer_type": "Company"},
        {"customer_name": "McDonald's Corporation", "customer_type": "Company"},
        {"customer_name": "Apple Retail Inc.", "customer_type": "Company"},
        {"customer_name": "Samsung Electronics", "customer_type": "Company"},
        {"customer_name": "Hugo Boss AG", "customer_type": "Company"},
        {"customer_name": "Gucci Group", "customer_type": "Company"},
        {"customer_name": "L'Oréal International", "customer_type": "Company"},
        {"customer_name": "Sephora USA Inc.", "customer_type": "Company"},
        {"customer_name": "Ray-Ban International", "customer_type": "Company"},
        {"customer_name": "Fossil Group Inc.", "customer_type": "Company"},
        {"customer_name": "Hertz Corporation", "customer_type": "Company"},
        {"customer_name": "Avis Budget Group", "customer_type": "Company"},
        {"customer_name": "WHSmith PLC", "customer_type": "Company"},
        {"customer_name": "Hudson Group", "customer_type": "Company"},
        {"customer_name": "Duty Free Shoppers", "customer_type": "Company"},
        {"customer_name": "Walgreens Boots Alliance", "customer_type": "Company"},
        {"customer_name": "7-Eleven Inc.", "customer_type": "Company"},
        {"customer_name": "Subway Franchising LLC", "customer_type": "Company"},
        {"customer_name": "Burger King Corporation", "customer_type": "Company"},
        {"customer_name": "Pizza Hut LLC", "customer_type": "Company"}
    ]
    
    created_count = 0
    for customer_data in customers:
        if not frappe.db.exists("Customer", customer_data["customer_name"]):
            customer = frappe.get_doc({
                "doctype": "Customer",
                **customer_data
            })
            customer.insert()
            created_count += 1
            print(f"   ✓ Created customer: {customer_data['customer_name']}")
    
    print(f"   📊 Total customers created: {created_count}")


def print_comprehensive_summary():
    """Print detailed summary of all created records"""
    
    # Count all records
    airlines_count = frappe.db.count("Airline")
    airports_count = frappe.db.count("Airport")
    airplanes_count = frappe.db.count("Airplane")
    shop_types_count = frappe.db.count("Shop Type")
    airport_shops_count = frappe.db.count("Airport Shop")
    passengers_count = frappe.db.count("Passenger")
    flights_count = frappe.db.count("Airplane Flight")
    customers_count = frappe.db.count("Customer")
    tenants_count = frappe.db.count("Tenant")
    
    # Additional analytics
    occupied_shops = frappe.db.count("Airport Shop", {"is_occupied": 1})
    vacant_shops = frappe.db.count("Airport Shop", {"is_occupied": 0})
    
    print(f"   ✈️  Airlines: {airlines_count}")
    print(f"   🏢 Airports: {airports_count}")
    print(f"   🛩️  Airplanes: {airplanes_count}")
    print(f"   🏪 Shop Types: {shop_types_count}")
    print(f"   🛍️  Airport Shops: {airport_shops_count}")
    print(f"      • Occupied: {occupied_shops}")
    print(f"      • Vacant: {vacant_shops}")
    print(f"      • Occupancy Rate: {(occupied_shops/airport_shops_count*100):.1f}%")
    print(f"   👥 Passengers: {passengers_count}")
    print(f"   🛫 Flights: {flights_count}")
    print(f"   🏢 Customers: {customers_count}")
    print(f"   🏠 Tenants: {tenants_count}")


def main():
    """Main execution function"""
    print("🎯 Bulk Sample Data Generator for Airplane Mode")
    print("This will create substantial sample data to populate your workspace")
    print("=" * 70)
    
    response = input("Do you want to proceed? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("Operation cancelled.")
        return
    
    create_bulk_sample_data()


if __name__ == "__main__":
    # This script should be run within Frappe context
    # Example: bench execute airplane_mode.create_bulk_sample_data
    main()
