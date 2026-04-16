import requests
import re
from datetime import datetime

# 英語の日付を日本語に変換するための処理
def format_to_japanese(date_text):
    # 月の英語名を数字に変換する辞書
    months = {
        'January': '1', 'February': '2', 'March': '3', 'April': '4',
        'May': '5', 'June': '6', 'July': '7', 'August': '8',
        'September': '9', 'October': '10', 'November': '11', 'December': '12'
    }
    try:
        # APKMirrorの形式 "April 16, 2026" を想定
        # カンマを取り除いて分割
        parts = date_text.replace(',', '').split()
        if len(parts) >= 3:
            m = months.get(parts[0], parts[0])
            d = parts[1]
            y = parts[2]
            return f"{y}年{m}月{d}日"
        return date_text
    except:
        return date_text

def get_ios_info():
    url = "https://itunes.apple.com/lookup?bundleId=com.waze.iphone&country=jp"
    try:
        res = requests.get(url, timeout=10).json()
        data = res["results"][0]
        version = data["version"]
        date_raw = data["currentVersionReleaseDate"]
        date_dt = datetime.strptime(date_raw, "%Y-%m-%dT%H:%M:%SZ")
        date_str = date_dt.strftime("%Y年%m月%d日")
        return version, date_str
    except:
        return "取得失敗", "取得失敗"

def get_apkmirror_info():
    url = "https://www.apkmirror.com/apk/waze/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        html = res.text

        # 1. 最新のバージョン名を抽出
        v_match = re.search(r'fontBlack">Waze\s*([\d\.]+)', html)
        version = v_match.group(1) if v_match else "バージョン取得失敗"

        # 2. 更新日を抽出
        d_match = re.search(r'datetime.*?">([^<]+)</span>', html)
        date_raw = d_match.group(1) if d_match else "日付取得失敗"
        
        # 日本語に変換
        date_jp = format_to_japanese(date_raw.strip())

        return version, date_jp
    except Exception as e:
        return "接続失敗", f"エラー: {e}"

ios_v, ios_d = get_ios_info()
apk_v, apk_d = get_apkmirror_info()

print(f"【iOS版】バージョン: {ios_v} / 更新日: {ios_d}")
print(f"【APKMirror (Android)】バージョン: {apk_v} / 更新日: {apk_d}")
