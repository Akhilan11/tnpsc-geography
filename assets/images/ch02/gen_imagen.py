"""
Generate chapter-opener / illustrative images for Chapter 2 via Imagen 4.

We use Imagen ONLY for aesthetic / illustrative images — never for maps
or factual diagrams (those stay as Natural Earth renders).

Each image is saved as PNG; Claude then verifies the result is on-brief
before it gets embedded.
"""
import os, sys, json, base64, urllib.request, urllib.error

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not set"); sys.exit(1)

OUT = "/Users/aniket/Documents/TNPSC-Geography/assets/images/ch02"
os.makedirs(OUT, exist_ok=True)

MODEL = "imagen-4.0-generate-001"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predict?key={API_KEY}"

PROMPTS = {
    "opener-hero": {
        "prompt": (
            "An elegant minimalist editorial illustration for an Indian "
            "geography textbook chapter on 'India in the World'. "
            "Style: soft watercolour, muted earthy palette of warm beiges, "
            "ochres, deep teals and soft blue, premium magazine quality. "
            "Composition: a stylised globe gently rotating to highlight the Indian "
            "subcontinent, with subtle latitude / longitude grid lines. "
            "Surrounding it, faint motifs of the Indian Ocean, lotus, banyan tree "
            "silhouettes, a temple gopuram in the distance. "
            "Clean, calm, refined — like a Penguin Classics cover. "
            "No text. No people. No flags. 16:9 landscape."
        ),
        "aspect": "16:9",
    },
    "tropic-illustration": {
        "prompt": (
            "Elegant editorial illustration showing the concept of the Tropic of "
            "Cancer dividing a stylised landscape into a tropical lush green south "
            "and a sub-tropical drier north. Style: soft watercolour, India-inspired "
            "warm palette (terracotta, ochre, deep greens, dusty pink), like a "
            "Penguin Classics book cover. A single dotted horizontal line "
            "represents the Tropic. Faint silhouettes of a palm tree in the south "
            "and pine on the north. Calm, refined, no text, no labels, no people. "
            "16:9 landscape."
        ),
        "aspect": "16:9",
    },
    "monsoon-arrows": {
        "prompt": (
            "An editorial illustration of the south-west monsoon over the Indian "
            "subcontinent. Style: soft watercolour, muted blues and greys, with "
            "warm earth tones for land. Curved soft arrows show winds sweeping from "
            "the Indian Ocean across the subcontinent toward the Himalayas. The "
            "Himalayas appear as a faint mountain range silhouette at the top. "
            "No text, no labels, no people, no flags. 16:9 landscape. "
            "Magazine-quality, refined, suitable for a premium textbook."
        ),
        "aspect": "16:9",
    },
}

def gen(name, prompt, aspect):
    print(f"\n=== Generating: {name} ===")
    body = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": aspect,
            "personGeneration": "dont_allow",
        }
    }
    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:500]}")
        return None
    if "predictions" not in resp or not resp["predictions"]:
        print(f"  Empty response: {json.dumps(resp)[:300]}")
        return None
    img_b64 = resp["predictions"][0].get("bytesBase64Encoded")
    if not img_b64:
        print(f"  No image bytes: keys={list(resp['predictions'][0].keys())}")
        return None
    path = f"{OUT}/{name}.png"
    with open(path, "wb") as f:
        f.write(base64.b64decode(img_b64))
    print(f"  Saved: {path} ({os.path.getsize(path)//1024} KB)")
    return path

if __name__ == "__main__":
    # generate just the hero first to validate before spending more
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for name, spec in PROMPTS.items():
        if only and name != only:
            continue
        gen(name, spec["prompt"], spec["aspect"])
    print("\nDone.")
