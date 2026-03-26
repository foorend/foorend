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

    function renderNewsGrid(container, sources) {
        const keys = Object.keys(sources);
        if (!keys.length) {
            container.innerHTML = '<p class="news-loading">뉴스를 준비 중입니다.</p>';
            return;
        }
        const grid = document.createElement('div');
        grid.className = 'news-grid';
        let hasItems = false;
        keys.forEach(key => {
            const src = sources[key];
            const items = src.items || [];
            if (!items.length) return;
            hasItems = true;
            const block = document.createElement('div');
            block.className = 'feed-source';
            block.innerHTML = `
                <div class="feed-source-header">
                    <h3 class="feed-source-name">${src.label}</h3>
                    <a href="${src.site}" class="feed-source-link" target="_blank" rel="noopener">더보기 →</a>
                </div>
                <ul class="feed-items">
                    ${items.map(item => `
                        <li class="feed-item">
                            <a href="${item.link}" class="feed-item-title" target="_blank" rel="noopener">${item.title}</a>
                            ${item.desc ? `<p class="feed-item-desc">${item.desc}</p>` : ''}
                        </li>
                    `).join('')}
                </ul>`;
            grid.appendChild(block);
        });
        if (!hasItems) {
            container.innerHTML = '<p class="news-loading">뉴스를 준비 중입니다.</p>';
            return;
        }
        container.innerHTML = '';
        container.appendChild(grid);
    }

    // Global news feeds
    const newsContainer = document.getElementById('news-feeds');
    // Korean news feeds
    const koreanNewsContainer = document.getElementById('korean-news-feeds');
    // Korean articles list
    const koreanArticlesList = document.getElementById('korean-articles-list');

    if (newsContainer || koreanNewsContainer || koreanArticlesList) {
        fetch('feeds.json')
            .then(r => r.json())
            .then(data => {
                if (newsContainer) {
                    renderNewsGrid(newsContainer, data.sources || {});
                }
                if (koreanNewsContainer) {
                    renderNewsGrid(koreanNewsContainer, data.korean_news || {});
                }
                if (koreanArticlesList) {
                    const articles = data.korean_articles || [];
                    if (!articles.length) {
                        koreanArticlesList.innerHTML = '<li class="articles-loading">아티클을 준비 중입니다.</li>';
                        return;
                    }
                    koreanArticlesList.innerHTML = articles.map(a => `
                        <li><a href="${a.link}" target="_blank" rel="noopener">${a.title}</a></li>
                    `).join('');
                }
            })
            .catch(() => {
                if (newsContainer) newsContainer.innerHTML = '<p class="news-loading">뉴스를 불러올 수 없습니다.</p>';
                if (koreanNewsContainer) koreanNewsContainer.innerHTML = '<p class="news-loading">뉴스를 불러올 수 없습니다.</p>';
                if (koreanArticlesList) koreanArticlesList.innerHTML = '<li class="articles-loading">아티클을 불러올 수 없습니다.</li>';
            });
    }

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