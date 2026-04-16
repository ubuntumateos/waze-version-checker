import requests
import re

def format_date_jp(date_text):
    """英語の日付（Month Day, Year）を日本語形式に変換"""
    months = {
        'January': '1', 'February': '2', 'March': '3', 'April': '4',
        'May': '5', 'June': '6', 'July': '7', 'August': '8',
        'September': '9', 'October': '10', 'November': '11', 'December': '12'
    }
    try:
        # 例: "April 14, 2026" -> ["April", "14", "2026"]
        p = date_text.replace(',', '').strip().split()
        if len(p) >= 3:
            return f"{p[2]}年{months.get(p[0], p[0])}月{p[1]}日"
        return date_text
    except:
        return date_text

def get_ios():
    """iOS版データの取得（Apple API）"""
    url = "https://itunes.apple.com/lookup?bundleId=com.waze.iphone&country=jp"
    try:
        r = requests.get(url, timeout=10).json()
        d = r["results"][0]
        from datetime import datetime
        dt = datetime.strptime(d["currentVersionReleaseDate"], "%Y-%m-%dT%H:%M:%SZ")
        return d["version"], dt.strftime("%Y年%m月%d日")
    except:
        return "取得失敗", "取得失敗"

def get_and_official():
    """Android版データの取得（Waze公式ヘルプページ）"""
    url = "https://support.google.com/waze/answer/6271171"
    try:
        # 公式サイトはボット対策があるためUser-Agentを設定
        h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        r = requests.get(url, headers=h, timeout=15)
        r.encoding = 'utf-8'
        html = r.text

        # 1. 最初の <h2> タブなどに記載されているバージョンを探す
        # 形式例: "Android: 4.102.0.1"
        v_match = re.search(r'Android:\s*([\d\.]+)', html)
        version = v_match.group(1) if v_match else "不明"

        # 2. ページ内の一番最初に出てくる日付（例: April 14, 2026）を探す
        # ページ上部の更新情報を狙います
        d_match = re.search(r'([A-Z][a-z]+ \d{1,2}, \d{4})', html)
        date_raw = d_match.group(1) if d_match else "不明"
        
        return version, format_date_jp(date_raw)
    except:
        return "接続失敗", "接続失敗"

# 実行
ios_v, ios_d = get_ios()
and_v, and_d = get_and_official()

print(f"【iOS】 {ios_v} （{ios_d}）")
print(f"【Android】 {and_v} （{and_d}）")
