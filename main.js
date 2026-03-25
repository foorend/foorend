document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('theme-toggle');
    const saved = localStorage.getItem('theme');
    if (saved === 'light') {
        document.body.classList.add('light');
        toggle.textContent = '☀️';
    }
    toggle.addEventListener('click', () => {
        document.body.classList.toggle('light');
        const isLight = document.body.classList.contains('light');
        toggle.textContent = isLight ? '☀️' : '🌙';
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
    });

    const form = document.getElementById('subscribe-form');
    const confirmationMessage = document.getElementById('confirmation-message');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const emailInput = document.getElementById('email');
        if (emailInput.value) {
            // Simulate a successful subscription
            form.classList.add('hidden');
            confirmationMessage.classList.remove('hidden');
        }
    });
});