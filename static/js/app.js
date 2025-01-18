/**
 * Main application logic for the Crypto Tracker
 */

class CryptoTracker {
    constructor() {
        this.charts = {};
        this.updateInterval = 10000; // 10 seconds
        this.intervals = [];
        
        this.init();
    }

    /**
     * Initialize the application
     */
    init() {
        this.setupEventListeners();
        this.startPriceUpdates();
        this.initializeCharts();
    }

    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Timeframe selector for price charts
        document.querySelectorAll('.timeframe-selector button').forEach(button => {
            button.addEventListener('click', (e) => {
                const buttons = e.target.parentElement.querySelectorAll('button');
                buttons.forEach(btn => btn.classList.remove('active'));
                e.target.classList.add('active');
                
                this.updateChart(e.target.dataset.timeframe);
            });
        });

        // Watchlist toggles
        document.querySelectorAll('.toggle-watchlist').forEach(button => {
            button.addEventListener('click', async (e) => {
                try {
                    const symbol = e.target.dataset.symbol;
                    const response = await CryptoAPI.toggleWatchlist(symbol);
                    
                    button.classList.toggle('active', response.status === 'added');
                    const icon = button.querySelector('i');
                    icon.classList.toggle('text-warning', response.status === 'added');
                    
                    CryptoUtils.showNotification(
                        `${symbol} ${response.status === 'added' ? 'added to' : 'removed from'} watchlist`,
                        'success'
                    );
                } catch (error) {
                    CryptoUtils.showNotification('Failed to update watchlist', 'error');
                }
            });
        });

        // Price alert form
        const alertForm = document.getElementById('alertForm');
        if (alertForm) {
            document.getElementById('createAlert').addEventListener('click', async () => {
                try {
                    const formData = new FormData(alertForm);
                    const symbol = alertForm.dataset.symbol;
                    
                    await CryptoAPI.createAlert(symbol, {
                        alert_type: formData.get('alert_type'),
                        target_price: formData.get('target_price')
                    });
                    
                    bootstrap.Modal.getInstance(document.getElementById('alertModal')).hide();
                    alertForm.reset();
                    
                    CryptoUtils.showNotification('Price alert created successfully', 'success');
                } catch (error) {
                    CryptoUtils.showNotification('Failed to create price alert', 'error');
                }
            });
        }

        // Delete alert buttons
        document.querySelectorAll('.delete-alert').forEach(button => {
            button.addEventListener('click', async (e) => {
                try {
                    const alertCard = e.target.closest('.alert-card');
                    const alertId = alertCard.dataset.alertId;
                    
                    if (confirm('Are you sure you want to delete this alert?')) {
                        await CryptoAPI.deleteAlert(alertId);
                        alertCard.remove();
                        
                        if (document.querySelectorAll('.alert-card').length === 0) {
                            location.reload();
                        }
                        
                        CryptoUtils.showNotification('Alert deleted successfully', 'success');
                    }
                } catch (error) {
                    CryptoUtils.showNotification('Failed to delete alert', 'error');
                }
            });
        });
    }

    /**
     * Initialize charts on the page
     */
    initializeCharts() {
        // Main price chart
        const priceChart = document.getElementById('priceChart');
        if (priceChart) {
            this.loadChartData('24h');  // Default to 24h timeframe
        }

        // Mini charts in watchlist
        document.querySelectorAll('.mini-chart').forEach(async (canvas) => {
            try {
                const symbol = canvas.dataset.symbol;
                const data = await CryptoAPI.getHistoricalData(symbol, '24h');
                this.charts[`mini-${symbol}`] = CryptoCharts.createMiniChart(canvas, data);
            } catch (error) {
                console.error('Failed to create mini chart:', error);
            }
        });

        // Market dominance chart
        const dominanceChart = document.getElementById('marketDominanceChart');
        if (dominanceChart) {
            this.loadMarketDominance();
        }
    }

    /**
     * Load chart data for the main price chart
     * @param {string} timeframe - Time interval
     */
    async loadChartData(timeframe) {
        try {
            const symbol = document.querySelector('[data-crypto-symbol]').dataset.cryptoSymbol;
            const data = await CryptoAPI.getHistoricalData(symbol, timeframe);
            
            if (this.charts.price) {
                CryptoCharts.updateChartData(this.charts.price, data);
            } else {
                const canvas = document.getElementById('priceChart');
                this.charts.price = CryptoCharts.createPriceChart(canvas, data, { symbol });
            }
        } catch (error) {
            console.error('Failed to load chart data:', error);
        }
    }

    /**
     * Load market dominance data
     */
    async loadMarketDominance() {
        try {
            const stats = await CryptoAPI.getMarketStats();
            const canvas = document.getElementById('marketDominanceChart');
            this.charts.dominance = CryptoCharts.createMarketDominanceChart(canvas, stats.dominance);
        } catch (error) {
            console.error('Failed to load market dominance:', error);
        }
    }

    /**
     * Start real-time price updates
     */
    startPriceUpdates() {
        // Update cryptocurrency prices
        const updatePrices = async () => {
            document.querySelectorAll('[data-crypto-symbol]').forEach(async (element) => {
                try {
                    const symbol = element.dataset.cryptoSymbol;
                    const data = await CryptoAPI.getCryptocurrency(symbol);
                    
                    const priceElement = element.querySelector('.crypto-price');
                    const changeElement = element.querySelector('.price-change');
                    
                    if (priceElement) {
                        const oldPrice = parseFloat(priceElement.dataset.price);
                        const newPrice = data.current_price;
                        
                        if (oldPrice !== newPrice) {
                            priceElement.classList.add(newPrice > oldPrice ? 'price-up' : 'price-down');
                            setTimeout(() => priceElement.classList.remove('price-up', 'price-down'), 1000);
                            
                            priceElement.textContent = `$${CryptoUtils.formatCurrency(newPrice)}`;
                            priceElement.dataset.price = newPrice;
                        }
                    }
                    
                    if (changeElement) {
                        changeElement.textContent = `${data.price_change_24h > 0 ? '+' : ''}${data.price_change_24h.toFixed(2)}%`;
                        changeElement.className = `price-change ${data.price_change_24h > 0 ? 'text-success' : 'text-danger'}`;
                    }
                } catch (error) {
                    console.error('Failed to update price:', error);
                }
            });
        };

        // Update mini charts
        const updateMiniCharts = async () => {
            document.querySelectorAll('.mini-chart').forEach(async (canvas) => {
                try {
                    const symbol = canvas.dataset.symbol;
                    const data = await CryptoAPI.getHistoricalData(symbol, '24h');
                    CryptoCharts.updateChartData(this.charts[`mini-${symbol}`], data);
                } catch (error) {
                    console.error('Failed to update mini chart:', error);
                }
            });
        };

        // Start update intervals
        this.intervals.push(setInterval(updatePrices, this.updateInterval));
        this.intervals.push(setInterval(updateMiniCharts, this.updateInterval * 6));  // Update charts every minute
    }

    /**
     * Clean up intervals when leaving the page
     */
    destroy() {
        this.intervals.forEach(interval => clearInterval(interval));
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.cryptoTracker = new CryptoTracker();
});

// Clean up when leaving the page
window.addEventListener('beforeunload', () => {
    if (window.cryptoTracker) {
        window.cryptoTracker.destroy();
    }
});
