import urllib.request, urllib.parse, re, html, json, xml.etree.ElementTree as ET, time
from datetime import datetime, timezone


def translate(text, from_lang, to_lang):
    """Translate text using MyMemory free API. Returns original on failure."""
    if not text:
        return text
    try:
        url = (
            'https://api.mymemory.translated.net/get?q='
            + urllib.parse.quote(text[:500])
            + f'&langpair={from_lang}|{to_lang}'
        )
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        result = data['responseData']['translatedText']
        if 'MYMEMORY' in result or 'QUERY LENGTH' in result:
            return text
        return result
    except Exception:
        return text

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

SOURCES = [
    {
        'key': 'restaurantbusiness',
        'label': 'Restaurant Business',
        'site': 'https://www.restaurantbusinessonline.com/',
        'rss': 'https://news.google.com/rss/search?q=site:restaurantbusinessonline.com&hl=en-US&gl=US&ceid=US:en',
        'mode': 'googlenews',
    },
    {
        'key': 'foodandwine',
        'label': 'Food & Wine',
        'site': 'https://www.foodandwine.com/news',
        'rss': 'https://news.google.com/rss/search?q=site:foodandwine.com/news&hl=en-US&gl=US&ceid=US:en',
        'mode': 'googlenews',
    },
    {
        'key': 'businessinsider',
        'label': 'Business Insider',
        'site': 'https://www.businessinsider.com/food',
        'rss': 'https://news.google.com/rss/search?q=site:businessinsider.com/food&hl=en-US&gl=US&ceid=US:en',
        'mode': 'googlenews',
    },
    {
        'key': 'eater',
        'label': 'Eater',
        'site': 'https://www.eater.com/trends',
        'rss': 'https://www.eater.com/rss/index.xml',
        'mode': 'direct',
    },
]

def _gnews_ko(site, keyword):
    q = urllib.parse.quote(f'site:{site} ({keyword})')
    return f'https://news.google.com/rss/search?q={q}&hl=ko&gl=KR&ceid=KR:ko'

KOREAN_SOURCES = [
    {
        'key': 'hankyung',
        'label': '한국경제',
        'site': 'https://www.hankyung.com/topic/food',
        'rss': _gnews_ko('hankyung.com', '푸드 OR 음식'),
        'mode': 'googlenews',
    },
    {
        'key': 'sedaily',
        'label': '서울경제',
        'site': 'https://www.sedaily.com',
        'rss': _gnews_ko('sedaily.com', '푸드 OR 음식'),
        'mode': 'googlenews',
    },
    {
        'key': 'maeil',
        'label': '매일경제',
        'site': 'https://www.mk.co.kr',
        'rss': _gnews_ko('mk.co.kr', '푸드 OR 음식'),
        'mode': 'googlenews',
    },
    {
        'key': 'realfoods',
        'label': '리얼푸드',
        'site': 'https://www.realfoods.co.kr',
        'rss': _gnews_ko('realfoods.co.kr', '푸드 OR 음식'),
        'mode': 'googlenews',
    },
]

def strip_html(text):
    return re.sub(r'<[^>]+>', '', html.unescape(text or '')).strip()

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read()

def parse_rss(content, mode):
    try:
        root = ET.fromstring(content)
    except ET.ParseError:
        return []

    items = []

    # RSS 2.0
    for item in root.findall('.//item'):
        t = item.find('title')
        l = item.find('link')
        d = item.find('description')

        title = strip_html(t.text) if t is not None else ''
        link = (l.text or '').strip() if l is not None else ''
        desc = strip_html(d.text)[:150] if d is not None else ''

        if mode == 'googlenews':
            title = re.sub(r'\s*-\s*[^-]+$', '', title).strip()
            desc = ''

        if title:
            items.append({'title': title, 'link': link, 'desc': desc})

    # Atom
    if not items:
        ns = 'http://www.w3.org/2005/Atom'
        for entry in root.findall(f'.//{{{ns}}}entry'):
            t = entry.find(f'{{{ns}}}title')
            l = entry.find(f'{{{ns}}}link')
            s_elem = entry.find(f'{{{ns}}}summary')
            s = s_elem if s_elem is not None else entry.find(f'{{{ns}}}content')

            title = strip_html(t.text) if t is not None else ''
            link = l.get('href', '') if l is not None else ''
            desc = strip_html(s.text)[:150] if s is not None else ''

            if title:
                items.append({'title': title, 'link': link, 'desc': desc})

    return items[:3]

