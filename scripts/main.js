// Main JavaScript functionality for Sociail Assistant landing page

// Confetti celebration animation
function triggerConfetti() {
    // Respect reduced motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        return;
    }

    const container = document.createElement('div');
    container.className = 'confetti-container';
    document.body.appendChild(container);

    const rootStyles = getComputedStyle(document.documentElement);
    const cssVar = (name, fallback) => (rootStyles.getPropertyValue(name).trim() || fallback);

    const colors = [
        cssVar('--sociail-blue', '#0066ff'),
        cssVar('--sociail-yellow', '#f9d949'),
        cssVar('--success-color', '#34c759'),
        cssVar('--warning-color', '#ff9500'),
        cssVar('--error-color', '#ff3b30'),
        '#5856d6', // Purple accent
        '#00c7be'  // Teal accent
    ];

    const shapes = ['confetti-circle', 'confetti-square', 'confetti-ribbon'];
    const particleCount = 80;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        const shape = shapes[Math.floor(Math.random() * shapes.length)];
        const color = colors[Math.floor(Math.random() * colors.length)];

        particle.className = `confetti ${shape}`;
        particle.style.backgroundColor = color;
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${-10 - Math.random() * 20}%`;
        particle.style.animationDuration = `${2 + Math.random() * 2}s`;
        particle.style.animationDelay = `${Math.random() * 0.5}s`;

        // Add some horizontal drift
        const drift = (Math.random() - 0.5) * 200;
        particle.style.setProperty('--drift', `${drift}px`);

        container.appendChild(particle);
    }

    // Clean up after animation
    setTimeout(() => {
        container.remove();
    }, 5000);
}

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
    const planInput = form.querySelector('input[name="plan"]');
    const status = form.parentElement?.querySelector('.form-status');
    const submitButton = form.querySelector('button[type="submit"]');
    const email = emailInput.value.trim();
    const plan = planInput ? planInput.value.trim() : '';

    if (planInput && !plan) {
        if (status) {
            status.textContent = 'Please select an option.';
            status.classList.add('error');
        }
        return;
    }
    const originalLabel = submitButton.textContent;

    if (status) {
        status.textContent = '';
        status.classList.remove('success', 'error');
    }

    if (!plan) {
        if (status) {
            status.textContent = 'Please select an option to continue.';
            status.classList.add('error');
        }
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent = originalLabel;
        }
        return;
    }

    submitButton.disabled = true;
    submitButton.classList.add('loading');
    submitButton.textContent = 'Sending...';

    try {
        const response = await fetch('/api/subscribe', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, plan })
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

        triggerConfetti();
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
        submitButton.classList.remove('loading');
        submitButton.textContent = originalLabel;
    }
}

// Space bubble interaction
document.querySelectorAll('.space-bubble').forEach(bubble => {
    bubble.addEventListener('click', function() {
        bubble.classList.add('is-popping');
        setTimeout(() => {
            bubble.classList.remove('is-popping');
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
    const planInput = document.querySelector('input[name="plan"]');
    const pricingCards = document.querySelectorAll('.pricing-card');
    const revealGroups = [
        { selector: '.features-grid .feature-card', step: 80 },
        { selector: '.mobility-grid .mobility-box', step: 80 },
        { selector: '.spaces-visual .space-bubble', step: 80 },
        { selector: '.pricing-grid .pricing-card', step: 80 },
        { selector: '.trust-signals .trust-signal', step: 60 }
    ];

    revealGroups.forEach(({ selector, step }) => {
        document.querySelectorAll(selector).forEach((item, index) => {
            item.classList.add('reveal');
            item.style.setProperty('--reveal-delay', `${index * step}ms`);
        });
    });

    const revealTargets = document.querySelectorAll('.reveal');

    pricingCards.forEach((card) => {
        const planValue = card.getAttribute('data-plan') || '';
        card.setAttribute('aria-pressed', card.classList.contains('selected') ? 'true' : 'false');

        card.addEventListener('click', () => {
            if (planInput) {
                pricingCards.forEach(c => {
                    c.classList.remove('selected');
                    c.setAttribute('aria-pressed', 'false');
                });
                card.classList.add('selected');
                card.setAttribute('aria-pressed', 'true');
                planInput.value = planValue;
            }
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

    if (revealTargets.length) {
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (prefersReducedMotion) {
            revealTargets.forEach(el => el.classList.add('in-view'));
        } else {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('in-view');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.2 });

            revealTargets.forEach(el => observer.observe(el));
        }
    }
});
