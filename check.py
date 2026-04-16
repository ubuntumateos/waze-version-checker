import requests
import re
import json

def get_ios_version():
    url = "https://itunes.apple.com/lookup?bundleId=com.waze.iphone&country=jp"
    try:
        res = requests.get(url).json()
        return res["results"][0]["version"]
    except:
        return "取得失敗"

def get_android_version():
    url = "https://play.google.com/store/apps/details?id=com.waze&hl=ja"
    try:
        res = requests.get(url)
        # ページ内のJSONデータからバージョン番号を抽出
        match = re.search(r'\[\[\["([\d\.]+)"\]\]\]', res.text)
        if match:
            return match.group(1)
        return "見つかりませんでした"
    except:
        return "取得失敗"

ios_v = get_ios_version()
and_v = get_android_version()

print(f"【iOS版】最新バージョンは {ios_v} です")
print(f"【Android版】最新バージョンは {and_v} です")
