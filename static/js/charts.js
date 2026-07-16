/**
 * ============================================================
 * InternAI - Chart.js Configurations
 * ============================================================
 * Predefined chart configurations for analytics dashboards.
 * Uses Chart.js library for rendering interactive charts
 * with consistent dark theme styling.
 * ============================================================
 */

/**
 * Default chart options shared across all chart types.
 * Applies dark theme colors and consistent typography.
 */
const defaultChartOptions = {
    // Make charts responsive to container size
    responsive: true,
    // Maintain aspect ratio based on container
    maintainAspectRatio: false,
    // Plugin configurations
    plugins: {
        // Legend configuration
        legend: {
            labels: {
                color: '#A0A0B0',              // Muted text color
                font: {
                    family: "'Inter', sans-serif", // Match site font
                    size: 12,
                },
                padding: 20,                    // Space between legend items
                usePointStyle: true,             // Use dots instead of rectangles
            },
        },
        // Tooltip configuration
        tooltip: {
            backgroundColor: '#1A1A2E',         // Dark surface background
            titleColor: '#FFFFFF',               // White title
            bodyColor: '#A0A0B0',                // Muted body text
            borderColor: 'rgba(255,255,255,0.1)', // Subtle border
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8,
            titleFont: {
                family: "'Inter', sans-serif",
                weight: '600',
            },
            bodyFont: {
                family: "'Inter', sans-serif",
            },
        },
    },
    // Scale (axes) configurations
    scales: {
        x: {
            grid: {
                color: 'rgba(255,255,255,0.05)',  // Very faint grid lines
                drawBorder: false,
            },
            ticks: {
                color: '#6B6B80',                  // Muted tick labels
                font: {
                    family: "'Inter', sans-serif",
                    size: 11,
                },
            },
        },
        y: {
            grid: {
                color: 'rgba(255,255,255,0.05)',
                drawBorder: false,
            },
            ticks: {
                color: '#6B6B80',
                font: {
                    family: "'Inter', sans-serif",
                    size: 11,
                },
            },
        },
    },
};

/**
 * Initialize a line chart for application trends.
 * Shows monthly application submissions over time.
 *
 * @param {string} canvasId - The ID of the canvas element
 * @param {Array} labels - Array of month labels
 * @param {Array} data - Array of application counts
 */
function initApplicationTrendChart(canvasId, labels, data) {
    // Get the canvas element by ID
    const ctx = document.getElementById(canvasId);

    // Exit if canvas element doesn't exist on this page
    if (!ctx) return;

    // Create gradient fill for the line
    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(108, 99, 255, 0.3)');   // Purple at top
    gradient.addColorStop(1, 'rgba(108, 99, 255, 0.0)');   // Transparent at bottom

    // Create and return the Chart.js instance
    return new Chart(ctx, {
        type: 'line',                          // Line chart type
        data: {
            labels: labels,                     // X-axis labels
            datasets: [{
                label: 'Applications',           // Dataset label
                data: data,                      // Y-axis data points
                borderColor: '#6C63FF',          // Line color (primary)
                backgroundColor: gradient,        // Fill gradient
                borderWidth: 2.5,                // Line thickness
                fill: true,                      // Fill area under line
                tension: 0.4,                    // Curve smoothness (0=straight, 1=very curved)
                pointBackgroundColor: '#6C63FF', // Point fill color
                pointBorderColor: '#1A1A2E',     // Point border (matches background)
                pointBorderWidth: 2,
                pointRadius: 4,                  // Point size
                pointHoverRadius: 7,             // Point size on hover
            }],
        },
        options: {
            ...defaultChartOptions,              // Spread default options
        },
    });
}

/**
 * Initialize a doughnut chart for application status distribution.
 * Shows breakdown of applications by status.
 *
 * @param {string} canvasId - The ID of the canvas element
 * @param {Array} labels - Array of status labels
 * @param {Array} data - Array of counts per status
 */
