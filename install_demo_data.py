#!/usr/bin/env python3
"""
Airplane Mode Demo Data Installation Script
This script installs comprehensive demo data for the Airport Management System
"""

import frappe
import json
from datetime import datetime, timedelta
import random


def install_demo_data():
    """Main function to install all demo data"""
    
    print("🚀 Starting Airplane Mode demo data installation...")
    print("=" * 60)
    
    try:
        # Install in proper order due to dependencies
        install_airlines()
        install_airports()
        install_airplanes()
        install_shop_types()
        install_airport_shops()
        install_customers()
        install_tenants()
        
        # Commit all changes
        frappe.db.commit()
        
        print("=" * 60)
        print("🎉 Demo data installation completed successfully!")
        print("\n📊 Summary of created records:")
        print_summary()
        
        print("\n✅ Next steps:")
        print("1. Access the 'Airport Shop Management' workspace")
        print("2. Explore the demo data and test functionality")
        print("3. Create Shop Lease Contracts using the available shops")
        print("4. Review reports and analytics in the workspace")
        
    except Exception as e:
        frappe.db.rollback()
        print(f"❌ Error installing demo data: {str(e)}")
        print("🔄 Rolling back all changes...")
        raise


def install_airlines():
    """Install sample airlines"""
    print("✈️  Installing Airlines...")
    
    airlines = [
        {
            "name": "Sky Airways",
            "website": "https://skyairways.com",
            "headquarters": "Seattle, Washington",
            "founding_year": 1985,
            "customer_care_number": "+1-800-759-9297"
        },
        {
            "name": "Global Wings",
            "website": "https://globalwings.ca",
            "headquarters": "Toronto, Canada",
            "founding_year": 1992,
            "customer_care_number": "+1-877-456-7890"
        },
        {
            "name": "Ocean Air",
            "website": "https://oceanair.com.au",
            "headquarters": "Sydney, Australia",
            "founding_year": 1988,
            "customer_care_number": "+61-2-9876-5432"
        }
    ]
    
    for airline_data in airlines:
        if not frappe.db.exists("Airline", airline_data["name"]):
            airline = frappe.get_doc({
                "doctype": "Airline",
                **airline_data
            })
            airline.insert()
            print(f"   ✓ Created airline: {airline_data['name']}")


def install_airports():
    """Install sample airports"""
    print("🏢 Installing Airports...")
    
    airports = [
        {"airport_name": "Dubai International Airport", "city": "Dubai", "country": "UAE", "code": "DXB"},
        {"airport_name": "Singapore Changi Airport", "city": "Singapore", "country": "Singapore", "code": "SIN"},
        {"airport_name": "Frankfurt Airport", "city": "Frankfurt", "country": "Germany", "code": "FRA"},
        {"airport_name": "Tokyo Haneda Airport", "city": "Tokyo", "country": "Japan", "code": "HND"},
        {"airport_name": "Mumbai Airport", "city": "Mumbai", "country": "India", "code": "BOM"}
    ]
    
    for airport_data in airports:
        # Check if airport already exists by name or code
        if not frappe.db.exists("Airport", {"airport_name": airport_data["airport_name"]}) and \
           not frappe.db.exists("Airport", {"code": airport_data["code"]}):
            airport = frappe.get_doc({
                "doctype": "Airport",
                **airport_data
            })
            airport.insert()
            print(f"   ✓ Created airport: {airport_data['airport_name']} ({airport_data['code']})")


def install_airplanes():
    """Install sample airplanes"""
    print("✈️  Installing Airplanes...")
    
    # Get existing airlines
    airlines = frappe.get_all("Airline", fields=["name"])
    
    if not airlines:
        print("   ⚠️  No airlines found. Skipping airplane creation.")
        return
    
    airplane_models = [
        {"model": "Boeing 737-800", "capacity": 172},
        {"model": "Airbus A320", "capacity": 150},
        {"model": "Boeing 787-9", "capacity": 290},
        {"model": "Airbus A350-900", "capacity": 315},
        {"model": "Boeing 777-300ER", "capacity": 396},
        {"model": "Airbus A380-800", "capacity": 615},
        {"model": "Boeing 747-8", "capacity": 469},
        {"model": "Airbus A321neo", "capacity": 185}
    ]
    
    created_count = 0
    for i, airplane_data in enumerate(airplane_models):
        if created_count >= 5:  # Limit to 5 new airplanes
            break
            
        # Assign airline in round-robin fashion
        airline = airlines[i % len(airlines)]["name"]
        
        airplane = frappe.get_doc({
            "doctype": "Airplane",
            "model": airplane_data["model"],
            "airline": airline,
            "capacity": airplane_data["capacity"],
            "initial_audit_completed": random.choice([0, 1])
        })
        airplane.insert()
        print(f"   ✓ Created airplane: {airplane.name}")
        created_count += 1


