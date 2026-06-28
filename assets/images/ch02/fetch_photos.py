"""
Search Wikimedia Commons and download real photos for Ch 2.

Uses the proper Commons API (no hard-coded URLs).
"""
import os, sys, json, time, urllib.parse, urllib.request, urllib.error

OUT = "/Users/aniket/Documents/TNPSC-Geography/assets/images/ch02"
os.makedirs(OUT, exist_ok=True)

UA = ("TNPSCBookBuilder/1.0 (educational personal project; "
      "non-commercial; Python-urllib)")

API = "https://commons.wikimedia.org/w/api.php"

# Map: output filename → (search query, preferred file substring)
QUERIES = {
    "kanyakumari.jpg": (
        "Vivekananda Rock Memorial Thiruvalluvar statue Kanyakumari",
        "Vivekananda"),
    "indira-point.jpg": (
        "Pygmalion Point lighthouse Great Nicobar India",
        "Great_Nicobar"),
    "adams-bridge-satellite.jpg": (
        "Adam's Bridge Rama Setu NASA satellite",
        "Ram"),
    "pamban-bridge.jpg": (
        "Pamban Bridge Rameswaram",
        "Pamban"),
    "wagah-border.jpg": (
        "Wagah border ceremony India Pakistan flag",
        "Wagah"),
    "earth-from-apollo.jpg": (
        "Earth Apollo 17 Blue Marble",
        "Apollo_17"),
    "marina-beach.jpg": (
        "Marina Beach Chennai",
        "Marina"),
    "ist-clock.jpg": (
        "Allahabad Mirzapur clock standard time India",
        "Mirzapur"),
}


def http_get(url, raw=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if raw else json.loads(data)


def search_commons(query, want_substr=None):
    """Return the best matching file title."""
    params = {
        "action": "query", "list": "search",
        "srsearch": query, "srnamespace": "6",
        "srlimit": "10", "format": "json"
    }
    url = API + "?" + urllib.parse.urlencode(params)
    try:
        data = http_get(url)
    except Exception as e:
        print(f"    search error: {e}")
        return None
    results = data.get("query", {}).get("search", [])
    if not results:
        return None
    if want_substr:
        for r in results:
            if want_substr.lower() in r["title"].lower():
                return r["title"]
    return results[0]["title"]


def get_image_url(title, width=1200, attempts=3):
    params = {
        "action": "query", "titles": title,
        "prop": "imageinfo", "iiprop": "url|extmetadata",
        "iiurlwidth": str(width),
        "format": "json"
    }
    url = API + "?" + urllib.parse.urlencode(params)
    for i in range(attempts):
        try:
            data = http_get(url)
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < attempts - 1:
                print(f"    429 retry in {6*(i+1)}s...")
                time.sleep(6 * (i + 1))
                continue
            raise
    pages = data.get("query", {}).get("pages", {})
    for _, p in pages.items():
        ii = p.get("imageinfo", [])
        if ii:
            return ii[0].get("thumburl") or ii[0].get("url"), ii[0].get("extmetadata", {})
    return None, None


def download(out_name, search_query, want_substr):
    print(f"\n→ {out_name}")
    title = search_commons(search_query, want_substr)
    if not title:
        print("    ✗ no match in search")
        return False
    print(f"    matched: {title}")
    url, meta = get_image_url(title, width=1200)
    if not url:
        print("    ✗ no imageinfo URL")
        return False
    print(f"    URL: {url[:90]}")
    try:
        img = http_get(url, raw=True)
        out_path = os.path.join(OUT, out_name)
        with open(out_path, "wb") as f:
            f.write(img)
        size_kb = len(img) // 1024
        # Save attribution
        if meta:
            cred = (meta.get("Artist", {}).get("value", "") or "").strip()
            lic = (meta.get("LicenseShortName", {}).get("value", "") or "").strip()
            attr_path = os.path.join(OUT, out_name + ".attribution.txt")
            with open(attr_path, "w") as f:
                f.write(f"Title: {title}\n")
                f.write(f"URL: {url}\n")
                f.write(f"Artist/Author: {cred}\n")
                f.write(f"License: {lic}\n")
                f.write(f"Source: Wikimedia Commons\n")
            print(f"    ✓ saved {size_kb} KB · License: {lic}")
        return True
    except Exception as e:
        print(f"    ✗ download error: {e}")
        return False


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    ok = 0
    for name, (query, substr) in QUERIES.items():
        if only and not only in name:
            continue
        if download(name, query, substr):
            ok += 1
        time.sleep(4)  # respect rate limits
    print(f"\nDone. {ok}/{len(QUERIES)} downloaded.")