function initStatusDistributionChart(canvasId, labels, data) {
    // Get the canvas element
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    return new Chart(ctx, {
        type: 'doughnut',                       // Doughnut chart type
        data: {
            labels: labels,                      // Status labels
            datasets: [{
                data: data,                      // Count per status
                backgroundColor: [               // Colors for each segment
                    '#6C63FF',  // Primary (Pending)
                    '#00C9A7',  // Success (Accepted)
                    '#FF6584',  // Accent (Interview)
                    '#FFB344',  // Warning (Reviewing)
                    '#FF4757',  // Danger (Rejected)
                    '#3498DB',  // Info (Assessment)
                ],
                borderColor: '#1A1A2E',          // Border matches background
                borderWidth: 3,                   // Space between segments
                hoverOffset: 8,                   // Pop-out on hover
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',                        // Size of center hole
            plugins: {
                legend: {
                    position: 'bottom',            // Legend below chart
                    labels: {
                        color: '#A0A0B0',
                        font: { family: "'Inter', sans-serif", size: 12 },
                        padding: 16,
                        usePointStyle: true,
                    },
                },
                tooltip: defaultChartOptions.plugins.tooltip,
            },
        },
    });
}

/**
 * Initialize a bar chart for recruitment funnel or skill frequency.
 *
 * @param {string} canvasId - The ID of the canvas element
 * @param {Array} labels - Array of category labels
 * @param {Array} data - Array of values
 * @param {string} label - Dataset label
 */
function initBarChart(canvasId, labels, data, label) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    return new Chart(ctx, {
        type: 'bar',                             // Bar chart type
        data: {
            labels: labels,
            datasets: [{
                label: label || 'Count',
                data: data,
                backgroundColor: [               // Gradient bars
                    'rgba(108, 99, 255, 0.7)',
                    'rgba(0, 201, 167, 0.7)',
                    'rgba(255, 101, 132, 0.7)',
                    'rgba(255, 179, 68, 0.7)',
                    'rgba(52, 152, 219, 0.7)',
                    'rgba(155, 89, 182, 0.7)',
                ],
                borderColor: [
                    '#6C63FF',
                    '#00C9A7',
                    '#FF6584',
                    '#FFB344',
                    '#3498DB',
                    '#9B59B6',
                ],
                borderWidth: 1,
                borderRadius: 6,                  // Rounded bar corners
                maxBarThickness: 50,              // Maximum bar width
            }],
        },
        options: {
            ...defaultChartOptions,
            plugins: {
                ...defaultChartOptions.plugins,
                legend: { display: false },        // Hide legend for bar charts
            },
        },
    });
}

/**
 * Initialize a radar chart for evaluation scores.
 * Shows multi-criteria performance assessment.
 *
 * @param {string} canvasId - The ID of the canvas element
 * @param {Array} labels - Array of criteria labels
 * @param {Array} data - Array of scores (1-10)
 */
function initRadarChart(canvasId, labels, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    return new Chart(ctx, {
        type: 'radar',                           // Radar chart type
        data: {
            labels: labels,                       // Criteria labels
            datasets: [{
                label: 'Score',
                data: data,
                backgroundColor: 'rgba(108, 99, 255, 0.2)',  // Fill area
                borderColor: '#6C63FF',           // Border line
                borderWidth: 2,
                pointBackgroundColor: '#6C63FF',  // Point fill
                pointBorderColor: '#1A1A2E',
                pointBorderWidth: 2,
                pointRadius: 5,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {                              // Radial axis
                    beginAtZero: true,
                    max: 10,                       // Maximum score
                    ticks: {
                        stepSize: 2,               // Grid lines every 2 points
                        color: '#6B6B80',
                        backdropColor: 'transparent',
                        font: { size: 10 },
                    },
                    grid: {
                        color: 'rgba(255,255,255,0.08)',
                    },
                    pointLabels: {
                        color: '#A0A0B0',
                        font: {
                            family: "'Inter', sans-serif",
                            size: 12,
                        },
                    },
                },
            },
            plugins: {
                legend: { display: false },
                tooltip: defaultChartOptions.plugins.tooltip,
            },
        },
    });
}