def install_shop_types():
    """Install sample shop types"""
    print("🏪 Installing Shop Types...")
    
    shop_types = [
        {"type_name": "Premium Restaurant", "enabled": 1},
        {"type_name": "Fast Food", "enabled": 1},
        {"type_name": "Coffee & Beverages", "enabled": 1},
        {"type_name": "Luxury Duty Free", "enabled": 1},
        {"type_name": "Electronics & Tech", "enabled": 1},
        {"type_name": "Books & Magazines", "enabled": 1},
        {"type_name": "Health & Pharmacy", "enabled": 1},
        {"type_name": "Fashion & Accessories", "enabled": 1},
        {"type_name": "Convenience Store", "enabled": 1},
        {"type_name": "Car Rental", "enabled": 1}
    ]
    
    for shop_type_data in shop_types:
        # Check if shop type already exists
        if not frappe.db.exists("Shop Type", {"type_name": shop_type_data["type_name"]}):
            shop_type = frappe.get_doc({
                "doctype": "Shop Type",
                **shop_type_data
            })
            shop_type.insert()
            print(f"   ✓ Created shop type: {shop_type_data['type_name']}")


def install_airport_shops():
    """Install sample airport shops"""
    print("🛍️  Installing Airport Shops...")
    
    # Get existing data
    airports = frappe.get_all("Airport", fields=["name", "airport_name", "code"])
    shop_types = frappe.get_all("Shop Type", fields=["name", "type_name"])
    
    if not airports or not shop_types:
        print("   ⚠️  Missing airports or shop types. Skipping shop creation.")
        return
    
    # Shop templates with realistic data
    shop_templates = [
        {"name": "Starbucks Reserve", "type_filter": "Coffee", "area": 850, "rent": 18000},
        {"name": "McDonald's Express", "type_filter": "Fast Food", "area": 1200, "rent": 25000},
        {"name": "Premium Duty Free", "type_filter": "Duty Free", "area": 2500, "rent": 45000},
        {"name": "Apple Store", "type_filter": "Electronics", "area": 1800, "rent": 38000},
        {"name": "WHSmith Travel", "type_filter": "Books", "area": 600, "rent": 12000},
        {"name": "Boots Pharmacy", "type_filter": "Pharmacy", "area": 900, "rent": 20000},
        {"name": "Hugo Boss", "type_filter": "Fashion", "area": 1100, "rent": 28000},
        {"name": "7-Eleven", "type_filter": "Convenience", "area": 500, "rent": 10000},
        {"name": "Hertz Car Rental", "type_filter": "Car Rental", "area": 400, "rent": 8000},
        {"name": "Five Guys Burgers", "type_filter": "Restaurant", "area": 1000, "rent": 22000}
    ]
    
    created_count = 0
    for i, airport in enumerate(airports[:4]):  # Use first 4 airports
        for j, shop_template in enumerate(shop_templates[:6]):  # 6 shops per airport
            if created_count >= 20:  # Limit total shops
                break
                
            # Find appropriate shop type
            shop_type = None
            for st in shop_types:
                if shop_template["type_filter"].lower() in st["type_name"].lower():
                    shop_type = st["name"]
                    break
            
            if not shop_type:
                shop_type = shop_types[j % len(shop_types)]["name"]
            
            # Generate shop data
            shop_number = f"T{i+1}-S{j+1:03d}"
            rent_variation = random.uniform(0.8, 1.2)
            final_rent = round(shop_template["rent"] * rent_variation, 2)
            
            # Random contract end date (6 months to 3 years from now)
            contract_end = datetime.now() + timedelta(days=random.randint(180, 1095))
            
            shop_name = f"{shop_template['name']} {airport['code']}"
            
            # Check if shop already exists
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
                print(f"   ✓ Created shop: {shop_name}")
                created_count += 1


