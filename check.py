import requests
import re

def get_ios_version():
    url = "https://itunes.apple.com/lookup?bundleId=com.waze.iphone&country=jp"
    try:
        res = requests.get(url, timeout=10).json()
        return res["results"][0]["version"]
    except Exception as e:
        return f"取得失敗 ({e})"

def get_android_version():
    url = "https://play.google.com/store/apps/details?id=com.waze&hl=ja"
    try:
        res = requests.get(url, timeout=10)
        # Google Playの特殊なJSON形式からバージョン番号を抽出
        match = re.search(r'\[\[\["([\d\.]+)"\]\]\]', res.text)
        if match:
            return match.group(1)
        return "バージョン構造が見つかりません"
    except Exception as e:
        return f"取得失敗 ({e})"

ios_v = get_ios_version()
and_v = get_android_version()

print(f"【iOS版】最新バージョンは {ios_v} です")
print(f"【Android版】最新バージョンは {and_v} です")
