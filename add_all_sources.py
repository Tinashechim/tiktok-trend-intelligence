import re

with open('deploy_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace fetch_tiktok_trends with enhanced version
old_scraper = '''def fetch_tiktok_trends():
    \"\"\"Fetch trending hashtags and sounds from TikTok public endpoints.\"\"\"
    trends = []'''

new_scraper = '''def fetch_tiktok_trends():
    \"\"\"Fetch trends from all possible sources.\"\"\"
    trends = []
    sources = {}

    def add_trend(name, type_, video_count, growth_rate, source, score=None):
        if not name or len(name) < 2:
            return
        name_lower = name.lower()
        if name_lower in BAD_WORDS:
            return
        if name_lower not in sources:
            if score is None:
                score = min(100, int(growth_rate / 5) + random.randint(0, 20))
            sources[name_lower] = source
            trends.append({
                'name': name,
                'type': type_,
                'video_count': video_count,
                'growth_rate': growth_rate,
                'score': score,
                'source': source
            })
        else:
            # Keep highest growth and score if duplicate
            existing = next((t for t in trends if t['name'].lower() == name_lower), None)
            if existing:
                if growth_rate > existing.get('growth_rate', 0):
                    existing['growth_rate'] = growth_rate
                if video_count > existing.get('video_count', 0):
                    existing['video_count'] = video_count
                if score and score > existing.get('score', 0):
                    existing['score'] = score
                # If multiple sources, mark as multi
                if sources[name_lower] != source:
                    existing['source'] = sources[name_lower] + '+' + source'''

content = content.replace(old_scraper, new_scraper)

# Insert source collection into the scraper (after headers setup)
# We'll append source attempts after the existing headers block.
old_headers = """headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
    }"""

new_headers = old_headers + """

    # 1) TikTok Creative Center (official free)
    try:
        cc_url = 'https://ads.tiktok.com/creative_radar_api/v1/popular_trend/hashtag/list'
        cc_params = {'period': '7', 'page': '1', 'limit': '20', 'country_code': 'US'}
        cc_resp = requests.get(cc_url, headers=headers, params=cc_params, timeout=6)
        if cc_resp.status_code == 200:
            cc_data = cc_resp.json()
            for item in cc_data.get('data', {}).get('list', []):
                hname = item.get('hashtag_name')
                if hname:
                    post_count = item.get('post_count', 0)
                    growth = item.get('growth_rate', 0) or random.randint(20, 200)
                    add_trend(f'#{hname}', 'hashtag', post_count, growth, 'creative_center')
    except Exception as e:
        pass

    # 2) TikTok Creative Center songs
    try:
        cc_song_url = 'https://ads.tiktok.com/creative_radar_api/v1/popular_trend/song/list'
        cc_song_params = {'period': '7', 'page': '1', 'limit': '20', 'country_code': 'US'}
        cc_song_resp = requests.get(cc_song_url, headers=headers, params=cc_song_params, timeout=6)
        if cc_song_resp.status_code == 200:
            cc_song_data = cc_song_resp.json()
            for item in cc_song_data.get('data', {}).get('list', []):
                sname = item.get('song_name') or item.get('title')
                if sname:
                    vc = item.get('video_count', 0)
                    growth = item.get('growth_rate', 0) or random.randint(20, 200)
                    add_trend(sname, 'sound', vc, growth, 'creative_center')
    except Exception as e:
        pass
"""

# Insert the creative center source block after headers and before public endpoints
content = content.replace(old_headers, new_headers)

# Now insert public endpoints and discover scraping attempts before the fallback database
# We'll find the existing endpoints loop and add our add_trend calls there.
# For simplicity, we replace the whole public endpoint/discover section with enhanced version.
old_public = """    # Attempt 1: TikTok public recommend endpoints
    endpoints = [
        ('https://www.tiktok.com/api/recommend/hashtag/', {'aid': '1988', 'count': '20'}),
        ('https://www.tiktok.com/api/recommend/sound/', {'aid': '1988', 'count': '20'}),
    ]
    for url, params in endpoints:
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if 'challengeList' in data:
                    for item in data['challengeList']:
                        challenge = item.get('challenge', {})
                        title = challenge.get('title', '')
                        if title and len(title) > 1 and title.lower() not in BAD_WORDS:
                            video_count = challenge.get('stats', {}).get('videoCount', 0)
                            trends.append({
                                'name': f'#{title}',
                                'type': 'hashtag',
                                'video_count': video_count,
                                'growth_rate': random.randint(50, 400),
                                'score': random.randint(50, 85)
                            })
                if 'musicList' in data:
                    for item in data['musicList']:
                        music = item.get('music', {})
                        title = music.get('title', '')
                        if title:
                            video_count = music.get('stats', {}).get('videoCount', 0)
                            trends.append({
                                'name': title,
                                'type': 'sound',
                                'video_count': video_count,
                                'growth_rate': random.randint(30, 250),
                                'score': random.randint(50, 85)
                            })
        except:
            pass"""

new_public = """    # 3) TikTok public recommend endpoints
    endpoints = [
        ('https://www.tiktok.com/api/recommend/hashtag/', {'aid': '1988', 'count': '20'}),
        ('https://www.tiktok.com/api/recommend/sound/', {'aid': '1988', 'count': '20'}),
    ]
    for url, params in endpoints:
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if 'challengeList' in data:
                    for item in data['challengeList']:
                        challenge = item.get('challenge', {})
                        title = challenge.get('title', '')
                        if title and len(title) > 1 and title.lower() not in BAD_WORDS:
                            video_count = challenge.get('stats', {}).get('videoCount', 0)
                            add_trend(f'#{title}', 'hashtag', video_count, random.randint(50, 400), 'public_api')
                if 'musicList' in data:
                    for item in data['musicList']:
                        music = item.get('music', {})
                        title = music.get('title', '')
                        if title:
                            video_count = music.get('stats', {}).get('videoCount', 0)
                            add_trend(title, 'sound', video_count, random.randint(30, 250), 'public_api')
        except:
            pass"""

content = content.replace(old_public, new_public)

# Replace the discover page scraping section to use add_trend and source label
old_discover = """    # Attempt 2: Discover page scrape
    try:
        resp = requests.get('https://www.tiktok.com/discover', headers=headers, timeout=5)
        if resp.status_code == 200:
            hashtags = re.findall(r'#(\w+)', resp.text)
            counts = Counter(hashtags)
            for tag, count in counts.most_common(20):
                tag_lower = tag.lower()
                if len(tag) < 3 or tag_lower in BAD_WORDS:
                    continue
                if re.match(r'^[0-9a-f]{6}$', tag_lower):
                    continue
                trends.append({
                    'name': f'#{tag}',
                    'type': 'hashtag',
                    'video_count': count * random.randint(500, 5000),
                    'growth_rate': random.randint(50, 250),
                    'score': random.randint(50, 80)
                })
    except:
        pass"""

new_discover = """    # 4) Discover page scrape
    try:
        resp = requests.get('https://www.tiktok.com/discover', headers=headers, timeout=5)
        if resp.status_code == 200:
            hashtags = re.findall(r'#(\w+)', resp.text)
            counts = Counter(hashtags)
            for tag, count in counts.most_common(20):
                tag_lower = tag.lower()
                if len(tag) < 3 or tag_lower in BAD_WORDS:
                    continue
                if re.match(r'^[0-9a-f]{6}$', tag_lower):
                    continue
                add_trend(f'#{tag}', 'hashtag', count * random.randint(500, 5000), random.randint(50, 250), 'discover')
    except:
        pass"""

content = content.replace(old_discover, new_discover)

# Add third-party public endpoint (Tokboard example)
old_fallback = """    # Attempt 3: Fallback realistic trend database"""
new_thirdparty = """    # 5) Third-party public TikTok trend API (free)
    try:
        tp_url = 'https://tokboard.com/api/trending'
        tp_resp = requests.get(tp_url, headers=headers, timeout=5)
        if tp_resp.status_code == 200:
            tp_data = tp_resp.json()
            for item in tp_data[:20]:
                name = item.get('name') or item.get('title') or item.get('hashtag')
                if name:
                    add_trend(name, item.get('type', 'hashtag'), item.get('videos', 0), item.get('growth', 0), 'tokboard')
    except:
        pass

    # 6) Fallback realistic trend database"""
content = content.replace(old_fallback, new_thirdparty)

# Replace fallback section to use add_trend
old_fallback_content = """    # Attempt 3: Fallback realistic trend database
    if len(trends) < 5:
        realistic = [
            {"name": "AI Filter Trend", "type": "format", "video_count": 120000, "growth_rate": 340},
            {"name": "Transformation Challenge", "type": "topic", "video_count": 89000, "growth_rate": 280},
            {"name": "Silent Review", "type": "format", "video_count": 280000, "growth_rate": 220},
            {"name": "#MoneyTok", "type": "hashtag", "video_count": 340000, "growth_rate": 210},
            {"name": "#CozyGaming", "type": "hashtag", "video_count": 450000, "growth_rate": 180},
            {"name": "#StudyTok", "type": "hashtag", "video_count": 410000, "growth_rate": 150},
        ]
        for item in realistic:
            trends.append({
                'name': item['name'],
                'type': item['type'],
                'video_count': item['video_count'],
                'growth_rate': item['growth_rate'],
                'score': min(100, int(item['growth_rate'] / 5))
            })"""

new_fallback_content = """    # 6) Fallback realistic trend database
    if len(trends) < 5:
        realistic = [
            {"name": "AI Filter Trend", "type": "format", "video_count": 120000, "growth_rate": 340},
            {"name": "Transformation Challenge", "type": "topic", "video_count": 89000, "growth_rate": 280},
            {"name": "Silent Review", "type": "format", "video_count": 280000, "growth_rate": 220},
            {"name": "#MoneyTok", "type": "hashtag", "video_count": 340000, "growth_rate": 210},
            {"name": "#CozyGaming", "type": "hashtag", "video_count": 450000, "growth_rate": 180},
            {"name": "#StudyTok", "type": "hashtag", "video_count": 410000, "growth_rate": 150},
        ]
        for item in realistic:
            add_trend(item['name'], item['type'], item['video_count'], item['growth_rate'], 'fallback')"""

content = content.replace(old_fallback_content, new_fallback_content)

# Add source field to trends returned by current/all endpoints
content = content.replace('"trend_score": t.trend_score,\n            "growth_rate": t.growth_rate,', '"trend_score": t.trend_score,\n            "source": getattr(t, "source", "unknown"),\n            "growth_rate": t.growth_rate,')

# Add source column to Trend model
old_trend_model = "data = Column(JSON, default=dict)"
new_trend_model = "data = Column(JSON, default=dict)\n    source = Column(String(50), default='fallback')"
content = content.replace(old_trend_model, new_trend_model)

# Store source when auto_update_database saves trends
old_store_trend = "trend_score=t.get('score', 70),"
new_store_trend = "trend_score=t.get('score', 70),\n                source=t.get('source', 'fallback'),"
content = content.replace(old_store_trend, new_store_trend)

with open('deploy_server.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Multi-source scraper added")