def install_customers():
    """Install sample customers"""
    print("👥 Installing Customers...")
    
    customers = [
        {"customer_name": "Starbucks Corporation", "customer_type": "Company"},
        {"customer_name": "McDonald's Corporation", "customer_type": "Company"},
        {"customer_name": "Apple Retail Inc.", "customer_type": "Company"},
        {"customer_name": "WHSmith PLC", "customer_type": "Company"},
        {"customer_name": "Boots UK Limited", "customer_type": "Company"},
        {"customer_name": "Hugo Boss AG", "customer_type": "Company"},
        {"customer_name": "Seven & I Holdings", "customer_type": "Company"},
        {"customer_name": "Hertz Corporation", "customer_type": "Company"}
    ]
    
    for customer_data in customers:
        if not frappe.db.exists("Customer", customer_data["customer_name"]):
            customer = frappe.get_doc({
                "doctype": "Customer",
                **customer_data
            })
            customer.insert()
            print(f"   ✓ Created customer: {customer_data['customer_name']}")


def install_tenants():
    """Install sample tenants"""
    print("🏢 Installing Tenants...")
    
    # Get data for tenant creation
    airport_shops = frappe.get_all("Airport Shop", 
                                 filters={"is_occupied": 1}, 
                                 fields=["name", "shop_name"], 
                                 limit=8)
    customers = frappe.get_all("Customer", fields=["name"])
    
    if not airport_shops or not customers:
        print("   ⚠️  Missing occupied shops or customers. Skipping tenant creation.")
        return
    
    tenant_emails = [
        "operations@starbucks.com",
        "leasing@mcdonalds.com",
        "retail@apple.com",
        "travel@whsmith.com",
        "stores@boots.com",
        "retail@hugoboss.com",
        "franchising@7eleven.com",
        "locations@hertz.com"
    ]
    
    for i, shop in enumerate(airport_shops):
        if i >= len(customers) or i >= len(tenant_emails):
            break
            
        customer = customers[i]["name"]
        email = tenant_emails[i]
        
        # Generate realistic contract dates
        start_date = datetime.now() - timedelta(days=random.randint(30, 730))
        end_date = start_date + timedelta(days=random.randint(365, 1095))
        
        # Check if tenant already exists for this shop
        if not frappe.db.exists("Tenant", {"shop": shop["name"]}):
            tenant = frappe.get_doc({
                "doctype": "Tenant",
                "shop": shop["name"],
                "email": email,
                "customer": customer,
                "contract_start_date": start_date.strftime("%Y-%m-%d"),
                "contract_end_date": end_date.strftime("%Y-%m-%d")
            })
            tenant.insert()
            print(f"   ✓ Created tenant: {customer} for {shop['shop_name']}")


def print_summary():
    """Print summary of created records"""
    
    # Count records
    airlines_count = frappe.db.count("Airline")
    airports_count = frappe.db.count("Airport")
    airplanes_count = frappe.db.count("Airplane")
    shop_types_count = frappe.db.count("Shop Type")
    airport_shops_count = frappe.db.count("Airport Shop")
    customers_count = frappe.db.count("Customer")
    tenants_count = frappe.db.count("Tenant")
    
    # Occupancy stats
    occupied_shops = frappe.db.count("Airport Shop", {"is_occupied": 1})
    vacant_shops = frappe.db.count("Airport Shop", {"is_occupied": 0})
    
    print(f"   Airlines: {airlines_count}")
    print(f"   Airports: {airports_count}")
    print(f"   Airplanes: {airplanes_count}")
    print(f"   Shop Types: {shop_types_count}")
    print(f"   Airport Shops: {airport_shops_count} (Occupied: {occupied_shops}, Vacant: {vacant_shops})")
    print(f"   Customers: {customers_count}")
    print(f"   Tenants: {tenants_count}")


def cleanup_demo_data():
    """Remove all demo data (use with caution!)"""
    print("🗑️  WARNING: This will remove ALL demo data!")
    response = input("Are you sure you want to continue? (type 'DELETE' to confirm): ")
    
    if response != "DELETE":
        print("Operation cancelled.")
        return
    
    print("Removing demo data...")
    
    # Remove in reverse dependency order
    frappe.db.delete("Tenant")
    frappe.db.delete("Airport Shop")
    frappe.db.delete("Shop Type")
    frappe.db.delete("Airplane")
    frappe.db.delete("Airport", {"code": ["in", ["DXB", "SIN", "FRA", "HND", "BOM"]]})
    frappe.db.delete("Airline", {"name": ["in", ["Sky Airways", "Global Wings", "Ocean Air"]]})
    frappe.db.delete("Customer", {"customer_type": "Company"})
    
    frappe.db.commit()
    print("✅ Demo data removed successfully.")


def main():
    """Main execution function"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--cleanup":
        cleanup_demo_data()
    else:
        install_demo_data()


if __name__ == "__main__":
    # This script should be run within Frappe context
    # Example: bench execute airplane_mode.install_demo_data --args "--install"
    main()
