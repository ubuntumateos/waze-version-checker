import requests
import re
from datetime import datetime

def format_date_jp(date_text):
    """英語の日付を日本語形式に変換（例: April 16, 2026 -> 2026年4月16日）"""
    months = {
        'January': '1', 'February': '2', 'March': '3', 'April': '4',
        'May': '5', 'June': '6', 'July': '7', 'August': '8',
        'September': '9', 'October': '10', 'November': '11', 'December': '12'
    }
    try:
        # カンマを除去して分割
        p = date_text.replace(',', '').strip().split()
        if len(p) >= 3:
            y = p[2]
            m = months.get(p[0], p[0])
            d = p[1]
            return f"{y}年{m}月{d}日"
        return date_text
    except:
        return date_text

def get_ios():
    """iOS版データの取得（Apple公式API）"""
    url = "https://itunes.apple.com/lookup?bundleId=com.waze.iphone&country=jp"
    try:
        r = requests.get(url, timeout=10).json()
        d = r["results"][0]
        dt = datetime.strptime(d["currentVersionReleaseDate"], "%Y-%m-%dT%H:%M:%SZ")
        return d["version"], dt.strftime("%Y年%m月%d日")
    except:
        return "---", "---"

def get_and_official():
    """Android版データの取得（Waze公式ヘルプページを徹底スキャン）"""
    url = "https://support.google.com/waze/answer/6271171"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9" # 英語ページを優先して取得（解析しやすいため）
    }
    try:
        res = requests.get(url, headers=headers, timeout=15)
        html = res.text

        # 1. バージョンの抽出 (Android: X.X.X.X の形式を探す)
        v_match = re.search(r'Android:\s*([\d\.]+)', html)
        if not v_match:
            # 別のパターン (Waze version X.X.X.X for Android)
            v_match = re.search(r'version\s*([\d\.]+)\s*for Android', html, re.IGNORECASE)
        version = v_match.group(1) if v_match else "取得失敗"

        # 2. 日付の抽出 (英語形式の月名が含まれる日付を探す)
        # 例: April 16, 2026
        d_match = re.search(r'([A-Z][a-z]+ \d{1,2}, \d{4})', html)
        date_raw = d_match.group(1) if d_match else "取得失敗"
        
        return version, format_date_jp(date_raw)
    except:
        return "接続失敗", "接続失敗"

# データの実行
ios_v, ios_d = get_ios()
and_v, and_d = get_and_official()

# 出力
print(f"【iOS】 {ios_v} （{ios_d}）")
print(f"【Android】 {and_v} （{and_d}）")
