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
    """APKCombo から Android 版のバージョンと更新日を取得"""
    url = "https://apkcombo.com/ja/waze/com.waze/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text

        # バージョン抽出
        version = "不明"
        version_patterns = [
            r'v\s*([\d\.]+)',
            r'バージョン\s*([\d\.]+)',
            r'Version\s*([\d\.]+)',
        ]
        for pattern in version_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                version = match.group(1)
                break

        # 更新日抽出
        updated = "不明"

        # YYYY-MM-DD
        match_date = re.search(r'(\d{4}-\d{2}-\d{2})', html)
        if match_date:
            updated = format_date_jp(match_date.group(1))
        else:
            # YYYY年M月D日
            match_date_jp = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)', html)
            if match_date_jp:
                updated = match_date_jp.group(1)

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
    
