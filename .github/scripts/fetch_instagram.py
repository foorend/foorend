"""
Instagram Graph API를 통해 최신 게시물 3개를 가져와 instagram.json에 저장합니다.

필요한 GitHub Secrets:
  INSTAGRAM_ENG_TOKEN  - @foodtrendmag_foorend 계정의 Page Access Token
  INSTAGRAM_ENG_IG_ID  - @foodtrendmag_foorend Instagram Business Account ID
  INSTAGRAM_KOR_TOKEN  - @foodtrend_foorend 계정의 Page Access Token
  INSTAGRAM_KOR_IG_ID  - @foodtrend_foorend Instagram Business Account ID

토큰 발급 방법:
  1. Meta for Developers (developers.facebook.com) 에서 앱 생성
  2. 각 Instagram 계정을 Business/Creator 계정으로 전환 후 Facebook 페이지에 연결
  3. Graph API Explorer에서 Page Access Token 발급 (만료: 60일, 이후 갱신 필요)
  4. IG User ID: GET https://graph.facebook.com/v21.0/me/accounts 로 확인
"""
import urllib.request, json, os
from datetime import datetime, timezone


def fetch_ig_posts(ig_user_id, access_token, limit=3):
    fields = 'id,media_type,media_url,thumbnail_url,permalink,timestamp'
    url = (
        f'https://graph.facebook.com/v21.0/{ig_user_id}/media'
        f'?fields={fields}&limit={limit}&access_token={access_token}'
    )
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    posts = []
    for item in data.get('data', []):
        # 동영상은 thumbnail_url 사용, 이미지는 media_url 사용
        media_url = item.get('thumbnail_url') or item.get('media_url', '')
        if not media_url:
            continue
        posts.append({
            'id': item['id'],
            'media_url': media_url,
            'permalink': item.get('permalink', ''),
            'timestamp': item.get('timestamp', ''),
        })
    return posts


result = {
    'lastUpdated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'eng': {
        'username': 'foodtrendmag_foorend',
        'profile_url': 'https://www.instagram.com/foodtrendmag_foorend',
        'posts': []
    },
    'kor': {
        'username': 'foodtrend_foorend',
        'profile_url': 'https://www.instagram.com/foodtrend_foorend',
        'posts': []
    }
}

for key, env_id, env_token in [
    ('eng', 'INSTAGRAM_ENG_IG_ID', 'INSTAGRAM_ENG_TOKEN'),
    ('kor', 'INSTAGRAM_KOR_IG_ID', 'INSTAGRAM_KOR_TOKEN'),
]:
    ig_id = os.environ.get(env_id, '')
    token = os.environ.get(env_token, '')
    if ig_id and token:
        try:
            result[key]['posts'] = fetch_ig_posts(ig_id, token)
            print(f"✓ {key.upper()} Instagram: {len(result[key]['posts'])} posts")
        except Exception as e:
            print(f"✗ {key.upper()} Instagram: {e}")
    else:
        print(f"  {key.upper()} Instagram: skipped (secrets not set)")

with open('instagram.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print('Saved instagram.json')
