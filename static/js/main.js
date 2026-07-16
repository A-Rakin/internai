/**
 * ============================================================
 * InternAI - Main JavaScript
 * ============================================================
 * Global JavaScript functionality including sidebar toggle,
 * notification handling, tooltips, CSRF token setup,
 * and alert auto-dismiss.
 * ============================================================
 */

// Wait for the DOM to be fully loaded before executing scripts
document.addEventListener('DOMContentLoaded', function() {

    // ============================================================
    // 1. SIDEBAR TOGGLE
    // ============================================================

    // Get the sidebar toggle button element
    const sidebarToggle = document.getElementById('sidebarToggle');

    // Get the sidebar element
    const sidebar = document.getElementById('sidebar');

    // Get the sidebar overlay element (for mobile)
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    // Only attach event listener if toggle button exists
    if (sidebarToggle && sidebar) {
        // Toggle sidebar visibility when button is clicked
        sidebarToggle.addEventListener('click', function() {
            // Toggle the 'show' class on sidebar for mobile
            sidebar.classList.toggle('show');

            // Toggle the overlay visibility
            if (sidebarOverlay) {
                sidebarOverlay.classList.toggle('show');
            }

            // Toggle body class for sidebar collapsed state (desktop)
            document.body.classList.toggle('sidebar-collapsed');
        });
    }

    // Close sidebar when overlay is clicked (mobile)
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            // Remove 'show' class from sidebar
            sidebar.classList.remove('show');
            // Remove 'show' class from overlay
            sidebarOverlay.classList.remove('show');
        });
    }

    // ============================================================
    // 2. NAVBAR SCROLL EFFECT (Landing Page)
    // ============================================================

    // Get the landing page navbar
    const landingNavbar = document.querySelector('.landing-navbar');

    // Only attach scroll listener if landing navbar exists
    if (landingNavbar) {
        // Listen for scroll events on the window
        window.addEventListener('scroll', function() {
            // Add 'scrolled' class when page is scrolled down 50px
            if (window.scrollY > 50) {
                landingNavbar.classList.add('scrolled');
            } else {
                // Remove 'scrolled' class when at the top
                landingNavbar.classList.remove('scrolled');
            }
        });
    }

    // ============================================================
    // 3. ACTIVE SIDEBAR LINK
    // ============================================================

    // Get the current page URL path
    const currentPath = window.location.pathname;

    // Get all sidebar navigation links
    const sidebarLinks = document.querySelectorAll('.sidebar-nav .nav-link');

    // Loop through each link and check if it matches the current URL
    sidebarLinks.forEach(function(link) {
        // Get the href attribute of the link
        const linkPath = link.getAttribute('href');

        // If the current path starts with the link path, mark it as active
        if (linkPath && currentPath.startsWith(linkPath)) {
            // Remove 'active' class from all links first
            sidebarLinks.forEach(function(l) {
                l.classList.remove('active');
            });
            // Add 'active' class to the matching link
            link.classList.add('active');
        }
    });

    // ============================================================
    // 4. BOOTSTRAP TOOLTIPS INITIALIZATION
    // ============================================================

    // Find all elements with data-bs-toggle="tooltip" attribute
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');

    // Initialize Bootstrap tooltip for each element
    tooltipTriggerList.forEach(function(tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ============================================================
    // 5. BOOTSTRAP POPOVERS INITIALIZATION
    // ============================================================

    // Find all elements with data-bs-toggle="popover" attribute
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');

    // Initialize Bootstrap popover for each element
    popoverTriggerList.forEach(function(popoverTriggerEl) {
        new bootstrap.Popover(popoverTriggerEl);
    });

    // ============================================================
    // 6. AUTO-DISMISS ALERTS
    // ============================================================

    // Find all alert messages that should auto-dismiss
    const alerts = document.querySelectorAll('.alert-dismissible');

    // Auto-dismiss each alert after 5 seconds
    alerts.forEach(function(alert) {
        setTimeout(function() {
            // Use Bootstrap's alert API to close it
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000); // 5000ms = 5 seconds
    });

    // ============================================================
    // 7. CSRF TOKEN SETUP FOR AJAX
    // ============================================================

    /**
     * Get the CSRF token from cookies.
     * Required for making POST/PUT/DELETE requests via AJAX.
     * Django's CSRF middleware validates this token.
     *
     * @param {string} name - The cookie name to look for
     * @returns {string|null} - The cookie value or null
     */
    function getCookie(name) {
        // Initialize the value as null
        let cookieValue = null;

        // Check if cookies exist and are not empty
        if (document.cookie && document.cookie !== '') {
            // Split all cookies by semicolons
            const cookies = document.cookie.split(';');

            // Loop through each cookie
            for (let i = 0; i < cookies.length; i++) {
                // Trim whitespace from the cookie
                const cookie = cookies[i].trim();

                // Check if this cookie starts with the name we're looking for
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    // Decode and extract the cookie value
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        // Return the cookie value (or null if not found)
        return cookieValue;
    }

    // Store the CSRF token for use in AJAX requests
    window.csrfToken = getCookie('csrftoken');

    // ============================================================
    // 8. SMOOTH SCROLL FOR ANCHOR LINKS
    // ============================================================

    // Find all anchor links that point to an ID on the same page
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');

    // Add smooth scrolling behavior to each anchor link
    smoothScrollLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            // Get the target element ID from the href
            const targetId = this.getAttribute('href');

            // Skip if href is just '#'
            if (targetId === '#') return;

            // Find the target element
            const targetElement = document.querySelector(targetId);

            // If target element exists, scroll to it smoothly
            if (targetElement) {
                e.preventDefault(); // Prevent default jump
                targetElement.scrollIntoView({
                    behavior: 'smooth',   // Smooth animation
                    block: 'start',       // Align to top
                });
            }
        });
    });

    // ============================================================
    // 9. COUNTER ANIMATION (Landing Page Stats)
    // ============================================================

    /**
     * Animate a number counting up from 0 to target value.
     * Used for the statistics section on the landing page.
     *
     * @param {HTMLElement} element - The element to animate
     * @param {number} target - The target number
     * @param {number} duration - Animation duration in milliseconds
     */
    function animateCounter(element, target, duration) {
        // Starting value
        let start = 0;
        // Calculate increment based on 60fps
        const increment = target / (duration / 16);
        // Current value tracker
        let current = start;

        // Animation function called on each frame
        function updateCounter() {
            // Increment the current value
            current += increment;

            // Check if we've reached the target
            if (current >= target) {
                // Set to exact target value
                element.textContent = target.toLocaleString();
            } else {
                // Update displayed value (rounded)
                element.textContent = Math.floor(current).toLocaleString();
                // Request next animation frame
                requestAnimationFrame(updateCounter);
            }
        }

        // Start the animation
        updateCounter();
    }

    // ============================================================
    // 10. INTERSECTION OBSERVER FOR ANIMATIONS
    // ============================================================

    // Create an Intersection Observer to trigger animations when
    // elements come into the viewport (scroll into view)
    const observerOptions = {
        root: null,            // Use the viewport as the root
        rootMargin: '0px',     // No margin
        threshold: 0.1,        // Trigger when 10% of element is visible
    };

    // Create the observer
    const animationObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            // When element enters the viewport
            if (entry.isIntersecting) {
                // Add the 'animate-fade-in' class to trigger animation
                entry.target.classList.add('animate-fade-in');

                // If it's a counter element, start counting
                if (entry.target.classList.contains('counter')) {
                    const target = parseInt(entry.target.getAttribute('data-target'));
                    if (target) {
                        animateCounter(entry.target, target, 2000);
                    }
                }

                // Stop observing this element (animate only once)
                animationObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all elements with the 'animate-on-scroll' class
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    animateElements.forEach(function(el) {
        animationObserver.observe(el);
    });

    // Observe all counter elements
    const counterElements = document.querySelectorAll('.counter');
    counterElements.forEach(function(el) {
        animationObserver.observe(el);
    });

    // ============================================================
    // 11. MOBILE MENU CLOSE ON LINK CLICK
    // ============================================================

    // On mobile, close the navbar when a link is clicked
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            // If the navbar collapse element exists and is shown
            if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                // Use Bootstrap's collapse API to hide it
                const bsCollapse = bootstrap.Collapse.getOrCreateInstance(navbarCollapse);
                bsCollapse.hide();
            }
        });
    });

}); // End DOMContentLoaded
