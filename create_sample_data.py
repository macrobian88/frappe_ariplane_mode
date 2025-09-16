#!/usr/bin/env python3
"""
Sample Data Generator for Airplane Mode App
This script creates sample data for testing the Airport Management System
"""

import frappe
import json
from datetime import datetime, timedelta
import random


def create_sample_data():
    """Create comprehensive sample data for the Airplane Mode app"""
    
    # Create sample airlines
    create_sample_airlines()
    
    # Create sample airports
    create_sample_airports()
    
    # Create sample airplanes
    create_sample_airplanes()
    
    # Create sample shop types
    create_sample_shop_types()
    
    # Create sample airport shops
    create_sample_airport_shops()
    
    # Create sample tenants
    create_sample_tenants()
    
    # Create sample flight data
    create_sample_flights()
    
    print("✅ Sample data creation completed successfully!")


def create_sample_airlines():
    """Create sample airline records"""
    airlines = [
        {"airline_name": "Sky Airways", "website": "https://skyairways.com", "country": "United States"},
        {"airline_name": "Eagle Airlines", "website": "https://eagleair.com", "country": "United Kingdom"},
        {"airline_name": "Global Wings", "website": "https://globalwings.com", "country": "Canada"},
        {"airline_name": "Ocean Air", "website": "https://oceanair.com", "country": "Australia"},
        {"airline_name": "Mountain Express", "website": "https://mountainexpress.com", "country": "India"},
    ]
    
    for airline_data in airlines:
        if not frappe.db.exists("Airline", airline_data["airline_name"]):
            airline = frappe.get_doc({
                "doctype": "Airline",
                **airline_data
            })
            airline.insert()
            print(f"Created airline: {airline_data['airline_name']}")


def create_sample_airports():
    """Create sample airport records"""
    airports = [
        {"airport_name": "John F. Kennedy International Airport", "city": "New York", "country": "United States", "code": "JFK"},
        {"airport_name": "Heathrow Airport", "city": "London", "country": "United Kingdom", "code": "LHR"},
        {"airport_name": "Toronto Pearson International Airport", "city": "Toronto", "country": "Canada", "code": "YYZ"},
        {"airport_name": "Sydney Kingsford Smith Airport", "city": "Sydney", "country": "Australia", "code": "SYD"},
        {"airport_name": "Indira Gandhi International Airport", "city": "New Delhi", "country": "India", "code": "DEL"},
        {"airport_name": "Los Angeles International Airport", "city": "Los Angeles", "country": "United States", "code": "LAX"},
        {"airport_name": "Dubai International Airport", "city": "Dubai", "country": "UAE", "code": "DXB"},
    ]
    
    for airport_data in airports:
        if not frappe.db.exists("Airport", airport_data["airport_name"]):
            airport = frappe.get_doc({
                "doctype": "Airport",
                **airport_data
            })
            airport.insert()
            print(f"Created airport: {airport_data['airport_name']}")


def create_sample_airplanes():
    """Create sample airplane records"""
    # Get existing airlines
    airlines = frappe.get_all("Airline", fields=["name"])
    
    if not airlines:
        print("⚠️  No airlines found. Please create airlines first.")
        return
    
    airplanes = [
        {"model": "Boeing 737-800", "capacity": 162},
        {"model": "Airbus A320", "capacity": 150},
        {"model": "Boeing 777-300ER", "capacity": 396},
        {"model": "Airbus A350-900", "capacity": 315},
        {"model": "Boeing 787-9", "capacity": 290},
        {"model": "Airbus A380", "capacity": 525},
    ]
    
    for i, airplane_data in enumerate(airplanes):
        # Assign airline in round-robin fashion
        airline = airlines[i % len(airlines)]["name"]
        
        airplane_name = f"{airline}-{airplane_data['model']}-{i+1:03d}"
        
        if not frappe.db.exists("Airplane", airplane_name):
            airplane = frappe.get_doc({
                "doctype": "Airplane",
                "airplane": airplane_name,
                "airline": airline,
                **airplane_data
            })
            airplane.insert()
            print(f"Created airplane: {airplane_name}")


def create_sample_shop_types():
    """Create sample shop type records"""
    shop_types = [
        {"name": "Restaurant", "description": "Food and dining establishments"},
        {"name": "Retail Store", "description": "General merchandise and goods"},
        {"name": "Duty Free", "description": "Tax-free shopping for travelers"},
        {"name": "Coffee Shop", "description": "Coffee and light refreshments"},
        {"name": "Electronics", "description": "Electronic devices and accessories"},
        {"name": "Bookstore", "description": "Books, magazines, and reading materials"},
        {"name": "Pharmacy", "description": "Medical supplies and health products"},
        {"name": "Car Rental", "description": "Vehicle rental services"},
    ]
    
    for shop_type_data in shop_types:
        if not frappe.db.exists("Shop Type", shop_type_data["name"]):
            shop_type = frappe.get_doc({
                "doctype": "Shop Type",
                **shop_type_data
            })
            shop_type.insert()
            print(f"Created shop type: {shop_type_data['name']}")


