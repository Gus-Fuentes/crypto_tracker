/**
 * API service for the Crypto Tracker application
 */

const CryptoAPI = {
    /**
     * Base configuration for API requests
     */
    config: {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value
        }
    },

    /**
     * Fetch cryptocurrency data
     * @param {string} symbol - Cryptocurrency symbol
     * @returns {Promise} Promise that resolves with cryptocurrency data
     */
    getCryptocurrency: async function(symbol) {
        try {
            const response = await fetch(`/api/cryptocurrencies/${symbol}/`);
            if (!response.ok) throw new Error('Failed to fetch cryptocurrency');
            return await response.json();
        } catch (error) {
            console.error('Error fetching cryptocurrency:', error);
            throw error;
        }
    },

    /**
     * Fetch historical price data
     * @param {string} symbol - Cryptocurrency symbol
     * @param {string} interval - Time interval (1h, 24h, 7d, 30d)
     * @returns {Promise} Promise that resolves with historical data
     */
    getHistoricalData: async function(symbol, interval) {
        try {
            const response = await fetch(`/api/cryptocurrencies/${symbol}/history/?interval=${interval}`);
            if (!response.ok) throw new Error('Failed to fetch historical data');
            return await response.json();
        } catch (error) {
            console.error('Error fetching historical data:', error);
            throw error;
        }
    },

    /**
     * Toggle watchlist status for a cryptocurrency
     * @param {string} symbol - Cryptocurrency symbol
     * @returns {Promise} Promise that resolves with updated watchlist status
     */
    toggleWatchlist: async function(symbol) {
        try {
            const response = await fetch(`/api/watchlist/toggle/${symbol}/`, {
                method: 'POST',
                ...this.config
            });
            if (!response.ok) throw new Error('Failed to toggle watchlist');
            return await response.json();
        } catch (error) {
            console.error('Error toggling watchlist:', error);
            throw error;
        }
    },

    /**
     * Create a price alert
     * @param {string} symbol - Cryptocurrency symbol
     * @param {object} alertData - Alert configuration
     * @returns {Promise} Promise that resolves with created alert data
     */
    createAlert: async function(symbol, alertData) {
        try {
            const response = await fetch(`/api/alerts/create/${symbol}/`, {
                method: 'POST',
                ...this.config,
                body: JSON.stringify(alertData)
            });
            if (!response.ok) throw new Error('Failed to create alert');
            return await response.json();
        } catch (error) {
            console.error('Error creating alert:', error);
            throw error;
        }
    },

    /**
     * Delete a price alert
     * @param {number} alertId - Alert ID
     * @returns {Promise} Promise that resolves when alert is deleted
     */
    deleteAlert: async function(alertId) {
        try {
            const response = await fetch(`/api/alerts/${alertId}/`, {
                method: 'DELETE',
                ...this.config
            });
            if (!response.ok) throw new Error('Failed to delete alert');
            return true;
        } catch (error) {
            console.error('Error deleting alert:', error);
            throw error;
        }
    },

    /**
     * Get market statistics
     * @returns {Promise} Promise that resolves with market statistics
     */
    getMarketStats: async function() {
        try {
            const response = await fetch('/api/market/stats/');
            if (!response.ok) throw new Error('Failed to fetch market stats');
            return await response.json();
        } catch (error) {
            console.error('Error fetching market stats:', error);
            throw error;
        }
    }
};
