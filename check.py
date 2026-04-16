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
        # 余計な空白やカンマを除去して分割
        p = date_text.replace(',', '').strip().split()
        if len(p) >= 3:
            return f"{p[2]}年{months.get(p[0], p[0])}月{p[1]}日"
        return date_text
    except:
        return date_text

def get_ios():
    """iOS版データの取得"""
    url = "https://itunes.apple.com/lookup?bundleId=com.waze.iphone&country=jp"
    try:
        r = requests.get(url, timeout=10).json()
        d = r["results"][0]
        v = d["version"]
        dt = datetime.strptime(d["currentVersionReleaseDate"], "%Y-%m-%dT%H:%M:%SZ")
        return v, dt.strftime("%Y年%m月%d日")
    except:
        return "---", "---"

def get_and():
    """Android版データの取得"""
    url = "https://www.apkmirror.com/apk/waze/"
    h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        r = requests.get(url, headers=h, timeout=15)
        # バージョン番号のみを抽出（余計なテキストを排除）
        v = re.search(r'fontBlack">Waze\s*([\d\.]+)', r.text).group(1)
        # 日付のみを抽出
        d_raw = re.search(r'datetime.*?">([^<]+)</span>', r.text).group(1)
        return v, format_date_jp(d_raw)
    except:
        return "---", "---"

# 実行と表示
ios_v, ios_d = get_ios()
and_v, and_d = get_and()

print(f"【iOS】 {ios_v} （{ios_d}）")
print(f"【Android】 {and_v} （{and_d}）")
