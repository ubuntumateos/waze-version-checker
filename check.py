import requests
import re
from datetime import datetime

def format_date_jp(date_text):
    """'2026-04-15 16:08:53' のような形式を '2026年4月15日' に変換"""
    try:
        dt = datetime.strptime(date_text.split()[0], "%Y-%m-%d")
        return f"{dt.year}年{dt.month}月{dt.day}日"
    except:
        return date_text

def get_ios():
    """iOSはApple公式APIから安定取得"""
    url = "https://itunes.apple.com/lookup?bundleId=com.waze.iphone&country=jp"
    try:
        r = requests.get(url, timeout=10).json()
        d = r["results"][0]
        dt = datetime.strptime(d["currentVersionReleaseDate"], "%Y-%m-%dT%H:%M:%SZ")
        return d["version"], dt.strftime("%Y年%m月%d日")
    except:
        return "---", "---"

def get_android_info():
    """Aptoideの解析ページからAndroidの最新バージョンと日時を取得"""
    url = "https://waze-gps-maps-traffic-alerts-sat-nav.en.aptoide.com/app"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=15)
        html = res.text

        # 1. APK Version: 5.18.0.0 のような箇所を探す
        v_match = re.search(r'APK Version:\s*([\d\.]+)', html)
        version = v_match.group(1) if v_match else "取得失敗"

        # 2. Release Date: 2026-04-15 16:08:53 のような箇所を探す
        d_match = re.search(r'Release Date:\s*([\d\-]+\s[\d\:]+)', html)
        date_raw = d_match.group(1) if d_match else "取得失敗"
        
        return version, format_date_jp(date_raw)
    except:
        return "接続失敗", "接続失敗"

# 実行
ios_v, ios_d = get_ios()
and_v, and_d = get_android_info()

# 最終出力
print(f"【iOS】 {ios_v} （{ios_d}）")
print(f"【Android】 {and_v} （{and_d}）")
