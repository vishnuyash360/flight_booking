// Chart.js - Admin dashboard charts

document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts if on admin dashboard
    if (document.getElementById('booking-chart')) {
        initializeBookingChart();
    }
    
    if (document.getElementById('revenue-chart')) {
        initializeRevenueChart();
    }
    
    if (document.getElementById('snack-revenue-chart')) {
        initializeSnackRevenueChart();
    }
    
    // Initialize monthly report table if present
    if (document.getElementById('monthly-report-table')) {
        initializeDataTable();
    }
});

/**
 * Initialize the bookings chart
 */
function initializeBookingChart() {
    const ctx = document.getElementById('booking-chart').getContext('2d');
    
    // Get data from the data attributes
    const chartData = JSON.parse(document.getElementById('booking-chart-data').dataset.bookings);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Number of Bookings',
                data: chartData.data,
                backgroundColor: 'rgba(26, 115, 232, 0.7)',
                borderColor: 'rgba(26, 115, 232, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    precision: 0
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Monthly Bookings by Flight',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Bookings: ${context.raw}`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Initialize the revenue chart
 */
function initializeRevenueChart() {
    const ctx = document.getElementById('revenue-chart').getContext('2d');
    
    // Get data from the data attributes
    const chartData = JSON.parse(document.getElementById('revenue-chart-data').dataset.revenue);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Revenue ($)',
                data: chartData.data,
                backgroundColor: 'rgba(13, 71, 161, 0.1)',
                borderColor: 'rgba(13, 71, 161, 1)',
                borderWidth: 2,
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value;
                        }
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Monthly Revenue by Flight',
                    font: {
                        size: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Revenue: $${context.raw.toFixed(2)}`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Initialize the snack revenue chart
 */
function initializeSnackRevenueChart() {
    const ctx = document.getElementById('snack-revenue-chart').getContext('2d');
    
    // Get data from the data attributes
    const chartData = JSON.parse(document.getElementById('snack-revenue-chart-data').dataset.snacks);
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: chartData.labels,
            datasets: [{
                data: chartData.data,
                backgroundColor: [
                    'rgba(26, 115, 232, 0.7)',
                    'rgba(13, 71, 161, 0.7)',
                    'rgba(25, 118, 210, 0.7)',
                    'rgba(66, 165, 245, 0.7)',
                    'rgba(100, 181, 246, 0.7)',
                    'rgba(144, 202, 249, 0.7)'
                ],
                borderColor: [
                    'rgba(26, 115, 232, 1)',
                    'rgba(13, 71, 161, 1)',
                    'rgba(25, 118, 210, 1)',
                    'rgba(66, 165, 245, 1)',
                    'rgba(100, 181, 246, 1)',
                    'rgba(144, 202, 249, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Snack Revenue Distribution',
                    font: {
                        size: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.raw / total) * 100).toFixed(1);
                            return `${context.label}: $${context.raw.toFixed(2)} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Initialize DataTable for report table
 */
function initializeDataTable() {
    // This would normally use DataTables library, but for simplicity we'll add basic functionality
    const table = document.getElementById('monthly-report-table');
    if (!table) return;
    
    // Add sort functionality to table headers
    const headers = table.querySelectorAll('th');
    headers.forEach((header, index) => {
        if (header.classList.contains('sortable')) {
            header.addEventListener('click', function() {
                sortTable(table, index);
            });
            header.style.cursor = 'pointer';
            header.innerHTML += '<span class="ms-1">↕️</span>';
        }
    });
    
    // Add search functionality
    const searchInput = document.getElementById('table-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            filterTable(table, this.value);
        });
    }
}

/**
 * Sort a table by a specific column
 */
function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const headerRow = table.querySelector('th:nth-child(' + (columnIndex + 1) + ')');
    
    // Determine sort direction
    const ascending = headerRow.classList.contains('sort-asc') ? false : true;
    
    // Update header classes
    table.querySelectorAll('th').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });
    
    headerRow.classList.add(ascending ? 'sort-asc' : 'sort-desc');
    
    // Sort the rows
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        // Check if the values are numbers (including currency)
        const aNum = parseFloat(aValue.replace(/[^0-9.-]+/g, ''));
        const bNum = parseFloat(bValue.replace(/[^0-9.-]+/g, ''));
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return ascending ? aNum - bNum : bNum - aNum;
        }
        
        // Otherwise sort as strings
        return ascending 
            ? aValue.localeCompare(bValue) 
            : bValue.localeCompare(aValue);
    });
    
    // Reorder the rows
    rows.forEach(row => tbody.appendChild(row));
}

/**
 * Filter table rows based on search input
 */
function filterTable(table, searchText) {
    const rows = table.querySelectorAll('tbody tr');
    const lowercaseSearch = searchText.toLowerCase();
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(lowercaseSearch) ? '' : 'none';
    });
}
