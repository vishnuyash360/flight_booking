// Main.js - General functions for SkyWays Airlines

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Flight search form
    const searchForm = document.getElementById('flight-search-form');
    if (searchForm) {
        // Add autocomplete functionality for departure/destination fields
        setupAutocomplete();
    }
    
    // Booking confirmation animation
    const confirmationElement = document.querySelector('.confirmation-animation');
    if (confirmationElement) {
        setTimeout(() => {
            confirmationElement.classList.add('show');
        }, 500);
    }
    
    // Snack quantity adjustment
    setupSnackQuantityControls();
});

/**
 * Set up autocomplete for departure and destination fields
 */
function setupAutocomplete() {
    // This would typically use a real autocomplete library or API
    // For now, we'll just demonstrate the concept with sample data
    const cities = [
        'Atlanta', 'Boston', 'Chicago', 'Dallas', 'Denver', 'Detroit',
        'Houston', 'Las Vegas', 'Los Angeles', 'Miami', 'New York', 
        'Philadelphia', 'Phoenix', 'San Francisco', 'Seattle'
    ];
    
    // Setup for departure field
    const departureField = document.getElementById('departure');
    if (departureField) {
        departureField.addEventListener('input', function() {
            showSuggestions(this, cities);
        });
    }
    
    // Setup for destination field
    const destinationField = document.getElementById('destination');
    if (destinationField) {
        destinationField.addEventListener('input', function() {
            showSuggestions(this, cities);
        });
    }
}

/**
 * Show autocomplete suggestions for a field
 */
function showSuggestions(inputField, suggestions) {
    const value = inputField.value.toLowerCase();
    
    // Remove existing suggestion container
    const existingContainer = document.getElementById('suggestions-container');
    if (existingContainer) {
        existingContainer.remove();
    }
    
    if (!value) return;
    
    // Filter suggestions based on input
    const matchingSuggestions = suggestions.filter(city => 
        city.toLowerCase().startsWith(value)
    );
    
    if (matchingSuggestions.length === 0) return;
    
    // Create suggestions container
    const container = document.createElement('div');
    container.id = 'suggestions-container';
    container.className = 'position-absolute bg-white shadow-sm rounded mt-1 w-100 z-index-1000';
    
    // Add each suggestion
    matchingSuggestions.forEach(city => {
        const suggestion = document.createElement('div');
        suggestion.className = 'p-2 suggestion';
        suggestion.textContent = city;
        suggestion.style.cursor = 'pointer';
        
        suggestion.addEventListener('click', () => {
            inputField.value = city;
            container.remove();
        });
        
        container.appendChild(suggestion);
    });
    
    // Add container after input field
    inputField.parentNode.style.position = 'relative';
    inputField.parentNode.appendChild(container);
    
    // Close suggestions when clicking outside
    document.addEventListener('click', function closeHandler(e) {
        if (!container.contains(e.target) && e.target !== inputField) {
            container.remove();
            document.removeEventListener('click', closeHandler);
        }
    });
}

/**
 * Setup quantity controls for snack selection
 */
function setupSnackQuantityControls() {
    const decrementButtons = document.querySelectorAll('.decrement-btn');
    const incrementButtons = document.querySelectorAll('.increment-btn');
    
    decrementButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentNode.querySelector('input');
            const currentValue = parseInt(input.value) || 0;
            if (currentValue > 0) {
                input.value = currentValue - 1;
                updateSnackSubtotal(input);
            }
        });
    });
    
    incrementButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentNode.querySelector('input');
            const currentValue = parseInt(input.value) || 0;
            input.value = currentValue + 1;
            updateSnackSubtotal(input);
        });
    });
    
    // Update subtotals when quantity changes directly
    const quantityInputs = document.querySelectorAll('.snack-quantity');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            updateSnackSubtotal(this);
        });
    });
}

/**
 * Update subtotal for a snack when quantity changes
 */
function updateSnackSubtotal(input) {
    const snackId = input.getAttribute('data-snack-id');
    const price = parseFloat(input.getAttribute('data-price'));
    const quantity = parseInt(input.value) || 0;
    const subtotal = price * quantity;
    
    // Update subtotal display
    const subtotalElement = document.getElementById(`subtotal-${snackId}`);
    if (subtotalElement) {
        subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
    }
    
    // Update total
    updateSnackTotal();
}

/**
 * Update the total price for all selected snacks
 */
function updateSnackTotal() {
    const quantityInputs = document.querySelectorAll('.snack-quantity');
    let total = 0;
    
    quantityInputs.forEach(input => {
        const price = parseFloat(input.getAttribute('data-price'));
        const quantity = parseInt(input.value) || 0;
        total += price * quantity;
    });
    
    // Update total display
    const totalElement = document.getElementById('snack-total');
    if (totalElement) {
        totalElement.textContent = `$${total.toFixed(2)}`;
    }
}
