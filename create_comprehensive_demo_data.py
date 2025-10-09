#!/usr/bin/env python3
"""
Demo Data Creation Script for Airport Shop Management
This script creates comprehensive sample data for testing and demonstration
"""

import frappe
import random
from datetime import datetime, timedelta
from frappe.utils import today, add_months, add_days

def create_demo_data():
    """Create comprehensive demo data for Airport Shop Management"""
    print("🚀 Starting demo data creation...")
    
    # Clear existing demo data
    clear_demo_data()
    
    # Create in logical order due to dependencies
    create_shop_types()
    create_airports()
    create_airport_shops()
    create_tenants()
    create_shop_lease_contracts()
    create_monthly_invoices()
    create_rent_payment_contracts()
    create_shop_leads()
    
    print("✅ Demo data creation completed successfully!")


def clear_demo_data():
    """Clear existing demo data"""
    print("🧹 Clearing existing demo data...")
    
    doctypes_to_clear = [
        "Shop Lead",
        "Rent Payment Contract", 
        "Monthly Invoice",
        "Shop Lease Contract",
        "Tenant",
        "Airport Shop",
        "Shop Type"
    ]
    
    for doctype in doctypes_to_clear:
        try:
            # Delete all records of this doctype
            records = frappe.get_all(doctype)
            for record in records:
                frappe.delete_doc(doctype, record.name, force=True)
            print(f"   Cleared {len(records)} {doctype} records")
        except Exception as e:
            print(f"   Warning: Could not clear {doctype}: {str(e)}")
    
    frappe.db.commit()


def create_shop_types():
    """Create different shop types"""
    print("📋 Creating Shop Types...")
    
    shop_types = [
        {"shop_type_name": "Food Court", "description": "Restaurants and food outlets"},
        {"shop_type_name": "Duty Free", "description": "Tax-free retail shops"},
        {"shop_type_name": "Electronics", "description": "Electronic goods and accessories"},
        {"shop_type_name": "Fashion", "description": "Clothing and accessories"},
        {"shop_type_name": "Bookstore", "description": "Books, magazines, and stationery"},
        {"shop_type_name": "Pharmacy", "description": "Medical supplies and pharmacy"},
        {"shop_type_name": "Souvenir", "description": "Gifts and local souvenirs"},
        {"shop_type_name": "Currency Exchange", "description": "Money exchange services"}
    ]
    
    for shop_type_data in shop_types:
        if not frappe.db.exists("Shop Type", shop_type_data["shop_type_name"]):
            shop_type = frappe.get_doc({
                "doctype": "Shop Type",
                **shop_type_data
            })
            shop_type.insert()
            print(f"   Created Shop Type: {shop_type.shop_type_name}")
    
    frappe.db.commit()


def create_airports():
    """Create sample airports"""
    print("✈️ Creating Airports...")
    
    airports = [
        {
            "airport_code": "BLR",
            "airport_name": "Kempegowda International Airport",
            "city": "Bangalore",
            "country": "India"
        },
        {
            "airport_code": "MAA", 
            "airport_name": "Chennai International Airport",
            "city": "Chennai",
            "country": "India"
        },
        {
            "airport_code": "DEL",
            "airport_name": "Indira Gandhi International Airport", 
            "city": "Delhi",
            "country": "India"
        }
    ]
    
    for airport_data in airports:
        if not frappe.db.exists("Airport", airport_data["airport_code"]):
            airport = frappe.get_doc({
                "doctype": "Airport",
                **airport_data
            })
            airport.insert()
            print(f"   Created Airport: {airport.airport_name}")
    
    frappe.db.commit()


def create_airport_shops():
    """Create airport shop spaces"""
    print("🏪 Creating Airport Shops...")
    
    shop_types = frappe.get_all("Shop Type", fields=["name"])
    airports = frappe.get_all("Airport", fields=["name"])
    
    if not shop_types or not airports:
        print("   ⚠️ No shop types or airports found. Skipping shop creation.")
        return
    
    shops_data = []
    terminals = ["Terminal 1", "Terminal 2", "Domestic Terminal", "International Terminal"]
    
    shop_id = 1
    for airport in airports[:2]:  # Create shops for first 2 airports
        for terminal in terminals[:2]:  # 2 terminals per airport
            for i in range(10):  # 10 shops per terminal
                shop_type = random.choice(shop_types)
                shops_data.append({
                    "shop_number": f"S{shop_id:03d}",
                    "shop_name": f"{shop_type.name} Shop {shop_id}",
                    "airport": airport.name,
                    "terminal": terminal,
                    "shop_type": shop_type.name,
                    "area_sqft": random.randint(200, 800),
                    "monthly_rent": random.randint(50000, 200000),
                    "is_available": random.choice([1, 0]),
                    "status": random.choice(["Available", "Occupied", "Under Maintenance"])
                })
                shop_id += 1
    
    for shop_data in shops_data:
        if not frappe.db.exists("Airport Shop", shop_data["shop_number"]):
            shop = frappe.get_doc({
                "doctype": "Airport Shop",
                **shop_data
            })
            shop.insert()
    
    print(f"   Created {len(shops_data)} Airport Shops")
    frappe.db.commit()


