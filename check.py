import requests
import re
from datetime import datetime

def get_ios_info():
    url = "https://itunes.apple.com/lookup?bundleId=com.waze.iphone&country=jp"
    try:
        res = requests.get(url, timeout=10).json()
        data = res["results"][0]
        version = data["version"]
        # iOSの日付を変換
        date_raw = data["currentVersionReleaseDate"]
        date_dt = datetime.strptime(date_raw, "%Y-%m-%dT%H:%M:%SZ")
        date_str = date_dt.strftime("%Y年%m月%d日")
        return version, date_str
    except:
        return "取得失敗", "取得失敗"

def get_android_info():
    # ご指定のURLを使用
    url = "https://play.google.com/store/apps/details?id=com.waze&hl=ja&pli=1"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        res = requests.get(url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        html = res.text

        # 1. バージョン番号の抽出
        v_match = re.search(r'\[\[\["([\d\.]+)"\]\]\]', html)
        version = v_match.group(1) if v_match else "構造変化"
        
        # 2. 更新日の抽出（複数のパターンで検索）
        # パターンA: <div>内の直接テキスト
        d_match = re.search(r'更新日</div><div[^>]*>([^<]+)</div>', html)
        if not d_match:
            # パターンB: より広い範囲での検索
            d_match = re.search(r'Updated on</div><div[^>]*>([^<]+)</div>', html)
        
        # 3. 取得した日付の整理
        date_str = d_match.group(1) if d_match else "ページから取得できず"
        
        return version, date_str
    except Exception as e:
        return "接続失敗", f"エラー: {e}"

ios_v, ios_d = get_ios_info()
and_v, and_d = get_android_info()

print(f"【iOS版】バージョン: {ios_v} / 更新日: {ios_d}")
print(f"【Android版】バージョン: {and_v} / 更新日: {and_d}")
