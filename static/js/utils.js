/**
 * Utility functions for the Crypto Tracker application
 */

const CryptoUtils = {
    /**
     * Format a number as currency
     * @param {number} number - Number to format
     * @param {number} decimals - Number of decimal places
     * @returns {string} Formatted currency string
     */
    formatCurrency: function(number, decimals = 2) {
        return new Intl.NumberFormat('en-US', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        }).format(number);
    },

    /**
     * Format a large number with appropriate suffix (K, M, B, T)
     * @param {number} number - Number to format
     * @returns {string} Formatted number with suffix
     */
    formatLargeNumber: function(number) {
        const suffixes = ['', 'K', 'M', 'B', 'T'];
        const suffixNum = Math.floor((''+number).length/3);
        let shortValue = parseFloat((suffixNum != 0 ? (number / Math.pow(1000,suffixNum)) : number).toPrecision(2));
        if (shortValue % 1 !== 0) {
            shortValue = shortValue.toFixed(1);
        }
        return shortValue + suffixes[suffixNum];
    },

    /**
     * Calculate percentage change between two values
     * @param {number} currentValue - Current value
     * @param {number} previousValue - Previous value
     * @returns {number} Percentage change
     */
    calculatePercentageChange: function(currentValue, previousValue) {
        return ((currentValue - previousValue) / previousValue) * 100;
    },

    /**
     * Format a timestamp into a readable date string
     * @param {string} timestamp - ISO timestamp
     * @param {boolean} includeTime - Whether to include time
     * @returns {string} Formatted date string
     */
    formatDate: function(timestamp, includeTime = true) {
        const date = new Date(timestamp);
        const options = {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            ...(includeTime && {
                hour: '2-digit',
                minute: '2-digit'
            })
        };
        return date.toLocaleDateString('en-US', options);
    },

    /**
     * Generate gradient colors for charts
     * @param {string} color - Base color in hex
     * @returns {object} Gradient object for Chart.js
     */
    createGradient: function(ctx, color) {
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, `${color}33`);  // 20% opacity
        gradient.addColorStop(1, `${color}00`);  // 0% opacity
        return gradient;
    },

    /**
     * Debounce function to limit the rate at which a function is called
     * @param {Function} func - Function to debounce
     * @param {number} wait - Time to wait in milliseconds
     * @returns {Function} Debounced function
     */
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Show a toast notification
     * @param {string} message - Message to display
     * @param {string} type - Type of notification (success, error, warning, info)
     */
    showNotification: function(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        const container = document.getElementById('toast-container') || (() => {
            const div = document.createElement('div');
            div.id = 'toast-container';
            div.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(div);
            return div;
        })();
        
        container.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        toast.addEventListener('hidden.bs.toast', () => toast.remove());
    }
};
