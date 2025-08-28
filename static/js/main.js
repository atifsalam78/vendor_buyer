// main.js - Common JavaScript functionality for BazaarHub

document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    checkLoginStatus();
    
    // Initialize mobile menu toggle if it exists
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', function() {
            const navMenu = document.querySelector('.nav-menu');
            navMenu.classList.toggle('active');
        });
    }
    
    // Add dark mode toggle
    addDarkModeToggle();
    
    // Initialize dark mode based on user preference
    initDarkMode();
});

// Function to check if user is logged in
function checkLoginStatus() {
    const token = localStorage.getItem('token');
    const navLoginBtn = document.getElementById('nav-login-btn');
    const navProfileBtn = document.getElementById('nav-profile-btn');
    const navLogoutBtn = document.getElementById('nav-logout-btn');
    
    if (token) {
        // User is logged in
        if (navLoginBtn) navLoginBtn.style.display = 'none';
        if (navProfileBtn) navProfileBtn.style.display = 'inline-block';
        if (navLogoutBtn) navLogoutBtn.style.display = 'inline-block';
    } else {
        // User is not logged in
        if (navLoginBtn) navLoginBtn.style.display = 'inline-block';
        if (navProfileBtn) navProfileBtn.style.display = 'none';
        if (navLogoutBtn) navLogoutBtn.style.display = 'none';
    }
}

// Function to handle logout
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user_type');
    localStorage.removeItem('email');
    window.location.href = '/login';
}

// Dark mode functions
function addDarkModeToggle() {
    // Create dark mode toggle button
    const darkModeToggle = document.createElement('button');
    darkModeToggle.id = 'dark-mode-toggle';
    darkModeToggle.className = 'dark-mode-toggle';
    darkModeToggle.innerHTML = '<span>🌙</span>';
    darkModeToggle.title = 'Toggle Dark Mode';
    
    // Add to navbar
    const navContainer = document.querySelector('.nav-container');
    if (navContainer) {
        navContainer.appendChild(darkModeToggle);
        
        // Add event listener
        darkModeToggle.addEventListener('click', toggleDarkMode);
    }
}

function initDarkMode() {
    // Check if user has a preference
    const darkMode = localStorage.getItem('darkMode');
    
    // If dark mode was previously enabled, turn it on
    if (darkMode === 'enabled') {
        document.body.classList.add('dark-mode');
        updateDarkModeToggle(true);
    }
}

function toggleDarkMode() {
    // Toggle dark mode class on body
    document.body.classList.toggle('dark-mode');
    
    // Update localStorage based on current state
    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('darkMode', 'enabled');
        updateDarkModeToggle(true);
    } else {
        localStorage.setItem('darkMode', 'disabled');
        updateDarkModeToggle(false);
    }
}

function updateDarkModeToggle(isDarkMode) {
    const toggle = document.getElementById('dark-mode-toggle');
    if (toggle) {
        toggle.innerHTML = isDarkMode ? '<span>☀️</span>' : '<span>🌙</span>';
        toggle.title = isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode';
    }
}

// Add event listener to logout button if it exists
document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('nav-logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
});