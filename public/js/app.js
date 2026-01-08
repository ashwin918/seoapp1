// SEO Bot - Main JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(function () {
                alert.remove();
            }, 300);
        }, 5000);
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                const originalText = submitBtn.innerHTML;
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

                // Re-enable after 10 seconds in case of error
                setTimeout(function () {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 10000);
            }
        });
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm(btn.dataset.confirm || 'Are you sure?')) {
                e.preventDefault();
            }
        });
    });

    // Copy to clipboard
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const text = btn.dataset.copy;
            navigator.clipboard.writeText(text).then(function () {
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                setTimeout(function () {
                    btn.innerHTML = originalText;
                }, 2000);
            });
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Initialize score animations
    const scoreCircles = document.querySelectorAll('.score-circle-progress');
    scoreCircles.forEach(function (circle) {
        const dasharray = circle.getAttribute('stroke-dasharray');
        circle.setAttribute('stroke-dasharray', '0 427');
        setTimeout(function () {
            circle.setAttribute('stroke-dasharray', dasharray);
        }, 100);
    });

    // Initialize score bar animations
    const scoreBars = document.querySelectorAll('.score-bar-fill');
    scoreBars.forEach(function (bar) {
        const width = bar.style.width;
        bar.style.width = '0';
        setTimeout(function () {
            bar.style.width = width;
        }, 100);
    });

    // Mobile menu toggle (if needed)
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const sidebar = document.querySelector('.sidebar');
    if (mobileMenuBtn && sidebar) {
        mobileMenuBtn.addEventListener('click', function () {
            sidebar.classList.toggle('show');
        });
    }

    // Dropdown menus
    const dropdownBtns = document.querySelectorAll('.dropdown-btn');
    dropdownBtns.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.stopPropagation();
            const dropdown = btn.nextElementSibling;
            dropdown.classList.toggle('show');
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function () {
        document.querySelectorAll('.dropdown-menu.show').forEach(function (menu) {
            menu.classList.remove('show');
        });
    });

    // Auto-fill character counts
    document.querySelectorAll('[data-char-count]').forEach(function (input) {
        const countEl = document.getElementById(input.dataset.charCount);
        if (countEl) {
            input.addEventListener('input', function () {
                countEl.textContent = input.value.length + ' characters';
            });
            // Initial count
            countEl.textContent = input.value.length + ' characters';
        }
    });

    console.log('SEO Bot initialized');
});

// Quick analyze function (for API usage)
async function quickAnalyze(url) {
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });

        if (!response.ok) {
            throw new Error('Analysis failed');
        }

        return await response.json();
    } catch (error) {
        console.error('Quick analyze error:', error);
        throw error;
    }
}

// Get stats function
async function getStats() {
    try {
        const response = await fetch('/api/stats');
        if (!response.ok) {
            throw new Error('Failed to get stats');
        }
        return await response.json();
    } catch (error) {
        console.error('Get stats error:', error);
        throw error;
    }
}
