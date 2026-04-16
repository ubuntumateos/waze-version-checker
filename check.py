import requests
import re
from datetime import datetime

def format_date_jp(date_text):
    """英語の日付（April 17, 2026）を日本語（2026年4月17日）に変換"""
    months = {
        'January': '1', 'February': '2', 'March': '3', 'April': '4',
        'May': '5', 'June': '6', 'July': '7', 'August': '8',
        'September': '9', 'October': '10', 'November': '11', 'December': '12'
    }
    try:
        # カンマを除去して、空白で分割
        # 例: "April 17, 2026" -> ["April", "17", "2026"]
        parts = date_text.replace(',', '').strip().split()
        if len(parts) >= 3:
            m = months.get(parts[0], parts[0])
            d = parts[1]
            y = parts[2]
            return f"{y}年{m}月{d}日"
        return date_text
    except:
        return date_text

def get_ios_info():
    """iOS版はこれまで通り正確に取得"""
    url = "https://itunes.apple.com/lookup?bundleId=com.waze.iphone&country=jp"
    try:
        res = requests.get(url, timeout=10).json()
        data = res["results"][0]
        v = data["version"]
        dt = datetime.strptime(data["currentVersionReleaseDate"], "%Y-%m-%dT%H:%M:%SZ")
        return v, dt.strftime("%Y年%m月%d日")
    except:
        return "取得失敗", "取得失敗"

def get_android_date():
    """Google Playの内部コードから更新日だけを抜き出す"""
    # 米国設定（hl=en&gl=US）にすることで、日付形式を英語に固定して解析しやすくします
    url = "https://play.google.com/store/apps/details?id=com.waze&hl=en&gl=US"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=15)
        # Google Play内の「Updated on」というキーワードの直後にある日付を狙い撃ち
        match = re.search(r'\"Updated on\",\"([^\"]+)\"', res.text)
        if not match:
            # 別のパターンでも検索
            match = re.search(r'Updated on[^>]*>([^<]+)<', res.text)
            
        if match:
            return format_date_jp(match.group(1))
        return "日付の抽出に失敗しました"
    except:
        return "通信エラー"

# 実行
ios_v, ios_d = get_ios_info()
and_d = get_android_date()

# 結果表示
print(f"【iOS】 {ios_v} （{ios_d}）")
print(f"【Android】 バージョン不明 （{and_d}）")
