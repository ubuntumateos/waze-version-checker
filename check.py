import requests
import re
from datetime import datetime


def format_date_jp(date_text):
    """日付文字列を YYYY年M月D日 に変換"""
    if not date_text:
        return "不明"

    patterns = [
        ("%Y-%m-%d", date_text[:10]),
        ("%Y-%m-%dT%H:%M:%SZ", date_text),
    ]

    for fmt, value in patterns:
        try:
            dt = datetime.strptime(value, fmt)
            return f"{dt.year}年{dt.month}月{dt.day}日"
        except:
            pass

    return date_text


def get_ios_info():
    """App Store から iOS 版のバージョンと更新日を取得"""
    url = "https://itunes.apple.com/lookup?bundleId=com.waze.iphone&country=jp"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            return {
                "platform": "iOS",
                "version": "不明",
                "updated": "不明"
            }

        app = data["results"][0]
        version = app.get("version", "不明")
        updated = format_date_jp(app.get("currentVersionReleaseDate", ""))

        return {
            "platform": "iOS",
            "version": version,
            "updated": updated
        }

    except Exception:
        return {
            "platform": "iOS",
            "version": "取得失敗",
            "updated": "取得失敗"
        }


def get_android_info():
    """Google Play ストアから Android 版のバージョンと更新日を取得"""
    url = "https://play.google.com/store/apps/details?id=com.waze&hl=ja&gl=JP"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text

        # バージョン抽出
        versions = re.findall(r'"(\d+\.\d+\.\d+\.\d+)"', html)
        if not versions:
            versions = re.findall(r'"(\d+\.\d+\.\d+)"', html)
        
        def parse_version(v):
            return [int(x) for x in v.split('.')]
            
        version = "不明"
        if versions:
            versions.sort(key=parse_version, reverse=True)
            version = versions[0]

        # 更新日抽出
        updated = "不明"
        date_pattern = r'"(\d{4}年\d{1,2}月\d{1,2}日)"'
        date_match = re.search(date_pattern, html)
        if date_match:
            updated = date_match.group(1)
        else:
            date_pattern2 = r'"(\d{4}/\d{2}/\d{2})"'
            date_match2 = re.search(date_pattern2, html)
            if date_match2:
                parts = date_match2.group(1).split('/')
                updated = f"{parts[0]}年{int(parts[1])}月{int(parts[2])}日"

        return {
            "platform": "Android",
            "version": version,
            "updated": updated
        }

    except Exception:
        return {
            "platform": "Android",
            "version": "取得失敗",
            "updated": "取得失敗"
        }


def print_app_versions(app_name="Waze"):
    ios_info = get_ios_info()
    android_info = get_android_info()

    print(f"=== {app_name} バージョン情報 ===")
    print(f"{'OS':<10} {'バージョン':<15} {'更新日'}")
    print("-" * 40)
    print(f"{ios_info['platform']:<10} {ios_info['version']:<15} {ios_info['updated']}")
    print(f"{android_info['platform']:<10} {android_info['version']:<15} {android_info['updated']}")


if __name__ == "__main__":
    print_app_versions("Waze")
    
