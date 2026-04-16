import requests
import re
from datetime import datetime

def get_ios_info():
    url = "https://itunes.apple.com/lookup?bundleId=com.waze.iphone&country=jp"
    try:
        res = requests.get(url, timeout=10).json()
        data = res["results"][0]
        version = data["version"]
        # 日付を読みやすい形式に変換
        date_raw = data["currentVersionReleaseDate"]
        date_dt = datetime.strptime(date_raw, "%Y-%m-%dT%H:%M:%SZ")
        date_str = date_dt.strftime("%Y年%m月%d日")
        return version, date_str
    except:
        return "取得失敗", "取得失敗"

def get_android_info():
    url = "https://play.google.com/store/apps/details?id=com.waze&hl=ja"
    try:
        res = requests.get(url, timeout=10)
        # バージョン番号の抽出（最新のストア構造に対応）
        v_match = re.search(r'\[\[\["([\d\.]+)"\]\]\]', res.text)
        version = v_match.group(1) if v_match else "構造変化"
        
        # 更新日の抽出
        d_match = re.search(r'更新日</div><div class="reAt0">([^<]+)</div>', res.text)
        date_str = d_match.group(1) if d_match else "不明"
        
        return version, date_str
    except:
        return "取得失敗", "取得失敗"

ios_v, ios_d = get_ios_info()
and_v, and_d = get_android_info()

print(f"【iOS版】バージョン: {ios_v} / 更新日: {ios_d}")
print(f"【Android版】バージョン: {and_v} / 更新日: {and_d}")
