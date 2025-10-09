/**
 * Airplane Mode - Main JavaScript File
 * 
 * This file contains core JavaScript functionality for the Airplane Mode app.
 * It handles workspace initialization, common utilities, and app-wide features.
 */

// App initialization
frappe.ready(function() {
    console.log('Airplane Mode app initialized');
    
    // Initialize any global features
    if (typeof initializeAirplaneMode === 'function') {
        initializeAirplaneMode();
    }
});

// Common utilities for Airplane Mode
window.airplane_mode = {
    
    // Initialize the app
    init: function() {
        console.log('Airplane Mode utilities loaded');
        this.setupEventHandlers();
        this.initializeWorkspaces();
    },
    
    // Setup common event handlers
    setupEventHandlers: function() {
        // Handle flight status changes
        $(document).on('click', '.flight-status-btn', function() {
            const status = $(this).data('status');
            airplane_mode.updateFlightStatus(status);
        });
        
        // Handle ticket status changes  
        $(document).on('click', '.ticket-status-btn', function() {
            const status = $(this).data('status');
            airplane_mode.updateTicketStatus(status);
        });
    },
    
    // Initialize workspace features
    initializeWorkspaces: function() {
        // Setup workspace-specific functionality
        if (window.location.pathname.includes('/app/airplane-mode')) {
            this.initializeFlightWorkspace();
        }
        
        if (window.location.pathname.includes('/app/airport-shop-management')) {
            this.initializeShopWorkspace();
        }
    },
    
    // Initialize flight workspace
    initializeFlightWorkspace: function() {
        console.log('Initializing Flight workspace');
        
        // Setup flight-specific features
        this.setupFlightDashboard();
        this.setupCrewManagement();
        this.setupGateTracking();
    },
    
    // Initialize shop workspace  
    initializeShopWorkspace: function() {
        console.log('Initializing Shop workspace');
        
        // Setup shop-specific features
        this.setupShopDashboard();
        this.setupTenantManagement();
        this.setupRentTracking();
    },
    
    // Setup flight dashboard
    setupFlightDashboard: function() {
        // Refresh dashboard data every 30 seconds
        if (typeof refreshFlightDashboard === 'function') {
            setInterval(refreshFlightDashboard, 30000);
        }
    },
    
    // Setup crew management features
    setupCrewManagement: function() {
        // Initialize crew assignment features
        console.log('Crew management initialized');
    },
    
    // Setup gate tracking features
    setupGateTracking: function() {
        // Initialize gate number synchronization
        console.log('Gate tracking initialized');
    },
    
    // Setup shop dashboard
    setupShopDashboard: function() {
        // Initialize shop analytics
        console.log('Shop dashboard initialized');
    },
    
    // Setup tenant management
    setupTenantManagement: function() {
        // Initialize tenant features
        console.log('Tenant management initialized');
    },
    
    // Setup rent tracking
    setupRentTracking: function() {
        // Initialize rent collection features
        console.log('Rent tracking initialized');
    },
    
    // Update flight status
    updateFlightStatus: function(status) {
        console.log('Updating flight status to:', status);
        // Implementation for flight status updates
    },
    
    // Update ticket status
    updateTicketStatus: function(status) {
        console.log('Updating ticket status to:', status);
        // Implementation for ticket status updates
    },
    
    // Utility function to show success message
    showSuccess: function(message) {
        frappe.show_alert({
            message: message,
            indicator: 'green'
        });
    },
    
    // Utility function to show error message
    showError: function(message) {
        frappe.show_alert({
            message: message,
            indicator: 'red'
        });
    },
    
    // Format currency for display
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },
    
    // Format date for display
    formatDate: function(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        }).format(new Date(date));
    },
    
    // Format time for display
    formatTime: function(time) {
        return new Intl.DateTimeFormat('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(time));
    }
};

// Initialize when DOM is ready
$(document).ready(function() {
    airplane_mode.init();
});

// Legacy support - initialize when frappe is ready
if (typeof frappe !== 'undefined') {
    frappe.ready(function() {
        airplane_mode.init();
    });
}

// Global function for backward compatibility
function initializeAirplaneMode() {
    airplane_mode.init();
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = airplane_mode;
}
