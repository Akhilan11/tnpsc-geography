"""
Generate aesthetic chapter-opener images for Ch 2 via OpenAI gpt-image-1.

POLICY:
  - These are decorative / conceptual illustrations only.
  - We do NOT use AI image gen for maps or factual diagrams.
  - All prompts include "no text, no labels" to prevent hallucinated info.
"""
import os, sys, json, base64, urllib.request, urllib.error

API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    print("ERROR: OPENAI_API_KEY not set"); sys.exit(1)

OUT = "/Users/aniket/Documents/TNPSC-Geography/assets/images/ch02"
os.makedirs(OUT, exist_ok=True)

URL = "https://api.openai.com/v1/images/generations"

PROMPTS = {
    "opener-hero": {
        "size": "1536x1024",
        "prompt": (
            "An elegant editorial illustration for a premium Indian geography textbook. "
            "Subject: the Indian subcontinent on a stylised antique-paper globe, gently "
            "rotated to face the viewer, with very faint latitude/longitude lines. "
            "Around it: subtle motifs of soft monsoon clouds, palm trees, a temple "
            "gopuram silhouette in the far distance, a fishing boat on a calm sea. "
            "Style: refined watercolour and ink, soft warm earthy palette of cream, "
            "ochre, terracotta, deep teal, soft sky blue. Texture like a Penguin "
            "Classics or Aramco World cover. "
            "Absolutely no text, no labels, no country names, no flags, no people, "
            "no political markings, no compass labels. Pure aesthetic illustration. "
            "Landscape composition with generous breathing room around the centre."
        ),
    },
    "tropic-concept": {
        "size": "1536x1024",
        "prompt": (
            "Editorial conceptual illustration showing a stylised horizontal divide "
            "across an Indian landscape: the upper half cooler with pine and "
            "snow-touched mountains in muted blue-grey, the lower half warm with palm "
            "trees, paddy fields and coastline in golden ochre and deep green. A "
            "single faint dotted horizontal line crosses the middle, suggesting a "
            "latitude. Sky transitions softly. Soft watercolour and ink, warm earthy "
            "palette, premium magazine quality. "
            "No text, no labels, no place names, no people, no flags. Landscape."
        ),
    },
    "monsoon-concept": {
        "size": "1536x1024",
        "prompt": (
            "Editorial conceptual illustration of the Indian south-west monsoon. "
            "Stylised view from above an indistinct landmass shaped loosely like a "
            "subcontinent, with soft curved arrows of misty clouds and rain sweeping "
            "from the lower-left ocean toward the upper-right mountains. Heavy soft "
            "rain over the western coast and mountains. Style: refined watercolour, "
            "wet-into-wet blues and greys with ochre coastline. Premium textbook "
            "aesthetic. "
            "No text, no labels, no place names, no flags, no people, no compass "
            "rose. Landscape composition."
        ),
    },
}

def gen(name, spec):
    print(f"\n=== Generating: {name} ===")
    body = {
        "model": "gpt-image-1",
        "prompt": spec["prompt"],
        "size": spec["size"],
        "n": 1,
        "quality": "high",
    }
    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=240) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:700]}")
        return None
    data = resp.get("data", [])
    if not data:
        print(f"  Empty response: {json.dumps(resp)[:300]}")
        return None
    item = data[0]
    if "b64_json" in item and item["b64_json"]:
        out = f"{OUT}/{name}.png"
        with open(out, "wb") as f:
            f.write(base64.b64decode(item["b64_json"]))
        print(f"  Saved: {out} ({os.path.getsize(out)//1024} KB)")
        return out
    if "url" in item:
        out = f"{OUT}/{name}.png"
        urllib.request.urlretrieve(item["url"], out)
        print(f"  Downloaded from URL: {out} ({os.path.getsize(out)//1024} KB)")
        return out
    print(f"  No image data: {json.dumps(item)[:300]}")
    return None

if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for name, spec in PROMPTS.items():
        if only and name != only:
            continue
        gen(name, spec)
    print("\nDone.")
