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
            form.classList.add('hidden');
            confirmationMessage.classList.remove('hidden');
        }
    });

    const contactForm = document.getElementById('contact-form');
    const contactConfirmation = document.getElementById('contact-confirmation');
    const contactSubmit = document.getElementById('contact-submit');

    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        contactSubmit.disabled = true;
        contactSubmit.textContent = '전송 중...';

        const res = await fetch(contactForm.action, {
            method: 'POST',
            body: new FormData(contactForm),
            headers: { 'Accept': 'application/json' }
        });

        if (res.ok) {
            contactForm.classList.add('hidden');
            contactConfirmation.classList.remove('hidden');
        } else {
            contactSubmit.disabled = false;
            contactSubmit.textContent = '문의 보내기';
            alert('전송에 실패했습니다. 잠시 후 다시 시도해주세요.');
        }
    });
});