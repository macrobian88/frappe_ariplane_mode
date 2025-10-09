// airplane_mode/public/js/airplane_dashboard.js

frappe.provide('airplane_mode.dashboard');

airplane_mode.dashboard = {
    init: function() {
        this.setup_dashboard();
        this.setup_auto_refresh();
    },

    setup_dashboard: function() {
        const dashboard_html = `
            <div class="row airplane-dashboard">
                <div class="col-xs-12">
                    <h3 class="text-center">Airplane Mode Dashboard</h3>
                </div>
            </div>
            
            <!-- Main Counters Row -->
            <div class="row airplane-counters" style="margin-bottom: 20px;">
                <div class="col-xs-12 col-md-3">
                    <div class="card card-stats">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-5">
                                    <div class="icon-big text-center icon-warning">
                                        <i class="fa fa-ticket text-primary"></i>
                                    </div>
                                </div>
                                <div class="col-7">
                                    <div class="numbers">
                                        <p class="card-category">Total Tickets</p>
                                        <h4 class="card-title" id="total-tickets">-</h4>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-xs-12 col-md-3">
                    <div class="card card-stats">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-5">
                                    <div class="icon-big text-center icon-warning">
                                        <i class="fa fa-plane text-success"></i>
                                    </div>
                                </div>
                                <div class="col-7">
                                    <div class="numbers">
                                        <p class="card-category">Total Flights</p>
                                        <h4 class="card-title" id="total-flights">-</h4>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-xs-12 col-md-3">
                    <div class="card card-stats">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-5">
                                    <div class="icon-big text-center icon-warning">
                                        <i class="fa fa-check text-info"></i>
                                    </div>
                                </div>
                                <div class="col-7">
                                    <div class="numbers">
                                        <p class="card-category">Confirmed Tickets</p>
                                        <h4 class="card-title" id="confirmed-tickets">-</h4>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-xs-12 col-md-3">
                    <div class="card card-stats">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-5">
                                    <div class="icon-big text-center icon-warning">
                                        <i class="fa fa-users text-warning"></i>
                                    </div>
                                </div>
                                <div class="col-7">
                                    <div class="numbers">
                                        <p class="card-category">Total Passengers</p>
                                        <h4 class="card-title" id="total-passengers">-</h4>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Detailed Status Row -->
            <div class="row airplane-status-details" style="margin-bottom: 20px;">
                <div class="col-xs-12 col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="card-title">Ticket Status Breakdown</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-6">
                                    <div class="status-item">
                                        <span class="badge badge-primary" id="booked-count">0</span>
                                        <span class="status-label">Booked</span>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="status-item">
                                        <span class="badge badge-info" id="checked-in-count">0</span>
                                        <span class="status-label">Checked-In</span>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="status-item">
                                        <span class="badge badge-success" id="boarded-count">0</span>
                                        <span class="status-label">Boarded</span>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="status-item">
                                        <span class="badge badge-danger" id="cancelled-tickets-count">0</span>
                                        <span class="status-label">Cancelled</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-xs-12 col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="card-title">Flight Status Breakdown</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-6">
                                    <div class="status-item">
                                        <span class="badge badge-warning" id="scheduled-count">0</span>
                                        <span class="status-label">Scheduled</span>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="status-item">
                                        <span class="badge badge-success" id="completed-count">0</span>
                                        <span class="status-label">Completed</span>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="status-item">
                                        <span class="badge badge-danger" id="cancelled-flights-count">0</span>
                                        <span class="status-label">Cancelled</span>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="status-item">
                                        <span class="badge badge-info" id="avg-occupancy">0%</span>
                                        <span class="status-label">Avg Occupancy</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Revenue Row -->
            <div class="row airplane-revenue" style="margin-bottom: 20px;">
                <div class="col-xs-12 col-md-6">
                    <div class="card card-stats">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-5">
                                    <div class="icon-big text-center icon-warning">
                                        <i class="fa fa-money text-success"></i>
                                    </div>
                                </div>
                                <div class="col-7">
                                    <div class="numbers">
                                        <p class="card-category">Total Revenue</p>
                                        <h4 class="card-title" id="total-revenue">₹0</h4>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-xs-12 col-md-6">
                    <div class="card card-stats">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-5">
                                    <div class="icon-big text-center icon-warning">
                                        <i class="fa fa-calculator text-info"></i>
                                    </div>
                                </div>
                                <div class="col-7">
                                    <div class="numbers">
                                        <p class="card-category">Avg Ticket Price</p>
                                        <h4 class="card-title" id="avg-ticket-price">₹0</h4>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Add CSS for better styling
        const style = `
            <style>
                .airplane-dashboard .card {
                    border: 1px solid #e9ecef;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                }
                
                .airplane-dashboard .card-body {
                    padding: 20px;
                }
                
                .airplane-dashboard .card-header {
                    padding: 15px 20px;
                    background-color: #f8f9fa;
                    border-bottom: 1px solid #e9ecef;
                }
                
                .airplane-dashboard .icon-big {
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background-color: #f8f9fa;
                }
                
                .airplane-dashboard .icon-big i {
                    font-size: 24px;
                }
                
                .airplane-dashboard .card-category {
                    color: #6c757d;
                    font-size: 14px;
                    margin-bottom: 5px;
                }
                
                .airplane-dashboard .card-title {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                    margin: 0;
                }
                
                .airplane-dashboard .status-item {
                    display: flex;
                    align-items: center;
                    margin-bottom: 10px;
                }
                
                .airplane-dashboard .status-item .badge {
                    margin-right: 10px;
                    font-size: 14px;
                    padding: 6px 12px;
                }
                
                .airplane-dashboard .status-label {
                    font-size: 14px;
                    color: #333;
                }
                
                .airplane-dashboard .text-primary { color: #007bff !important; }
                .airplane-dashboard .text-success { color: #28a745 !important; }
                .airplane-dashboard .text-info { color: #17a2b8 !important; }
                .airplane-dashboard .text-warning { color: #ffc107 !important; }
                .airplane-dashboard .text-danger { color: #dc3545 !important; }
                
                .refresh-indicator {
                    color: #28a745;
                    font-size: 12px;
                    float: right;
                }
            </style>
        `;

        // Create dashboard container
        const dashboard_container = $(dashboard_html);
        $(style).appendTo('head');
        
        return dashboard_container;
    },

    load_dashboard_data: function() {
        const self = this;
        
        frappe.call({
            method: 'airplane_mode.api.dashboard.get_airplane_dashboard_data',
            callback: function(response) {
                if (response.message && response.message.success) {
                    self.update_dashboard(response.message.data);
                } else {
                    frappe.msgprint(__('Error loading dashboard data'));
                }
            }
        });
    },

    update_dashboard: function(data) {
        const counters = data.counters;
        const revenue = data.revenue;
        const occupancy = data.occupancy;
        const ticket_breakdown = data.ticket_status_breakdown;
        const flight_breakdown = data.flight_status_breakdown;

        // Update main counters
        $('#total-tickets').text(counters.total_tickets || 0);
        $('#total-flights').text(counters.total_flights || 0);
        $('#confirmed-tickets').text(counters.confirmed_tickets || 0);
        $('#total-passengers').text(counters.total_passengers || 0);

        // Update ticket status breakdown
        $('#booked-count').text(ticket_breakdown.Booked || 0);
        $('#checked-in-count').text(ticket_breakdown['Checked-In'] || 0);
        $('#boarded-count').text(ticket_breakdown.Boarded || 0);
        $('#cancelled-tickets-count').text(ticket_breakdown.Cancelled || 0);

        // Update flight status breakdown
        $('#scheduled-count').text(flight_breakdown.Scheduled || 0);
        $('#completed-count').text(flight_breakdown.Completed || 0);
        $('#cancelled-flights-count').text(flight_breakdown.Cancelled || 0);
        $('#avg-occupancy').text(Math.round(occupancy.avg_occupancy || 0) + '%');

        // Update revenue information
        $('#total-revenue').text('₹' + (revenue.total_revenue || 0).toLocaleString());
        $('#avg-ticket-price').text('₹' + Math.round(revenue.avg_ticket_price || 0).toLocaleString());

        // Show last updated time
        $('.refresh-indicator').remove();
        $('<span class="refresh-indicator">Last updated: ' + frappe.datetime.now_time() + '</span>')
            .appendTo('.airplane-dashboard h3');
    },

    setup_auto_refresh: function() {
        const self = this;
        // Refresh every 30 seconds
        setInterval(function() {
            self.load_dashboard_data();
        }, 30000);
    },

    render: function(parent) {
        const self = this;
        const dashboard = self.setup_dashboard();
        $(parent).html(dashboard);
        
        // Load initial data
        self.load_dashboard_data();
    }
};

// Initialize when page loads
$(document).ready(function() {
    if (frappe.get_route()[0] === 'airplane-dashboard') {
        airplane_mode.dashboard.init();
    }
});