import requests
import re
from datetime import datetime

def format_date_jp(date_text):
    """英語の日付を日本語形式に変換"""
    months = {
        'January': '1', 'February': '2', 'March': '3', 'April': '4',
        'May': '5', 'June': '6', 'July': '7', 'August': '8',
        'September': '9', 'October': '10', 'November': '11', 'December': '12'
    }
    try:
        # "April 16, 2026" などの形式を想定
        p = date_text.replace(',', '').strip().split()
        if len(p) >= 3:
            return f"{p[2]}年{months.get(p[0], p[0])}月{p[1]}日"
        return date_text
    except:
        return date_text

def get_ios():
    url = "https://itunes.apple.com/lookup?bundleId=com.waze.iphone&country=jp"
    try:
        r = requests.get(url, timeout=10).json()
        d = r["results"][0]
        dt = datetime.strptime(d["currentVersionReleaseDate"], "%Y-%m-%dT%H:%M:%SZ")
        return d["version"], dt.strftime("%Y年%m月%d日")
    except:
        return "取得失敗", "取得失敗"

def get_android_google_play():
    """Google Playの内部データから抽出"""
    url = "https://play.google.com/store/apps/details?id=com.waze&hl=en&gl=US" # 解析しやすいよう英語・米国設定で取得
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=15)
        html = res.text

        # 1. バージョンの抽出 (JSON形式内のパターン)
        v_match = re.search(r'\[\[\["([\d\.]+)"\]\]\]', html)
        version = v_match.group(1) if v_match else "構造変化"

        # 2. 更新日の抽出 (Google Playの新しいデータ形式に対応)
        # "Updated on" の後にある日付を探す
        d_match = re.search(r'\"Updated on\",\"([^\"]+)\"', html)
        if not d_match:
            # 予備のパターン
            d_match = re.search(r'Updated on[^>]*>([^<]+)<', html)
            
        date_raw = d_match.group(1) if d_match else "不明"
        
        return version, format_date_jp(date_raw)
    except:
        return "接続失敗", "接続失敗"

# 実行
ios_v, ios_d = get_ios()
and_v, and_d = get_android_google_play()

print(f"【iOS】 {ios_v} （{ios_d}）")
print(f"【Android】 {and_v} （{and_d}）")
