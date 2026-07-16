/**
 * ============================================================
 * InternAI - Sidebar JavaScript
 * ============================================================
 * Handles sidebar collapse/expand functionality,
 * active menu detection, and mobile overlay behavior.
 * ============================================================
 */

document.addEventListener('DOMContentLoaded', function() {

    // ============================================================
    // 1. SIDEBAR COLLAPSE/EXPAND (DESKTOP)
    // ============================================================

    // Get references to sidebar elements
    const sidebar = document.getElementById('sidebar');
    const collapseBtn = document.getElementById('sidebarCollapse');

    // Only proceed if sidebar exists (portal pages only)
    if (collapseBtn && sidebar) {
        collapseBtn.addEventListener('click', function() {
            // Toggle the collapsed state on the body
            document.body.classList.toggle('sidebar-collapsed');

            // Store the preference in localStorage
            const isCollapsed = document.body.classList.contains('sidebar-collapsed');
            localStorage.setItem('sidebarCollapsed', isCollapsed);
        });

        // Restore sidebar state from localStorage on page load
        const savedState = localStorage.getItem('sidebarCollapsed');
        if (savedState === 'true') {
            document.body.classList.add('sidebar-collapsed');
        }
    }

    // ============================================================
    // 2. MOBILE SIDEBAR TOGGLE
    // ============================================================

    // Get the mobile hamburger menu button
    const mobileToggle = document.getElementById('sidebarToggle');
    const overlay = document.getElementById('sidebarOverlay');

    if (mobileToggle && sidebar) {
        // Open sidebar on hamburger click
        mobileToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
            if (overlay) overlay.classList.toggle('show');
        });
    }

    // Close sidebar on overlay click (mobile)
    if (overlay) {
        overlay.addEventListener('click', function() {
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
        });
    }

    // Close sidebar on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar && sidebar.classList.contains('show')) {
            sidebar.classList.remove('show');
            if (overlay) overlay.classList.remove('show');
        }
    });

    // ============================================================
    // 3. ACTIVE MENU ITEM DETECTION
    // ============================================================

    /**
     * Detect which sidebar menu item corresponds to the current
     * page URL and highlight it as active.
     */
    function setActiveMenuItem() {
        // Get the current page path
        const path = window.location.pathname;

        // Find all sidebar nav links
        const navLinks = document.querySelectorAll('.sidebar-nav .nav-link');

        // Track the best match (longest matching path)
        let bestMatch = null;
        let bestMatchLength = 0;

        navLinks.forEach(function(link) {
            // Get the link's href
            const href = link.getAttribute('href');

            // Skip links without href or with '#'
            if (!href || href === '#') return;

            // Check if the current path starts with this link's href
            if (path.startsWith(href) && href.length > bestMatchLength) {
                bestMatch = link;
                bestMatchLength = href.length;
            }
        });

        // If a match was found, set it as active
        if (bestMatch) {
            // Remove active class from all links
            navLinks.forEach(function(link) {
                link.classList.remove('active');
            });
            // Add active class to the best match
            bestMatch.classList.add('active');
        }
    }

    // Run active menu detection
    setActiveMenuItem();

    // ============================================================
    // 4. SIDEBAR SUBMENU TOGGLE
    // ============================================================

    // Find all submenu toggle links
    const submenuToggles = document.querySelectorAll('.has-submenu');

    submenuToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();

            // Find the associated submenu
            const submenu = this.nextElementSibling;

            if (submenu && submenu.classList.contains('submenu')) {
                // Toggle submenu visibility
                submenu.classList.toggle('show');

                // Toggle the arrow icon direction
                const arrow = this.querySelector('.submenu-arrow');
                if (arrow) {
                    arrow.classList.toggle('rotated');
                }
            }
        });
    });

    // ============================================================
    // 5. RESIZE HANDLER
    // ============================================================

    // Handle window resize events
    let resizeTimer;
    window.addEventListener('resize', function() {
        // Debounce the resize handler
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            // If window is wider than 991px, remove mobile classes
            if (window.innerWidth > 991) {
                if (sidebar) sidebar.classList.remove('show');
                if (overlay) overlay.classList.remove('show');
            }
        }, 250); // Wait 250ms after last resize event
    });

}); // End DOMContentLoaded