def create_sample_airport_shops():
    """Create sample airport shop records"""
    # Get existing airports and shop types
    airports = frappe.get_all("Airport", fields=["name"])
    shop_types = frappe.get_all("Shop Type", fields=["name"])
    
    if not airports or not shop_types:
        print("⚠️  No airports or shop types found. Please create them first.")
        return
    
    shop_templates = [
        {"name": "Starbucks Coffee", "area": 800, "rent": 15000},
        {"name": "Hudson News", "area": 600, "rent": 12000},
        {"name": "McDonald's", "area": 1200, "rent": 25000},
        {"name": "Duty Free Americas", "area": 2000, "rent": 40000},
        {"name": "Apple Store", "area": 1500, "rent": 35000},
        {"name": "Walgreens Pharmacy", "area": 900, "rent": 18000},
        {"name": "Hertz Car Rental", "area": 500, "rent": 10000},
        {"name": "Barnes & Noble", "area": 1100, "rent": 20000},
    ]
    
    for airport in airports[:3]:  # Create shops for first 3 airports
        for i, shop_template in enumerate(shop_templates):
            shop_number = f"S{i+1:03d}"
            shop_type = shop_types[i % len(shop_types)]["name"]
            
            # Add some random variation to rent
            base_rent = shop_template["rent"]
            rent_variation = random.uniform(0.8, 1.2)
            final_rent = round(base_rent * rent_variation, 2)
            
            # Random contract end date (1-3 years from now)
            contract_end = datetime.now() + timedelta(days=random.randint(365, 1095))
            
            shop_name = f"{shop_template['name']} - {airport['name'][:20]}"
            
            if not frappe.db.exists("Airport Shop", {"shop_name": shop_name}):
                airport_shop = frappe.get_doc({
                    "doctype": "Airport Shop",
                    "shop_name": shop_name,
                    "shop_number": shop_number,
                    "airport": airport["name"],
                    "shop_type": shop_type,
                    "area_sq_feet": shop_template["area"],
                    "rent_amount": final_rent,
                    "contract_end_date": contract_end.strftime("%Y-%m-%d"),
                    "is_occupied": random.choice([0, 1])
                })
                airport_shop.insert()
                print(f"Created airport shop: {shop_name}")


def create_sample_tenants():
    """Create sample tenant records"""
    tenants = [
        {
            "tenant_name": "Starbucks Corporation",
            "contact_person": "John Smith",
            "email": "john.smith@starbucks.com",
            "phone": "+1-555-0101"
        },
        {
            "tenant_name": "Hudson Group",
            "contact_person": "Sarah Johnson",
            "email": "sarah.j@hudsongroup.com",
            "phone": "+1-555-0102"
        },
        {
            "tenant_name": "McDonald's USA",
            "contact_person": "Mike Davis",
            "email": "mike.davis@mcdonalds.com",
            "phone": "+1-555-0103"
        },
        {
            "tenant_name": "Duty Free Americas",
            "contact_person": "Emma Wilson",
            "email": "emma.wilson@dfa.com",
            "phone": "+1-555-0104"
        },
        {
            "tenant_name": "Apple Inc.",
            "contact_person": "David Chen",
            "email": "david.chen@apple.com",
            "phone": "+1-555-0105"
        }
    ]
    
    for tenant_data in tenants:
        if not frappe.db.exists("Tenant", tenant_data["tenant_name"]):
            tenant = frappe.get_doc({
                "doctype": "Tenant",
                **tenant_data
            })
            tenant.insert()
            print(f"Created tenant: {tenant_data['tenant_name']}")


def create_sample_flights():
    """Create sample flight records"""
    # Get existing data
    airlines = frappe.get_all("Airline", fields=["name"])
    airports = frappe.get_all("Airport", fields=["name"])
    airplanes = frappe.get_all("Airplane", fields=["name"])
    
    if not airlines or not airports or not airplanes:
        print("⚠️  Missing required data for flights. Skipping flight creation.")
        return
    
    # Create some sample flights
    flight_routes = [
        ("John F. Kennedy International Airport", "Heathrow Airport"),
        ("Los Angeles International Airport", "Tokyo Haneda Airport"),
        ("Dubai International Airport", "Indira Gandhi International Airport"),
        ("Toronto Pearson International Airport", "Sydney Kingsford Smith Airport"),
    ]
    
    for i, (source, destination) in enumerate(flight_routes):
        if frappe.db.exists("Airport", source) and frappe.db.exists("Airport", destination):
            airline = airlines[i % len(airlines)]["name"]
            airplane = airplanes[i % len(airplanes)]["name"]
            
            # Create departure and arrival times
            departure_time = datetime.now() + timedelta(days=random.randint(1, 30), hours=random.randint(6, 20))
            duration_hours = random.randint(3, 14)
            arrival_time = departure_time + timedelta(hours=duration_hours)
            
            flight_number = f"{airline[:2].upper()}{random.randint(100, 999)}"
            
            if not frappe.db.exists("Airplane Flight", flight_number):
                flight = frappe.get_doc({
                    "doctype": "Airplane Flight",
                    "flight": flight_number,
                    "airline": airline,
                    "airplane": airplane,
                    "source_airport": source,
                    "destination_airport": destination,
                    "departure_date": departure_time.strftime("%Y-%m-%d"),
                    "departure_time": departure_time.strftime("%H:%M:%S"),
                    "arrival_time": arrival_time.strftime("%H:%M:%S"),
                    "status": random.choice(["Scheduled", "Boarding", "Departed", "Arrived"])
                })
                flight.insert()
                print(f"Created flight: {flight_number}")


def main():
    """Main function to run the sample data creation"""
    print("🚀 Starting sample data creation for Airplane Mode app...")
    print("=" * 60)
    
    try:
        create_sample_data()
        frappe.db.commit()
        print("=" * 60)
        print("🎉 All sample data has been created successfully!")
        print("\nYou can now:")
        print("1. Browse Airport Shops in the system")
        print("2. Create Shop Lease Contracts")
        print("3. Test the search functionality")
        print("4. Explore all the sample data created")
        
    except Exception as e:
        frappe.db.rollback()
        print(f"❌ Error creating sample data: {str(e)}")
        print("Rolling back all changes...")


if __name__ == "__main__":
    # This script should be run within Frappe context
    # Example: bench execute airplane_mode.create_sample_data
    main()