def fetch_stibee_articles(base_url='https://foodtrend.stibee.com', count=6):
    """Fetch latest Korean newsletter articles via sitemap + og:title from each article page."""
    try:
        # Step 1: Parse sitemap to get article URLs sorted by number (newest first)
        sitemap = fetch(base_url.rstrip('/') + '/sitemap.xml')
        root = ET.fromstring(sitemap)
        ns_sm = 'http://www.sitemaps.org/schemas/sitemap/0.9'

        urls = []
        for url_elem in root.findall(f'{{{ns_sm}}}url'):
            loc = url_elem.find(f'{{{ns_sm}}}loc')
            if loc is None or not loc.text:
                continue
            m = re.search(r'/p/(\d+)', loc.text)
            if m:
                urls.append((int(m.group(1)), loc.text.rstrip('/')))

        urls.sort(key=lambda x: x[0], reverse=True)
        top_urls = [url for _, url in urls[:count]]
        print(f"  stibee sitemap: found {len(urls)} articles, fetching top {len(top_urls)}")

        # Step 2: Fetch og:title from the head of each article page (first 8KB)
        articles = []
        for url in top_urls:
            try:
                req = urllib.request.Request(url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=10) as r:
                    head_html = r.read(8192).decode('utf-8', errors='ignore')

                title_m = (
                    re.search(r'property="og:title"\s+content="([^"]+)"', head_html) or
                    re.search(r'<title>([^<]+)</title>', head_html)
                )
                title = html.unescape(title_m.group(1)) if title_m else url
                articles.append({'title': title, 'link': url, 'desc': ''})
                print(f"  ✓ {title[:60]}")
            except Exception as e:
                print(f"  stibee {url}: {e}")

        return articles

    except Exception as e:
        print(f"✗ stibee: {e}")
        return []

result = {
    'lastUpdated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'sources': {},
    'korean_news': {},
    'korean_articles': [],
}

# Global sources — add Korean translations for titles
for src in SOURCES:
    try:
        content = fetch(src['rss'])
        items = parse_rss(content, src['mode'])
        for item in items:
            item['title_ko'] = translate(item['title'], 'en', 'ko')
            time.sleep(0.3)
            item['title_ja'] = translate(item['title'], 'en', 'ja')
            time.sleep(0.3)
            item['title_zh'] = translate(item['title'], 'en', 'zh')
            time.sleep(0.3)
        result['sources'][src['key']] = {
            'label': src['label'],
            'site': src['site'],
            'items': items,
        }
        print(f"✓ {src['label']}: {len(items)} articles (translated to ko, ja, zh)")
    except Exception as e:
        print(f"✗ {src['label']}: {e}")
        result['sources'][src['key']] = {
            'label': src['label'],
            'site': src['site'],
            'items': [],
        }

# Korean news sources — add English translations for titles
for src in KOREAN_SOURCES:
    try:
        content = fetch(src['rss'])
        items = parse_rss(content, src['mode'])
        for item in items:
            item['title_en'] = translate(item['title'], 'ko', 'en')
            time.sleep(0.3)
            item['title_ja'] = translate(item['title'], 'ko', 'ja')
            time.sleep(0.3)
            item['title_zh'] = translate(item['title'], 'ko', 'zh')
            time.sleep(0.3)
        result['korean_news'][src['key']] = {
            'label': src['label'],
            'site': src['site'],
            'items': items,
        }
        print(f"✓ {src['label']}: {len(items)} articles (translated to en, ja, zh)")
    except Exception as e:
        print(f"✗ {src['label']}: {e}")
        result['korean_news'][src['key']] = {
            'label': src['label'],
            'site': src['site'],
            'items': [],
        }

# Korean newsletter articles (stibee)
print("Fetching stibee Korean newsletter articles...")
result['korean_articles'] = fetch_stibee_articles()

with open('feeds.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print('Saved feeds.json')
