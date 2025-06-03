// Main JavaScript functionality for Sociail Assistant landing page

// Smooth scrolling for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Form handler
function handleSubmit(e) {
    e.preventDefault();
    const email = e.target.querySelector('input').value;
    alert(`Thanks for your interest! We'll notify ${email} when Sociail Assistant launches.`);
    e.target.reset();
}

// Space bubble interaction
document.querySelectorAll('.space-bubble').forEach(bubble => {
    bubble.addEventListener('click', function() {
        const spaceName = this.textContent.trim().split('\n')[1];
        this.style.transform = 'scale(1.1)';
        setTimeout(() => {
            this.style.transform = '';
        }, 300);
    });
});

// Theme toggle functionality
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (currentTheme === null) {
        // No theme set, use opposite of system preference
        document.documentElement.setAttribute('data-theme', prefersDark ? 'light' : 'dark');
    } else if (currentTheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
    }
    
    // Store preference
    localStorage.setItem('theme', document.documentElement.getAttribute('data-theme'));
    updateThemeIcon();
}

function updateThemeIcon() {
    const themeButton = document.querySelector('.theme-switch');
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const isDark = currentTheme === 'dark' || (currentTheme === null && prefersDark);
    
    themeButton.innerHTML = isDark ? 
        `<svg class="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>` :
        `<svg class="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>`;
}

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    }
    updateThemeIcon();
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function() {
        if (!document.documentElement.getAttribute('data-theme')) {
            updateThemeIcon();
        }
    });
});
