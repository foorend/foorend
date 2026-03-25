import urllib.request, urllib.parse, re, html, json, xml.etree.ElementTree as ET
from datetime import datetime, timezone

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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

        # Google News: strip source name from title (e.g., " - Restaurant Business")
        if mode == 'googlenews':
            title = re.sub(r'\s*-\s*[^-]+$', '', title).strip()
            desc = ''  # Google News descriptions are just HTML links, not useful

        if title:
            items.append({'title': title, 'link': link, 'desc': desc})

    # Atom
    if not items:
        ns = 'http://www.w3.org/2005/Atom'
        for entry in root.findall(f'.//{{{ns}}}entry'):
            t = entry.find(f'{{{ns}}}title')
            l = entry.find(f'{{{ns}}}link')
            s = entry.find(f'{{{ns}}}summary') or entry.find(f'{{{ns}}}content')

            title = strip_html(t.text) if t is not None else ''
            link = l.get('href', '') if l is not None else ''
            desc = strip_html(s.text)[:150] if s is not None else ''

            if title:
                items.append({'title': title, 'link': link, 'desc': desc})

    return items[:3]

result = {
    'lastUpdated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'sources': {}
}

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

with open('feeds.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print('Saved feeds.json')
