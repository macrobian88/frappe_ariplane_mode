# airplane_mode/api/dashboard.py

import frappe
from frappe import _

@frappe.whitelist()
def get_airplane_dashboard_data():
    """
    Get comprehensive dashboard data for Airplane Mode
    Returns counters for tickets, flights, and various statuses
    """
    try:
        # Get ticket counts by status
        ticket_counts = frappe.db.sql("""
            SELECT 
                status,
                COUNT(*) as count
            FROM `tabAirplane Ticket`
            WHERE docstatus != 2
            GROUP BY status
        """, as_dict=True)
        
        # Convert to dictionary for easier access
        ticket_status_counts = {item['status']: item['count'] for item in ticket_counts}
        
        # Get flight counts by status
        flight_counts = frappe.db.sql("""
            SELECT 
                status,
                COUNT(*) as count
            FROM `tabAirplane Flight`
            WHERE docstatus != 2
            GROUP BY status
        """, as_dict=True)
        
        # Convert to dictionary for easier access
        flight_status_counts = {item['status']: item['count'] for item in flight_counts}
        
        # Calculate total counts
        total_tickets = sum(ticket_status_counts.values())
        total_flights = sum(flight_status_counts.values())
        
        # Calculate confirmed tickets (all except cancelled)
        confirmed_tickets = (
            ticket_status_counts.get('Booked', 0) + 
            ticket_status_counts.get('Checked-In', 0) + 
            ticket_status_counts.get('Boarded', 0)
        )
        
        # Get additional statistics
        revenue_data = frappe.db.sql("""
            SELECT 
                SUM(CASE WHEN total_price IS NOT NULL THEN total_price ELSE 0 END) as total_revenue,
                AVG(CASE WHEN total_price IS NOT NULL AND total_price > 0 THEN total_price ELSE NULL END) as avg_ticket_price
            FROM `tabAirplane Ticket`
            WHERE docstatus != 2 AND status != 'Cancelled'
        """, as_dict=True)[0]
        
        # Get occupancy statistics
        occupancy_data = frappe.db.sql("""
            SELECT 
                AVG(occupancy_percentage) as avg_occupancy,
                SUM(occupancy_count) as total_passengers,
                COUNT(*) as flight_count
            FROM `tabAirplane Flight`
            WHERE docstatus != 2
        """, as_dict=True)[0]
        
        # Get airline statistics
        airline_stats = frappe.db.sql("""
            SELECT 
                airline,
                COUNT(*) as flight_count,
                AVG(occupancy_percentage) as avg_occupancy
            FROM `tabAirplane Flight`
            WHERE docstatus != 2
            GROUP BY airline
            ORDER BY flight_count DESC
            LIMIT 5
        """, as_dict=True)
        
        # Get recent activity
        recent_bookings = frappe.db.sql("""
            SELECT 
                name,
                passenger,
                flight,
                status,
                creation
            FROM `tabAirplane Ticket`
            WHERE docstatus != 2
            ORDER BY creation DESC
            LIMIT 5
        """, as_dict=True)
        
        return {
            'success': True,
            'data': {
                # Main counters
                'counters': {
                    'total_tickets': total_tickets,
                    'total_flights': total_flights,
                    'confirmed_tickets': confirmed_tickets,
                    'cancelled_tickets': ticket_status_counts.get('Cancelled', 0),
                    'completed_flights': flight_status_counts.get('Completed', 0),
                    'scheduled_flights': flight_status_counts.get('Scheduled', 0),
                    'cancelled_flights': flight_status_counts.get('Cancelled', 0),
                    'total_passengers': int(occupancy_data.get('total_passengers') or 0)
                },
                
                # Detailed status breakdown
                'ticket_status_breakdown': ticket_status_counts,
                'flight_status_breakdown': flight_status_counts,
                
                # Financial data
                'revenue': {
                    'total_revenue': float(revenue_data.get('total_revenue') or 0),
                    'avg_ticket_price': float(revenue_data.get('avg_ticket_price') or 0)
                },
                
                # Occupancy data
                'occupancy': {
                    'avg_occupancy': float(occupancy_data.get('avg_occupancy') or 0),
                    'total_passengers': int(occupancy_data.get('total_passengers') or 0)
                },
                
                # Top airlines
                'top_airlines': airline_stats,
                
                # Recent activity
                'recent_bookings': recent_bookings
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_airplane_dashboard_data: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

@frappe.whitelist()
def get_ticket_statistics():
    """Get detailed ticket statistics"""
    try:
        stats = frappe.db.sql("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Booked' THEN 1 ELSE 0 END) as booked,
                SUM(CASE WHEN status = 'Checked-In' THEN 1 ELSE 0 END) as checked_in,
                SUM(CASE WHEN status = 'Boarded' THEN 1 ELSE 0 END) as boarded,
                SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled,
                SUM(CASE WHEN total_price IS NOT NULL THEN total_price ELSE 0 END) as total_revenue
            FROM `tabAirplane Ticket`
            WHERE docstatus != 2
        """, as_dict=True)[0]
        
        return {
            'success': True,
            'data': stats
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@frappe.whitelist()
def get_flight_statistics():
    """Get detailed flight statistics"""
    try:
        stats = frappe.db.sql("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Scheduled' THEN 1 ELSE 0 END) as scheduled,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled,
                AVG(occupancy_percentage) as avg_occupancy,
                SUM(occupancy_count) as total_passengers
            FROM `tabAirplane Flight`
            WHERE docstatus != 2
        """, as_dict=True)[0]
        
        return {
            'success': True,
            'data': stats
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }