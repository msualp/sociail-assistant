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
async function handleSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const emailInput = form.querySelector('input[type="email"]');
    const status = form.parentElement?.querySelector('.form-status');
    const submitButton = form.querySelector('button[type="submit"]');
    const email = emailInput.value.trim();
    const originalLabel = submitButton.textContent;

    if (status) {
        status.textContent = '';
        status.classList.remove('success', 'error');
    }

    submitButton.disabled = true;
    submitButton.textContent = 'Sending...';

    try {
        const response = await fetch('/api/subscribe', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });

        if (!response.ok) {
            const data = await response.json().catch(() => ({}));
            throw new Error(data.error || 'Something went wrong. Please try again.');
        }

        if (status) {
            status.textContent = 'Thanks! We will be in touch soon.';
            status.classList.add('success');
        } else {
            alert('Thanks! We will be in touch soon.');
        }

        form.reset();
    } catch (error) {
        if (status) {
            status.textContent = error.message || 'Something went wrong. Please try again.';
            status.classList.add('error');
        } else {
            alert('Something went wrong. Please try again.');
        }
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = originalLabel;
    }
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

    const emailInput = document.querySelector('.email-input');
    const pricingCards = document.querySelectorAll('.pricing-card');

    pricingCards.forEach(card => {
        card.addEventListener('click', () => {
            if (emailInput) {
                emailInput.focus();
                emailInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });

        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                card.click();
            }
        });
    });
});
