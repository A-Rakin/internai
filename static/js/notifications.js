/**
 * ============================================================
 * InternAI - Notification Handling
 * ============================================================
 * Manages notification badge counts, mark-as-read functionality,
 * notification dropdown population, and real-time updates.
 * ============================================================
 */

document.addEventListener('DOMContentLoaded', function() {

    // ============================================================
    // 1. NOTIFICATION BADGE COUNT
    // ============================================================

    // Get the notification badge element
    const notifBadge = document.querySelector('.badge-count');

    /**
     * Update the notification badge count.
     * Hides the badge when count is 0.
     *
     * @param {number} count - The number of unread notifications
     */
    function updateBadgeCount(count) {
        if (notifBadge) {
            if (count > 0) {
                // Show the badge with the count
                notifBadge.textContent = count > 99 ? '99+' : count;
                notifBadge.style.display = 'flex';
            } else {
                // Hide the badge when no unread notifications
                notifBadge.style.display = 'none';
            }
        }
    }

    // ============================================================
    // 2. MARK NOTIFICATION AS READ
    // ============================================================

    /**
     * Mark a single notification as read via AJAX.
     *
     * @param {number} notificationId - The ID of the notification
     * @param {HTMLElement} element - The notification DOM element
     */
    function markAsRead(notificationId, element) {
        // Send AJAX request to mark as read
        fetch('/notifications/' + notificationId + '/read/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': window.csrfToken,   // Include CSRF token
                'Content-Type': 'application/json',
            },
        })
        .then(function(response) {
            if (response.ok) {
                // Remove 'unread' styling from the notification element
                if (element) {
                    element.classList.remove('unread');
                }

                // Update the badge count
                const currentCount = parseInt(notifBadge?.textContent) || 0;
                updateBadgeCount(currentCount - 1);
            }
        })
        .catch(function(error) {
            // Log error but don't disrupt user experience
            console.error('Failed to mark notification as read:', error);
        });
    }

    // ============================================================
    // 3. MARK ALL NOTIFICATIONS AS READ
    // ============================================================

    // Find the "Mark all as read" button
    const markAllBtn = document.querySelector('.mark-all-read');

    if (markAllBtn) {
        markAllBtn.addEventListener('click', function() {
            // Send AJAX request to mark all as read
            fetch('/notifications/mark-all-read/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': window.csrfToken,
                    'Content-Type': 'application/json',
                },
            })
            .then(function(response) {
                if (response.ok) {
                    // Remove 'unread' class from all notification items
                    const unreadItems = document.querySelectorAll('.notification-item.unread');
                    unreadItems.forEach(function(item) {
                        item.classList.remove('unread');
                    });

                    // Reset badge count to 0
                    updateBadgeCount(0);
                }
            })
            .catch(function(error) {
                console.error('Failed to mark all notifications as read:', error);
            });
        });
    }

    // ============================================================
    // 4. NOTIFICATION ITEM CLICK HANDLER
    // ============================================================

    // Add click handler to all notification items
    const notifItems = document.querySelectorAll('.notification-item');

    notifItems.forEach(function(item) {
        item.addEventListener('click', function() {
            // Get the notification ID from data attribute
            const notifId = this.dataset.notificationId;
            // Get the link to navigate to
            const link = this.dataset.link;

            // Mark as read if currently unread
            if (this.classList.contains('unread') && notifId) {
                markAsRead(notifId, this);
            }

            // Navigate to the related page if link exists
            if (link) {
                window.location.href = link;
            }
        });
    });

    // ============================================================
    // 5. NOTIFICATION TIME AGO
    // ============================================================

    /**
     * Convert a timestamp to a human-readable "time ago" string.
     *
     * @param {string} timestamp - ISO timestamp string
     * @returns {string} - Human-readable time difference
     */
    function timeAgo(timestamp) {
        // Parse the timestamp
        const date = new Date(timestamp);
        const now = new Date();

        // Calculate the difference in seconds
        const seconds = Math.floor((now - date) / 1000);

        // Define time intervals in seconds
        const intervals = {
            year: 31536000,
            month: 2592000,
            week: 604800,
            day: 86400,
            hour: 3600,
            minute: 60,
        };

        // Find the appropriate interval
        for (const [unit, secondsInUnit] of Object.entries(intervals)) {
            const count = Math.floor(seconds / secondsInUnit);
            if (count >= 1) {
                return count + ' ' + unit + (count > 1 ? 's' : '') + ' ago';
            }
        }

        // Less than a minute
        return 'Just now';
    }

    // Update all time-ago elements
    const timeAgoElements = document.querySelectorAll('[data-timestamp]');
    timeAgoElements.forEach(function(el) {
        const timestamp = el.dataset.timestamp;
        if (timestamp) {
            el.textContent = timeAgo(timestamp);
        }
    });

    // ============================================================
    // 6. AUTO-REFRESH NOTIFICATION COUNT
    // ============================================================

    /**
     * Periodically check for new notifications.
     * Polls the server every 60 seconds for unread count.
     */
    function checkNotifications() {
        fetch('/notifications/unread-count/', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            if (data.count !== undefined) {
                updateBadgeCount(data.count);
            }
        })
        .catch(function(error) {
            // Silently fail - don't disrupt user experience
            console.debug('Notification check failed:', error);
        });
    }

    // Check for new notifications every 60 seconds
    // Only if the user is on a portal page (not landing)
    if (notifBadge) {
        setInterval(checkNotifications, 60000); // 60000ms = 60 seconds
    }

}); // End DOMContentLoaded
