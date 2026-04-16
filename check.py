import requests
import re
from datetime import datetime

def format_date_jp(date_text):
    """英語の日付を日本語形式（YYYY年M月D日）に変換"""
    months = {
        'January': '1', 'February': '2', 'March': '3', 'April': '4',
        'May': '5', 'June': '6', 'July': '7', 'August': '8',
        'September': '9', 'October': '10', 'November': '11', 'December': '12'
    }
    try:
        # "April 17, 2026" などの形式を想定
        p = date_text.replace(',', '').strip().split()
        if len(p) >= 3:
            return f"{p[2]}年{months.get(p[0], p[0])}月{p[1]}日"
        return date_text
    except:
        return date_text

def get_ios():
    """iOS版は今まで通り正確に取得"""
    url = "https://itunes.apple.com/lookup?bundleId=com.waze.iphone&country=jp"
    try:
        r = requests.get(url, timeout=10).json()
        d = r["results"][0]
        dt = datetime.strptime(d["currentVersionReleaseDate"], "%Y-%m-%dT%H:%M:%SZ")
        return d["version"], dt.strftime("%Y年%m月%d日")
    except:
        return "---", "---"

def get_android_date_only():
    """Google Playから更新日のみを抽出"""
    # 英語(US)設定で取得するのが最も解析が安定します
    url = "https://play.google.com/store/apps/details?id=com.waze&hl=en&gl=US"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=15)
        html = res.text

        # Google Playの内部データ構造から "Updated on" の日付を検索
        # パターン1: 構造化データ
        d_match = re.search(r'\"Updated on\",\"([^\"]+)\"', html)
        if not d_match:
            # パターン2: HTML要素内
            d_match = re.search(r'Updated on[^>]*>([^<]+)<', html)
        
        date_raw = d_match.group(1) if d_match else "取得失敗"
        return format_date_jp(date_raw)
    except:
        return "接続失敗"

# データの実行
ios_v, ios_d = get_ios()
and_d = get_android_date_only()

# 出力（バージョンは不明として表示）
print(f"【iOS】 {ios_v} （{ios_d}）")
print(f"【Android】 バージョン不明 （{and_d}）")