def create_tenants():
    """Create sample tenants"""
    print("👥 Creating Tenants...")
    
    tenants_data = [
        {
            "tenant_name": "McDonald's India",
            "contact_person": "Raj Kumar",
            "email": "raj.kumar@mcdonalds.in",
            "phone": "+91-9876543210",
            "business_type": "Food Court",
            "company_registration": "MCD001"
        },
        {
            "tenant_name": "Samsung Electronics",
            "contact_person": "Priya Sharma", 
            "email": "priya.sharma@samsung.com",
            "phone": "+91-9876543211",
            "business_type": "Electronics",
            "company_registration": "SAM001"
        },
        {
            "tenant_name": "Crossword Bookstores",
            "contact_person": "Amit Patel",
            "email": "amit.patel@crossword.in", 
            "phone": "+91-9876543212",
            "business_type": "Bookstore",
            "company_registration": "CRW001"
        },
        {
            "tenant_name": "Zara Fashion",
            "contact_person": "Maria Lopez",
            "email": "maria.lopez@zara.com",
            "phone": "+91-9876543213", 
            "business_type": "Fashion",
            "company_registration": "ZAR001"
        },
        {
            "tenant_name": "Apollo Pharmacy",
            "contact_person": "Dr. Suresh Reddy",
            "email": "suresh.reddy@apollopharmacy.in",
            "phone": "+91-9876543214",
            "business_type": "Pharmacy", 
            "company_registration": "APO001"
        }
    ]
    
    for tenant_data in tenants_data:
        if not frappe.db.exists("Tenant", tenant_data["tenant_name"]):
            tenant = frappe.get_doc({
                "doctype": "Tenant",
                **tenant_data
            })
            tenant.insert()
            print(f"   Created Tenant: {tenant.tenant_name}")
    
    frappe.db.commit()


def create_shop_lease_contracts():
    """Create shop lease contracts"""
    print("📄 Creating Shop Lease Contracts...")
    
    tenants = frappe.get_all("Tenant", fields=["name"])
    shops = frappe.get_all("Airport Shop", fields=["name", "monthly_rent"], filters={"is_available": 1})
    
    if not tenants or not shops:
        print("   ⚠️ No tenants or available shops found. Skipping contract creation.")
        return
    
    contracts_created = 0
    for i, tenant in enumerate(tenants[:5]):  # Create contracts for first 5 tenants
        if i < len(shops):
            shop = shops[i]
            start_date = add_days(today(), -random.randint(30, 365))
            
            contract = frappe.get_doc({
                "doctype": "Shop Lease Contract",
                "tenant": tenant.name,
                "shop": shop.name,
                "start_date": start_date,
                "end_date": add_months(start_date, 12),  # 1 year contract
                "monthly_rent": shop.monthly_rent,
                "security_deposit": shop.monthly_rent * 3,  # 3 months deposit
                "status": random.choice(["Active", "Pending", "Expired"]),
                "contract_terms": "Standard lease agreement with monthly rent payment."
            })
            contract.insert()
            contracts_created += 1
            
            # Update shop availability
            shop_doc = frappe.get_doc("Airport Shop", shop.name)
            shop_doc.is_available = 0
            shop_doc.status = "Occupied"
            shop_doc.save()
    
    print(f"   Created {contracts_created} Shop Lease Contracts")
    frappe.db.commit()


def create_monthly_invoices():
    """Create monthly invoices for contracts"""
    print("💰 Creating Monthly Invoices...")
    
    contracts = frappe.get_all("Shop Lease Contract", fields=["name", "tenant", "shop", "monthly_rent", "start_date"])
    
    if not contracts:
        print("   ⚠️ No contracts found. Skipping invoice creation.")
        return
    
    invoices_created = 0
    for contract in contracts:
        # Create invoices for the last 6 months
        for month_offset in range(6):
            invoice_date = add_months(today(), -month_offset)
            due_date = add_days(invoice_date, 30)
            
            # Random payment status
            payment_status = random.choice(["Paid", "Unpaid", "Overdue"])
            payment_date = None
            if payment_status == "Paid":
                payment_date = add_days(invoice_date, random.randint(1, 25))
            
            invoice = frappe.get_doc({
                "doctype": "Monthly Invoice",
                "title": f"Invoice {contract.name} - {invoice_date.strftime('%B %Y')}",
                "contract": contract.name,
                "tenant": contract.tenant,
                "shop": contract.shop,
                "invoice_date": invoice_date,
                "due_date": due_date,
                "invoice_amount": contract.monthly_rent,
                "payment_status": payment_status,
                "payment_date": payment_date,
                "description": f"Monthly rent for {invoice_date.strftime('%B %Y')}"
            })
            invoice.insert()
            invoices_created += 1
    
    print(f"   Created {invoices_created} Monthly Invoices")
    frappe.db.commit()


