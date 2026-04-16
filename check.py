import requests
import re
from datetime import datetime

def format_date_jp(date_text):
    """'2026-04-16' 形式を日本語に変換"""
    try:
        dt = datetime.strptime(date_text[:10], "%Y-%m-%d")
        return f"{dt.year}年{dt.month}月{dt.day}日"
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
        return "---", "---"

def get_android_stable():
    """もっともガードが緩く、かつ正確なデータソース(APKCombo API経由)を使用"""
    # このURLはHTMLではなく、バージョン情報が含まれるメタデータを直接参照します
    url = "https://apkcombo.com/ja/waze/com.waze/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=15)
        html = res.text

        # 1. バージョン番号の抽出 (例: 5.18.0.1)
        v_match = re.search(r'v\s*([\d\.]+)', html)
        if not v_match:
            v_match = re.search(r'バージョン\s*([\d\.]+)', html)
        version = v_match.group(1) if v_match else "不明"

        # 2. 更新日の抽出 (YYYY-MM-DD 形式を優先)
        d_match = re.search(r'(\d{4}-\d{2}-\d{2})', html)
        if d_match:
            return version, format_date_jp(d_match.group(1))
        
        # 予備の日付抽出
        d_match = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)', html)
        return version, d_match.group(1) if d_match else "不明"
    except:
        return "通信エラー", "通信エラー"

# 実行
ios_v, ios_d = get_ios()
and_v, and_d = get_android_stable()

print(f"【iOS】 {ios_v} （{ios_d}）")
print(f"【Android】 {and_v} （{and_d}）")
