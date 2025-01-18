document.addEventListener('DOMContentLoaded', function() {
    // Handle watchlist toggle buttons
    document.querySelectorAll('.toggle-watchlist').forEach(button => {
        button.addEventListener('click', function() {
            const symbol = this.dataset.symbol;
            const icon = this.querySelector('i');
            const csrfToken = getCookie('csrftoken');
            
            // Make API call to toggle watchlist
            fetch(`/api/watchlist/toggle/${symbol}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
                credentials: 'same-origin'  // This is needed for the CSRF token to be sent
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'added') {
                    icon.classList.add('text-warning');
                    showToast('Success', `${symbol} added to watchlist!`, 'success');
                } else {
                    icon.classList.remove('text-warning');
                    showToast('Success', `${symbol} removed from watchlist!`, 'success');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (error.message.includes('401')) {
                    showToast('Error', 'Please log in to use the watchlist feature.', 'error');
                } else {
                    showToast('Error', 'Failed to update watchlist. Please try again.', 'error');
                }
            });
        });
    });
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Helper function to show toast notifications
function showToast(title, message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : 'success'} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <strong>${title}</strong><br>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    document.getElementById('toast-container').appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();

    // Remove the toast after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}
