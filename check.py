import requests
import re
from datetime import datetime

def format_date_jp(date_text):
    """RSSの日付形式（例: Wed, 15 Apr 2026）を日本語に変換"""
    months = {
        'Jan': '1', 'Feb': '2', 'Mar': '3', 'Apr': '4', 'May': '5', 'Jun': '6',
        'Jul': '7', 'Aug': '8', 'Sep': '9', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }
    try:
        # RSSの標準的な日付は "15 Apr 2026" のような部分を含む
        match = re.search(r'(\d{1,2})\s([A-Z][a-z]{2})\s(\d{4})', date_text)
        if match:
            d, m_str, y = match.groups()
            return f"{y}年{months.get(m_str, m_str)}月{d}日"
        return date_text
    except:
        return date_text

def get_ios():
    """iOSはApple公式APIが最強なのでそのまま維持"""
    url = "https://itunes.apple.com/lookup?bundleId=com.waze.iphone&country=jp"
    try:
        r = requests.get(url, timeout=10).json()
        d = r["results"][0]
        dt = datetime.strptime(d["currentVersionReleaseDate"], "%Y-%m-%dT%H:%M:%SZ")
        return d["version"], dt.strftime("%Y年%m月%d日")
    except:
        return "---", "---"

def get_waze_rss_info():
    """Waze公式の更新フィードからAndroid情報を取得"""
    # Wazeのリリース情報が集まる公式フィード（一例）
    url = "https://www.waze.com/forum/feed.php?f=162" # Release Notes Forum
    try:
        res = requests.get(url, timeout=15)
        content = res.text
        
        # 1. Androidのバージョンを探す
        # フィード内のタイトルから "Android v4.XXX" のような形式を抽出
        v_match = re.search(r'Android\s+v?([\d\.]+)', content)
        version = v_match.group(1) if v_match else "不明"
        
        # 2. 更新日を探す（RSSの <pubDate> タグ）
        d_match = re.search(r'<pubDate>(.*?)</pubDate>', content)
        date_raw = d_match.group(1) if d_match else "不明"
        
        return version, format_date_jp(date_raw)
    except:
        return "不明", "接続失敗"

# 実行
ios_v, ios_d = get_ios()
and_v, and_d = get_waze_rss_info()

# 結果表示
print(f"【iOS】 {ios_v} （{ios_d}）")
print(f"【Android】 {and_v} （{and_d}）")
