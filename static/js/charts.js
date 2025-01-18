/**
 * Chart configurations and utilities for the Crypto Tracker application
 */

const CryptoCharts = {
    /**
     * Default chart colors
     */
    colors: {
        primary: '#1a237e',
        success: '#2ecc71',
        danger: '#e74c3c',
        warning: '#f1c40f'
    },

    /**
     * Create a price chart
     * @param {HTMLCanvasElement} canvas - Canvas element
     * @param {Array} data - Price data
     * @param {object} options - Additional options
     * @returns {Chart} Chart.js instance
     */
    createPriceChart: function(canvas, data, options = {}) {
        const ctx = canvas.getContext('2d');
        const gradient = CryptoUtils.createGradient(ctx, this.colors.primary);

        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(item => CryptoUtils.formatDate(item.timestamp)),
                datasets: [{
                    label: options.symbol ? `${options.symbol} Price` : 'Price',
                    data: data.map(item => item.price),
                    borderColor: this.colors.primary,
                    backgroundColor: gradient,
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHitRadius: 20
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `$${CryptoUtils.formatCurrency(context.parsed.y)}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            maxTicksLimit: 8,
                            maxRotation: 0
                        }
                    },
                    y: {
                        grid: {
                            borderDash: [5, 5]
                        },
                        ticks: {
                            callback: function(value) {
                                return '$' + CryptoUtils.formatCurrency(value);
                            }
                        }
                    }
                },
                ...options
            }
        });
    },

    /**
     * Create a mini price chart (for watchlist cards)
     * @param {HTMLCanvasElement} canvas - Canvas element
     * @param {Array} data - Price data
     * @param {object} options - Additional options
     * @returns {Chart} Chart.js instance
     */
    createMiniChart: function(canvas, data, options = {}) {
        const ctx = canvas.getContext('2d');
        const priceChange = CryptoUtils.calculatePercentageChange(
            data[data.length - 1].price,
            data[0].price
        );
        const color = priceChange >= 0 ? this.colors.success : this.colors.danger;

        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(item => item.timestamp),
                datasets: [{
                    data: data.map(item => item.price),
                    borderColor: color,
                    borderWidth: 1.5,
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                },
                scales: {
                    x: {
                        display: false
                    },
                    y: {
                        display: false
                    }
                },
                ...options
            }
        });
    },

    /**
     * Create a market dominance pie chart
     * @param {HTMLCanvasElement} canvas - Canvas element
     * @param {Array} data - Market dominance data
     * @returns {Chart} Chart.js instance
     */
    createMarketDominanceChart: function(canvas, data) {
        return new Chart(canvas, {
            type: 'doughnut',
            data: {
                labels: data.map(item => item.symbol),
                datasets: [{
                    data: data.map(item => item.dominance),
                    backgroundColor: [
                        '#1a237e',
                        '#283593',
                        '#303f9f',
                        '#3949ab',
                        '#3f51b5'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed}%`;
                            }
                        }
                    }
                }
            }
        });
    },

    /**
     * Update chart data
     * @param {Chart} chart - Chart.js instance
     * @param {Array} newData - New data points
     */
    updateChartData: function(chart, newData) {
        chart.data.labels = newData.map(item => CryptoUtils.formatDate(item.timestamp));
        chart.data.datasets[0].data = newData.map(item => item.price);
        chart.update('none');
    }
};