def create_rent_payment_contracts():
    """Create rent payment contracts"""
    print("💳 Creating Rent Payment Contracts...")
    
    paid_invoices = frappe.get_all("Monthly Invoice", 
                                 fields=["name", "invoice_amount", "payment_date"],
                                 filters={"payment_status": "Paid"})
    
    if not paid_invoices:
        print("   ⚠️ No paid invoices found. Skipping payment contract creation.")
        return
    
    payments_created = 0
    for invoice in paid_invoices[:10]:  # Create payments for first 10 paid invoices
        payment = frappe.get_doc({
            "doctype": "Rent Payment Contract",
            "monthly_invoice": invoice.name,
            "payment_amount": invoice.invoice_amount,
            "payment_date": invoice.payment_date,
            "payment_method": random.choice(["Bank Transfer", "Check", "Cash", "Credit Card"]),
            "reference_number": f"PAY{random.randint(10000, 99999)}",
            "status": "Completed",
            "remarks": "Payment received and processed successfully"
        })
        payment.insert()
        payments_created += 1
    
    print(f"   Created {payments_created} Rent Payment Contracts")
    frappe.db.commit()


def create_shop_leads():
    """Create shop leads/applications"""
    print("📧 Creating Shop Leads...")
    
    leads_data = [
        {
            "lead_name": "Starbucks Corporation",
            "contact_person": "John Smith",
            "email": "john.smith@starbucks.com",
            "phone": "+91-9876543215",
            "business_type": "Food Court",
            "preferred_location": "International Terminal",
            "status": "New",
            "source": "Website"
        },
        {
            "lead_name": "Apple India",
            "contact_person": "Sarah Johnson", 
            "email": "sarah.johnson@apple.com",
            "phone": "+91-9876543216",
            "business_type": "Electronics",
            "preferred_location": "Terminal 1",
            "status": "Qualified",
            "source": "Direct Inquiry"
        },
        {
            "lead_name": "Burger King India",
            "contact_person": "Mike Brown",
            "email": "mike.brown@burgerking.in",
            "phone": "+91-9876543217", 
            "business_type": "Food Court",
            "preferred_location": "Terminal 2",
            "status": "Proposal Sent",
            "source": "Referral"
        },
        {
            "lead_name": "Nike Store",
            "contact_person": "Lisa Davis",
            "email": "lisa.davis@nike.com",
            "phone": "+91-9876543218",
            "business_type": "Fashion",
            "preferred_location": "International Terminal", 
            "status": "Negotiation",
            "source": "Trade Show"
        },
        {
            "lead_name": "Local Souvenir Co",
            "contact_person": "Ravi Gupta",
            "email": "ravi.gupta@souvenirs.in",
            "phone": "+91-9876543219",
            "business_type": "Souvenir",
            "preferred_location": "Domestic Terminal",
            "status": "Lost",
            "source": "Cold Call"
        }
    ]
    
    for lead_data in leads_data:
        if not frappe.db.exists("Shop Lead", lead_data["email"]):
            lead = frappe.get_doc({
                "doctype": "Shop Lead",
                **lead_data
            })
            lead.insert()
            print(f"   Created Shop Lead: {lead.lead_name}")
    
    frappe.db.commit()


def print_summary():
    """Print summary of created demo data"""
    print("\n📊 Demo Data Summary:")
    print("=" * 50)
    
    doctypes = [
        "Shop Type",
        "Airport", 
        "Airport Shop",
        "Tenant",
        "Shop Lease Contract",
        "Monthly Invoice",
        "Rent Payment Contract",
        "Shop Lead"
    ]
    
    for doctype in doctypes:
        try:
            count = frappe.db.count(doctype)
            print(f"{doctype:25}: {count:3d} records")
        except:
            print(f"{doctype:25}: N/A")
    
    print("=" * 50)
    print("✅ Demo data creation completed!")
    print("\nYou can now:")
    print("• View Airport Shop Management workspace")
    print("• Test Monthly Invoice functionality")
    print("• Explore shop lease contracts")
    print("• Review payment tracking")
    print("• Manage shop leads and applications")


if __name__ == "__main__":
    frappe.connect()
    create_demo_data()
    print_summary()
