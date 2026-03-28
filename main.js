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

    // ── Language toggle ──────────────────────────────────────────
    const translations = {
        ko: {
            heroWelcome: `FOOREND's Food Trend Archive에 오신 것을 환영합니다✨<br><br>이 페이지는 단순한 뉴스 모음이 아닙니다.<br>FOOREND는 2022년, 백화점 F&B팀 바이어로 일하던 Alex가 퇴사 후에도 현업의 감각을 잃지 않기 위해 시작한 국내외 F&B 비즈니스 뉴스 클리핑에서 출발했습니다. 그 기록이 쌓이고 쌓여, 지금은 메일 뉴스레터 구독자 3,500+, 인스타그램 팔로워 4,900+, 카카오톡 레터 구독자 1,000+분들과 함께하는 FOOREND가 되었고요.<br><br>이 아카이브 페이지는 그 루틴을 그대로 공개한 공간입니다.<br>매주 어떤 매체에서, 어떤 뉴스를 보고, 그 안에서 무엇을 클리핑하는지. FOOREND가 200건이 넘는 뉴스레터를 발행해오며 쌓아온 정보 탐색의 루틴을 담았습니다. 여기에 더해, 그 매체들의 뉴스가 3시간마다 자동으로 업데이트되도록 구성해두었습니다.<br><br>F&B 현업에 계신 분들께는 빠르게 트렌드를 짚을 수 있는 레퍼런스로, 크리에이터분들께는 콘텐츠 아이디어의 출발점으로, 이 업계에 관심을 갖기 시작한 분들께는 넓고 깊은 시야를 열어주는 공간이 되길 바라는 마음으로 만들었습니다.<br><br>한국에서도 글로벌 F&B 트렌드를, 글로벌에서도 한국 현지 F&B 트렌드를 자연스럽게 접할 수 있도록, 페이지 우측 상단에 한글/영어 자동번역 기능도 함께 준비했으니 많은 관심과 활용 부탁드립니다. 감사합니다🙇🏻`,
            globalNewsTitle: '글로벌 F&B 최신 뉴스 📰',
            koreanNewsTitle: '한국 F&B 최신 뉴스 📰',
            contactTitle: '제휴 문의',
            contactDesc: '광고, 콜라보, 원고 제안 등 편하게 남겨주세요 🤝',
            namePlaceholder: '이름 / 회사명',
            emailPlaceholder: '이메일',
            subjectPlaceholder: '문의 유형 (광고, 콜라보, 기타 등)',
            messagePlaceholder: '문의 내용을 입력해주세요',
            submitBtn: '문의 보내기',
            newsLoading: '뉴스를 불러오는 중...',
            newsEmpty: '뉴스를 준비 중입니다.',
            newsError: '뉴스를 불러올 수 없습니다.',
            articlesEmpty: '아티클을 준비 중입니다.',
            articlesError: '아티클을 불러올 수 없습니다.',
            seeMore: '더보기 →',
            articlesMoreBtn: '더보기 →',
        },
        en: {
            heroWelcome: `Welcome to FOOREND's Food Trend Archive ✨<br><br>This isn't just a news feed.<br>FOOREND began in 2022, when Alex — a former F&B buyer at a Korean department store — started clipping domestic and international F&B business news after leaving the industry, simply to stay sharp. That quiet habit grew into something bigger: a newsletter now shared with 3,500+ email subscribers, 4,900+ Instagram followers, and 1,000+ KakaoTalk Letter subscribers.<br><br>This archive is where that routine becomes visible. Which outlets. Which stories. What gets picked and why. Everything that goes into building over 200 issues of FOOREND is laid out here — and the sources update automatically every 3 hours, so what you're seeing is always current. It's built for the F&B professionals who need to move fast, the creators looking for their next angle, and anyone curious enough to want a real window into what's happening in this industry — not just locally, but globally.<br><br>Whether you're based in Korea and want to track global F&B trends, or you're somewhere in the world trying to understand what's happening in the Korean market, you'll find it here. Language buttons (KO/EN/JA) sit in the top right corner — use them freely. Hope this becomes a space you come back to 🙇🏻`,
            globalNewsTitle: 'Global F&B Latest News 📰',
            koreanNewsTitle: 'Korean F&B Latest News 📰',
            contactTitle: 'Partnership Inquiries',
            contactDesc: 'Advertising, collabs, content proposals — feel free to reach out 🤝',
            namePlaceholder: 'Name / Company',
            emailPlaceholder: 'Email',
            subjectPlaceholder: 'Inquiry Type (Advertising, Collaboration, Other)',
            messagePlaceholder: 'Write your message here',
            submitBtn: 'Send a Message',
            newsLoading: 'Loading news...',
            newsEmpty: 'No news available.',
            newsError: 'Failed to load news.',
            articlesEmpty: 'No articles available.',
            articlesError: 'Failed to load articles.',
            seeMore: 'More →',
            articlesMoreBtn: 'See More →',
        },
        ja: {
            heroWelcome: `FOOREND's Food Trend Archive へようこそ ✨<br><br>このページは、単なるニュースまとめではありません。<br>FOORENDは2022年、百貨店のF&Bチームバイヤーとして働いていたAlexが退職後も現場感覚を失わないよう、国内外のF&Bビジネスニュースのクリッピングを始めたことから生まれました。その記録が積み重なり、現在はメールニュースレター読者3,500+、Instagramフォロワー4,900+、KakaoTalkレター読者1,000+の方々とともにあるFOORENDとなりました。<br><br>このアーカイブページは、そのルーティンをそのまま公開した場所です。<br>毎週どのメディアから、どんなニュースを見て、その中から何をクリッピングするか。FOORENDが200件を超えるニュースレターを発行してきた情報探索のルーティンを詰め込んでいます。さらに、それらのメディアのニュースが3時間ごとに自動更新されるよう設定しています。<br><br>F&B業界のプロフェッショナルには素早くトレンドを把握するリファレンスとして、クリエイターにはコンテンツアイデアの出発点として、この業界に興味を持ち始めた方々には広く深い視野を開く場所となることを願って作りました。<br><br>韓国からもグローバルF&Bトレンドを、グローバルからも韓国のF&Bトレンドを自然に知ることができるよう、ページ右上に言語切り替えボタン（KO/EN/JA）を用意しています。ぜひご活用ください。ありがとうございます🙇🏻`,
            globalNewsTitle: 'グローバル F&B 最新ニュース 📰',
            koreanNewsTitle: '韓国 F&B 最新ニュース 📰',
            contactTitle: 'お問い合わせ',
            contactDesc: '広告、コラボ、原稿提案などお気軽にどうぞ 🤝',
            namePlaceholder: 'お名前 / 会社名',
            emailPlaceholder: 'メールアドレス',
            subjectPlaceholder: 'お問い合わせ種別（広告、コラボ、その他）',
            messagePlaceholder: 'お問い合わせ内容をご記入ください',
            submitBtn: '送信する',
            newsLoading: 'ニュースを読み込み中...',
            newsEmpty: 'ニュースを準備中です。',
            newsError: 'ニュースを読み込めませんでした。',
            articlesEmpty: '記事を準備中です。',
            articlesError: '記事を読み込めませんでした。',
            seeMore: 'もっと見る →',
            articlesMoreBtn: 'もっと見る →',
        }
    };

    const langBtns = document.querySelectorAll('.lang-btn');
    let currentLang = localStorage.getItem('lang') || 'ko';
    let fetchedData = null;

    function renderNewsGrid(container, sources, lang) {
        const t = translations[lang];
        const keys = Object.keys(sources);
        if (!keys.length) {
            container.innerHTML = `<p class="news-loading">${t.newsEmpty}</p>`;
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
                    <a href="${src.site}" class="feed-source-link" target="_blank" rel="noopener">${t.seeMore}</a>
                </div>
                <ul class="feed-items">
                    ${items.map(item => {
                        const title = lang === 'ko'
                            ? (item.title_ko || item.title)
                            : (item.title_en || item.title);
                        return `
                        <li class="feed-item">
                            <a href="${item.link}" class="feed-item-title" target="_blank" rel="noopener">${title}</a>
                            ${item.desc ? `<p class="feed-item-desc">${item.desc}</p>` : ''}
                        </li>`;
                    }).join('')}
                </ul>`;
            grid.appendChild(block);
        });
        if (!hasItems) {
            container.innerHTML = `<p class="news-loading">${t.newsEmpty}</p>`;
            return;
        }
        container.innerHTML = '';
        container.appendChild(grid);
    }

    function applyLang(lang) {
        const t = translations[lang];
        document.getElementById('hero-welcome').innerHTML = t.heroWelcome;
        document.getElementById('global-news-title').textContent = t.globalNewsTitle;
        document.getElementById('korean-news-title').textContent = t.koreanNewsTitle;
        document.getElementById('contact-title').textContent = t.contactTitle;
        document.getElementById('contact-desc').textContent = t.contactDesc;
        document.querySelector('input[name="name"]').placeholder = t.namePlaceholder;
        document.querySelector('input[name="email"]').placeholder = t.emailPlaceholder;
        document.querySelector('input[name="subject"]').placeholder = t.subjectPlaceholder;
        document.querySelector('textarea[name="message"]').placeholder = t.messagePlaceholder;
        document.getElementById('contact-submit').textContent = t.submitBtn;
        const enMore = document.getElementById('en-articles-more');
        const koMore = document.getElementById('ko-articles-more');
        if (enMore) enMore.textContent = t.articlesMoreBtn;
        if (koMore) koMore.textContent = t.articlesMoreBtn;
        langBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.lang === lang);
        });
        currentLang = lang;
        localStorage.setItem('lang', lang);

        // Re-render news grids if data is already loaded
        if (fetchedData) {
            const newsContainer = document.getElementById('news-feeds');
            const koreanNewsContainer = document.getElementById('korean-news-feeds');
            if (newsContainer) renderNewsGrid(newsContainer, fetchedData.sources || {}, lang);
            if (koreanNewsContainer) renderNewsGrid(koreanNewsContainer, fetchedData.korean_news || {}, lang);
        }
    }

    // ── Visitor counter ──────────────────────────────────────────
    const visitorLabel = document.getElementById('visitor-label');
    function updateVisitorLabel(lang) {
        if (lang === 'en') visitorLabel.textContent = ' visitors';
        else if (lang === 'ja') visitorLabel.textContent = '人が訪問';
        else visitorLabel.textContent = '명 방문';
    }

    function loadVisitorCount() {
        const APIs = [
            {
                url: 'https://api.counterapi.dev/v1/foorend-github-io/visits/up',
                parse: d => d.count,
            },
            {
                url: 'https://hits.dwyl.com/foorend/foorend.json',
                parse: d => d.count,
            },
        ];
        function tryNext(i) {
            if (i >= APIs.length) return; // keep placeholder "—"
            const { url, parse } = APIs[i];
            fetch(url)
                .then(r => { if (!r.ok) throw new Error(); return r.json(); })
                .then(data => {
                    const n = parse(data);
                    if (n != null && !isNaN(Number(n))) {
                        document.getElementById('visitor-count').textContent = Number(n).toLocaleString();
                    } else {
                        tryNext(i + 1);
                    }
                })
                .catch(() => tryNext(i + 1));
        }
        tryNext(0);
    }
    loadVisitorCount();

    applyLang(currentLang);

    langBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const lang = btn.dataset.lang;
            applyLang(lang);
            updateVisitorLabel(lang);
        });
    });

    updateVisitorLabel(currentLang);

    // ── News & articles fetch ────────────────────────────────────
    const newsContainer = document.getElementById('news-feeds');
    const koreanNewsContainer = document.getElementById('korean-news-feeds');
    const koreanArticlesList = document.getElementById('korean-articles-list');

    if (newsContainer || koreanNewsContainer || koreanArticlesList) {
        fetch('feeds.json')
            .then(r => r.json())
            .then(data => {
                fetchedData = data;
                if (newsContainer) {
                    renderNewsGrid(newsContainer, data.sources || {}, currentLang);
                }
                if (koreanNewsContainer) {
                    renderNewsGrid(koreanNewsContainer, data.korean_news || {}, currentLang);
                }
                if (koreanArticlesList) {
                    const articles = data.korean_articles || [];
                    if (!articles.length) {
                        koreanArticlesList.innerHTML = `<li class="articles-loading">${translations[currentLang].articlesEmpty}</li>`;
                        return;
                    }
                    koreanArticlesList.innerHTML = articles.map(a => `
                        <li><a href="${a.link}" target="_blank" rel="noopener">${a.title}</a></li>
                    `).join('');
                }
            })
            .catch(() => {
                const t = translations[currentLang];
                if (newsContainer) newsContainer.innerHTML = `<p class="news-loading">${t.newsError}</p>`;
                if (koreanNewsContainer) koreanNewsContainer.innerHTML = `<p class="news-loading">${t.newsError}</p>`;
                if (koreanArticlesList) koreanArticlesList.innerHTML = `<li class="articles-loading">${t.articlesError}</li>`;
            });
    }

    // ── Contact form ─────────────────────────────────────────────
    const contactForm = document.getElementById('contact-form');
    const contactConfirmation = document.getElementById('contact-confirmation');
    const contactSubmit = document.getElementById('contact-submit');

    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        contactSubmit.disabled = true;
        contactSubmit.textContent = currentLang === 'en' ? 'Sending...' : '전송 중...';

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
            contactSubmit.textContent = translations[currentLang].submitBtn;
            alert(currentLang === 'en' ? 'Submission failed. Please try again later.' : '전송에 실패했습니다. 잠시 후 다시 시도해주세요.');
        }
    });
});
