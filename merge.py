import json
import urllib.request
import urllib.error

REPO_URLS = [
    "https://raw.githubusercontent.com/keiyoushi/extensions/repo/index.min.json",
    "https://raw.githubusercontent.com/yuzono/tachiyomi-extensions/repo/index.min.json",
    "https://raw.githubusercontent.com/Secozzi/aniyomi-extensions/repo/index.min.json",
    "https://raw.githubusercontent.com/yuzono/anime-extensions/repo/index.min.json",
]


def fetch_and_merge(urls, timeout=15):
    seen_packages = {}
    merged_extensions = []

    for url in urls:
        print(f"Fetching: {url}")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = json.loads(response.read().decode("utf-8"))

            extensions = data if isinstance(data, list) else (data.get("extensions") or [])

            added = 0
            for ext in extensions:
                if not isinstance(ext, dict):
                    continue
                pkg = ext.get("pkg")
                if pkg and pkg not in seen_packages:
                    seen_packages[pkg] = url
                    merged_extensions.append(ext)
                    added += 1
                elif pkg:
                    print(f"  Skipping duplicate {pkg} (already from {seen_packages[pkg]})")
            print(f"  Added {added} extensions from this repo")

        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
            print(f"Failed to fetch {url}: {e}")

    return merged_extensions


if __name__ == "__main__":
    combined = fetch_and_merge(REPO_URLS)

    with open("index.min.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, separators=(",", ":"), ensure_ascii=False)

    print(f"Successfully merged {len(combined)} extensions into index.min.json")