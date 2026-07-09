// SeatMap.js - Handle seat selection functionality

document.addEventListener('DOMContentLoaded', function() {
    initializeSeatMap();
});

/**
 * Initialize the seat map functionality
 */
function initializeSeatMap() {
    const seatElements = document.querySelectorAll('.seat.available');
    const selectedSeatInput = document.getElementById('selected-seat');
    const seatPriceElement = document.getElementById('seat-price');
    const seatClassElement = document.getElementById('seat-class');
    const nextStepButton = document.getElementById('next-step-button');
    
    if (!seatElements.length) return;
    
    // Add click event to each available seat
    seatElements.forEach(seat => {
        seat.addEventListener('click', function() {
            // Deselect any currently selected seat
            const currentlySelected = document.querySelector('.seat.selected');
            if (currentlySelected) {
                currentlySelected.classList.remove('selected');
            }
            
            // Select this seat
            this.classList.add('selected');
            
            // Update the hidden input value
            if (selectedSeatInput) {
                selectedSeatInput.value = this.dataset.code;
            }
            
            // Update price display
            if (seatPriceElement) {
                seatPriceElement.textContent = `$${parseFloat(this.dataset.price).toFixed(2)}`;
            }
            
            // Update seat class display
            if (seatClassElement) {
                seatClassElement.textContent = this.dataset.class;
            }
            
            // Enable the next step button
            if (nextStepButton) {
                nextStepButton.disabled = false;
            }
            
            // Update legend selection
            updateLegendSelection(this.dataset.class);
            
            // Show seat details
            showSeatDetails(this.dataset.code, this.dataset.price, this.dataset.class);
        });
    });
    
    // Initialize legend interactivity
    initializeLegend();
}

/**
 * Show seat details in the sidebar
 */
function showSeatDetails(code, price, seatClass) {
    const detailsContainer = document.getElementById('seat-details');
    if (!detailsContainer) return;
    
    // Update seat details
    detailsContainer.innerHTML = `
        <div class="card">
            <div class="card-header bg-sky text-white">
                <h5 class="mb-0">Selected Seat</h5>
            </div>
            <div class="card-body">
                <h3 class="mb-3">${code}</h3>
                <p class="mb-2"><strong>Class:</strong> ${seatClass}</p>
                <p class="mb-2"><strong>Price:</strong> $${parseFloat(price).toFixed(2)}</p>
                
                <div class="mt-3">
                    <h6>Seat Features:</h6>
                    <ul class="list-unstyled">
                        ${getSeatFeatures(seatClass)}
                    </ul>
                </div>
            </div>
        </div>
    `;
    
    // Show the details container
    detailsContainer.classList.remove('d-none');
}

/**
 * Get seat features based on seat class
 */
function getSeatFeatures(seatClass) {
    let features = '';
    
    if (seatClass === 'First') {
        features = `
            <li><i class="fas fa-check-circle text-success me-2"></i> Fully reclining seat</li>
            <li><i class="fas fa-check-circle text-success me-2"></i> Premium dining service</li>
            <li><i class="fas fa-check-circle text-success me-2"></i> Personal entertainment system</li>
            <li><i class="fas fa-check-circle text-success me-2"></i> Priority boarding</li>
            <li><i class="fas fa-check-circle text-success me-2"></i> Extra baggage allowance</li>
        `;
    } else if (seatClass === 'Business') {
        features = `
            <li><i class="fas fa-check-circle text-success me-2"></i> Reclining seat with extra legroom</li>
            <li><i class="fas fa-check-circle text-success me-2"></i> Enhanced dining options</li>
            <li><i class="fas fa-check-circle text-success me-2"></i> Personal entertainment system</li>
            <li><i class="fas fa-check-circle text-success me-2"></i> Priority boarding</li>
        `;
    } else {
        features = `
            <li><i class="fas fa-check-circle text-success me-2"></i> Standard seat</li>
            <li><i class="fas fa-check-circle text-success me-2"></i> Complimentary beverage</li>
            <li><i class="fas fa-check-circle text-success me-2"></i> Shared entertainment system</li>
        `;
    }
    
    return features;
}

/**
 * Initialize seat map legend functionality
 */
function initializeLegend() {
    const legendItems = document.querySelectorAll('.seat-legend-item');
    
    legendItems.forEach(item => {
        item.addEventListener('click', function() {
            const seatClass = this.dataset.class;
            highlightSeatsByClass(seatClass);
        });
    });
}

/**
 * Highlight seats of a specific class
 */
function highlightSeatsByClass(seatClass) {
    // Remove highlight from all seats first
    const allSeats = document.querySelectorAll('.seat');
    allSeats.forEach(seat => {
        seat.classList.remove('highlight');
    });
    
    // If a class was specified, highlight those seats
    if (seatClass) {
        const classSeats = document.querySelectorAll(`.seat[data-class="${seatClass}"]`);
        classSeats.forEach(seat => {
            seat.classList.add('highlight');
        });
    }
}

/**
 * Update the legend selection indicator
 */
function updateLegendSelection(seatClass) {
    const legendItems = document.querySelectorAll('.seat-legend-item');
    
    legendItems.forEach(item => {
        if (item.dataset.class === seatClass) {
            item.classList.add('selected');
        } else {
            item.classList.remove('selected');
        }
    });
}
