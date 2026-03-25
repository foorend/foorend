document.addEventListener('DOMContentLoaded', () => {
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