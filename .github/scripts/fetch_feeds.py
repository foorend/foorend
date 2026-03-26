import urllib.request, urllib.parse, re, html, json, xml.etree.ElementTree as ET
from datetime import datetime, timezone

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

SOURCES = [
    {
        'key': 'eater',
        'label': 'Eater',
        'site': 'https://www.eater.com/trends',
        'rss': 'https://www.eater.com/rss/index.xml',
        'mode': 'direct',
    },
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

def fetch_stibee_articles(base_url, count=6):
    """Fetch recent newsletter issues from stibee public archive page."""
    articles = []

    # Try RSS/Atom feed variants first
    for rss_path in ['/rss', '/feed', '/atom']:
        try:
            rss_url = base_url.rstrip('/') + rss_path
            content = fetch(rss_url)
            items = parse_rss(content, 'direct')
            if items:
                print(f"  stibee RSS found at {rss_path}: {len(items)} articles")
                return items[:count]
        except Exception:
            pass

    # Fall back to HTML scraping of the archive page
    try:
        content_bytes = fetch(base_url)
        content = content_bytes.decode('utf-8', errors='ignore')

        # Try Next.js __NEXT_DATA__ embedded JSON (most reliable for SSR pages)
        nd_match = re.search(r'<script[^>]+id="__NEXT_DATA__"[^>]*>(\{.+?\})</script>', content, re.DOTALL)
        if nd_match:
            try:
                nd = json.loads(nd_match.group(1))
                props = nd.get('props', {}).get('pageProps', {})
                # Try common stibee data shapes
                for field in ('emailList', 'emails', 'issues', 'archiveList', 'list'):
                    items_data = props.get(field, [])
                    if isinstance(items_data, list) and items_data:
                        for item in items_data[:count]:
                            title = item.get('subject', item.get('title', item.get('name', '')))
                            link = item.get('archiveUrl', item.get('url', item.get('link', '')))
                            if title and link:
                                articles.append({'title': title, 'link': link, 'desc': ''})
                        if articles:
                            print(f"  stibee __NEXT_DATA__[{field}]: {len(articles)} articles")
                            return articles[:count]
            except (json.JSONDecodeError, KeyError):
                pass

        # Regex fallback: look for stibee API archive links with adjacent text
        link_pat = re.compile(
            r'href="((?:https://(?:stibee\.com|foodtrend\.stibee\.com))?/api/v1\.0/emails/auto/[^"]+)"[^>]*>'
            r'((?:[^<]|<(?!/))+)'
        )
        for m in link_pat.finditer(content):
            link = m.group(1)
            if not link.startswith('http'):
                link = 'https://stibee.com' + link
            text_block = strip_html(m.group(2)).strip()
            if text_block and len(text_block) > 4:
                articles.append({'title': text_block[:120], 'link': link, 'desc': ''})
                if len(articles) >= count:
                    break

        if articles:
            print(f"  stibee HTML scrape: {len(articles)} articles")
            return articles

        # Last resort: Google News search for stibee foodtrend newsletter
        q = urllib.parse.quote('site:stibee.com foodtrend')
        gn_url = f'https://news.google.com/rss/search?q={q}&hl=ko&gl=KR&ceid=KR:ko'
        gn_content = fetch(gn_url)
        items = parse_rss(gn_content, 'googlenews')
        if items:
            print(f"  stibee via Google News: {len(items)} articles")
            return items[:count]

    except Exception as e:
        print(f"  stibee HTML fetch error: {e}")

    print("  stibee: no articles found")
    return []

result = {
    'lastUpdated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'sources': {},
    'korean_news': {},
    'korean_articles': [],
}

# Global sources
for src in SOURCES:
    try:
        content = fetch(src['rss'])
        items = parse_rss(content, src['mode'])
        result['sources'][src['key']] = {
            'label': src['label'],
            'site': src['site'],
            'items': items,
        }
        print(f"✓ {src['label']}: {len(items)} articles")
    except Exception as e:
        print(f"✗ {src['label']}: {e}")
        result['sources'][src['key']] = {
            'label': src['label'],
            'site': src['site'],
            'items': [],
        }

# Korean news sources
for src in KOREAN_SOURCES:
    try:
        content = fetch(src['rss'])
        items = parse_rss(content, src['mode'])
        result['korean_news'][src['key']] = {
            'label': src['label'],
            'site': src['site'],
            'items': items,
        }
        print(f"✓ {src['label']}: {len(items)} articles")
    except Exception as e:
        print(f"✗ {src['label']}: {e}")
        result['korean_news'][src['key']] = {
            'label': src['label'],
            'site': src['site'],
            'items': [],
        }

# Korean newsletter articles (stibee)
print("Fetching stibee Korean newsletter articles...")
result['korean_articles'] = fetch_stibee_articles('https://foodtrend.stibee.com')

with open('feeds.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print('Saved feeds.json')
