"""
Try Gemini's native image generation (gemini-2.5-flash-image / gemini-3.x).
These return images inline in a multi-modal response.
"""
import os, sys, json, base64, urllib.request, urllib.error

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not set"); sys.exit(1)

OUT = "/Users/aniket/Documents/TNPSC-Geography/assets/images/ch02"

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemini-2.5-flash-image"
OUTFILE = sys.argv[2] if len(sys.argv) > 2 else "opener-hero.png"
PROMPT = (
    "Generate an editorial illustration for an Indian geography textbook "
    "chapter on 'India in the World'. Soft watercolour style, muted earthy "
    "palette of warm beiges, ochres, deep teals and soft blues. "
    "Stylised globe with India highlighted, faint latitude/longitude grid. "
    "Subtle motifs of the Indian Ocean. Premium magazine quality. "
    "No text, no labels, no people, no flags. 16:9 landscape."
)

URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

body = {
    "contents": [
        {"parts": [{"text": PROMPT}], "role": "user"}
    ],
    "generationConfig": {
        "responseModalities": ["IMAGE", "TEXT"],
    },
}

print(f"=== Using model: {MODEL} ===")
req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                             headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=180) as r:
        resp = json.loads(r.read())
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:800]}")
    sys.exit(1)

candidates = resp.get("candidates", [])
if not candidates:
    print("No candidates:", json.dumps(resp)[:600])
    sys.exit(1)

found = False
for part in candidates[0].get("content", {}).get("parts", []):
    if "inlineData" in part:
        b64 = part["inlineData"].get("data")
        mime = part["inlineData"].get("mimeType", "image/png")
        ext = mime.split("/")[-1]
        out = f"{OUT}/{OUTFILE}"
        if not out.endswith("." + ext):
            out = f"{OUT}/{os.path.splitext(OUTFILE)[0]}.{ext}"
        with open(out, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f"  Saved: {out} ({os.path.getsize(out)//1024} KB)")
        found = True
    elif "text" in part:
        print("  Text:", part["text"][:200])
if not found:
    print("No image part in response:", json.dumps(resp)[:600])
