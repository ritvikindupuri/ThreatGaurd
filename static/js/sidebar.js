document.addEventListener('DOMContentLoaded', () => {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const menuIcons = document.querySelectorAll('.nav-item i');
    const customHamburger = document.querySelector('.custom-hamburger');
    const mobileMenuButton = document.getElementById('mobile-menu-button');

    // Function to set sidebar state
    function setSidebarState(isCollapsed) {
        sidebar.classList.toggle('collapsed', isCollapsed);
        mainContent.classList.toggle('expanded', isCollapsed);
        
        // Center icons when sidebar is collapsed
        menuIcons.forEach(icon => {
            icon.parentElement.classList.toggle('text-center', isCollapsed);
        });

        // Adjust the width of the Overview container
        const overviewContainer = document.querySelector('.main-content > .container-fluid');
        if (overviewContainer) {
            overviewContainer.style.width = isCollapsed ? 'calc(100% - 80px)' : 'calc(100% - 250px)';
        }

        // Center the toggle button when sidebar is collapsed
        const toggleContainer = sidebarToggle.parentElement;
        toggleContainer.style.justifyContent = isCollapsed ? 'center' : 'flex-start';

        // Save state to localStorage
        localStorage.setItem('sidebarCollapsed', isCollapsed);
    }

    if (sidebarToggle && sidebar && mainContent && customHamburger) {
        // Load initial state from localStorage
        const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        
        // Set initial state without animation
        sidebar.style.transition = 'none';
        mainContent.style.transition = 'none';
        setSidebarState(isCollapsed);
        
        // Re-enable transitions after a short delay
        setTimeout(() => {
            sidebar.style.transition = '';
            mainContent.style.transition = '';
        }, 50);

        sidebarToggle.addEventListener('click', () => {
            const newState = !sidebar.classList.contains('collapsed');
            setSidebarState(newState);
        });
    }

    // Mobile menu functionality removed as per request
});