"""
Generate accuracy-conscious maps for Ch 2 via OpenAI gpt-image-1.

Each prompt is engineered to:
 - List every label letter-exact
 - Use a clean infographic style (not a "real map" style)
 - Avoid the model trying to invent extra states / details

After each generation we PRINT the prompt's expected labels so a
human can verify before swap-in.
"""
import os, sys, json, base64, urllib.request, urllib.error

API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    print("ERROR: OPENAI_API_KEY not set"); sys.exit(1)

OUT = "/Users/aniket/Documents/TNPSC-Geography/assets/images/ch02"
os.makedirs(OUT, exist_ok=True)
URL = "https://api.openai.com/v1/images/generations"

PROMPTS = {

    # ---- 1. Tropic of Cancer · 8 states ----
    "map-tropic": {
        "size": "1536x1024",
        "must_have_labels": [
            "Gujarat", "Rajasthan", "Madhya Pradesh", "Chhattisgarh",
            "Jharkhand", "West Bengal", "Tripura", "Mizoram",
            "TROPIC OF CANCER", "23",
        ],
        "prompt": (
            "A clean modern educational infographic-style map of India "
            "highlighting only the 8 states that the Tropic of Cancer crosses. "
            "Style: flat vector look, soft cream off-white background, "
            "navy blue map outline, the 8 highlighted states filled in "
            "warm terracotta with white state names printed clearly inside. "
            "Other Indian states shown in pale grey. "
            "A bold dashed horizontal red-orange line runs across the middle of "
            "the map labelled \"TROPIC OF CANCER · 23° 30' N\" near the right edge. "
            "\n\n"
            "Each of the 8 highlighted states must show TWO things, in this exact "
            "spelling: a small white circular number badge with the number 1 to 8, "
            "and the state name in clean sans-serif text. Number them strictly "
            "west to east in this order:\n"
            "  1 = Gujarat\n"
            "  2 = Rajasthan\n"
            "  3 = Madhya Pradesh\n"
            "  4 = Chhattisgarh\n"
            "  5 = Jharkhand\n"
            "  6 = West Bengal\n"
            "  7 = Tripura\n"
            "  8 = Mizoram\n"
            "\n"
            "Title bar at top in dark navy: 'TROPIC OF CANCER  · 8 STATES OF INDIA'. "
            "Subtitle: 'Numbered west to east'. "
            "Footer: 'TNPSC Group 1 · Geography'. "
            "\n\n"
            "Important rules: do NOT add any other state names. Do NOT add any "
            "country names. Do NOT spell any of the 8 state names differently "
            "from above — spelling must match exactly, especially Chhattisgarh "
            "(double h, single t), West Bengal (two words), and Mizoram. "
            "Wide landscape composition, premium textbook quality."
        ),
    },

    # ---- 2. Standard Meridian · 5 states ----
    "map-meridian": {
        "size": "1024x1536",
        "must_have_labels": [
            "Uttar Pradesh", "Madhya Pradesh", "Chhattisgarh",
            "Odisha", "Andhra Pradesh", "82", "30", "Mirzapur",
            "STANDARD MERIDIAN",
        ],
        "prompt": (
            "A clean modern educational infographic-style map of India "
            "highlighting the 5 states the Standard Meridian (82° 30' E) crosses. "
            "Style: flat vector, soft cream background, navy outlines. The 5 "
            "highlighted states filled in deep blue with white text. Other Indian "
            "states shown in pale grey. "
            "\n\n"
            "A bold dashed vertical line runs from north to south through the "
            "centre of India labelled \"STANDARD MERIDIAN · 82° 30' E\" near the "
            "bottom. A small gold dot marks the city Mirzapur, labelled "
            "'Mirzapur (UP)'. \n\n"
            "Number the 5 highlighted states 1 to 5, north to south, in this "
            "exact spelling:\n"
            "  1 = Uttar Pradesh\n"
            "  2 = Madhya Pradesh\n"
            "  3 = Chhattisgarh\n"
            "  4 = Odisha\n"
            "  5 = Andhra Pradesh\n"
            "\n"
            "Title at top: 'STANDARD MERIDIAN · 5 STATES'. Subtitle: "
            "'Numbered north to south'. Footer: 'TNPSC Group 1 · Geography'. "
            "An IST callout box in the lower-left says in two lines: "
            "'INDIAN STANDARD TIME' / 'UTC + 5:30'. "
            "\n\n"
            "Important: spell all 5 state names exactly as above, especially "
            "Chhattisgarh (double h). Do not add any other state names. "
            "Portrait composition."
        ),
    },

    # ---- 3. Four extreme points ----
    "map-extremes": {
        "size": "1024x1536",
        "must_have_labels": [
            "Indira Col", "Kanyakumari", "Indira Point",
            "Guhar Moti", "Kibithoo", "NORTH", "SOUTH", "EAST", "WEST",
        ],
        "prompt": (
            "A clean modern educational infographic map of India showing the "
            "country's four extreme points. Style: flat vector, soft cream "
            "background, India filled in warm terracotta, country outlined in "
            "navy. Pale grey for neighbouring countries (Pakistan, China, Nepal, "
            "Bangladesh, Myanmar, Sri Lanka). \n\n"
            "Mark four extreme points with large gold circular badges and connect "
            "each to a clean white label card via a thin line. The badges and "
            "their labels must read EXACTLY as follows:\n"
            "  NORTH — 'Indira Col, Ladakh · 37° 6' N'\n"
            "  SOUTH (mainland) — 'Kanyakumari, Tamil Nadu · 8° 4' N'\n"
            "  SOUTH (territory) — 'Indira Point, Great Nicobar · 6° 45' N'\n"
            "  WEST — 'Guhar Moti, Gujarat · 68° 7' E'\n"
            "  EAST — 'Kibithoo, Arunachal Pradesh · 97° 25' E'\n"
            "\n"
            "A subtle dashed line across the country marks the Tropic of Cancer "
            "(23.5° N). Title at top in navy: 'INDIA · FOUR EXTREME POINTS'. "
            "Footer: 'TNPSC Group 1 · Geography'. "
            "\n\n"
            "Important: place names must be spelled exactly as above, "
            "especially 'Kibithoo' (one word), 'Kanyakumari' (one word), and "
            "'Indira Col'. Portrait composition. Premium textbook quality."
        ),
    },

    # ---- 4. Seven maritime neighbours ----
    "map-maritime": {
        "size": "1536x1024",
        "must_have_labels": [
            "Pakistan", "Maldives", "Sri Lanka", "Bangladesh",
            "Myanmar", "Thailand", "Indonesia",
        ],
        "prompt": (
            "A clean modern educational infographic map of India and the Indian "
            "Ocean region, showing the seven maritime neighbours of India. "
            "Style: flat vector, off-white background. India filled in warm "
            "terracotta. The seven maritime neighbours filled in soft rose-pink. "
            "Sea / ocean filled in pale blue. \n\n"
            "Label each of the seven maritime neighbours with its name in clean "
            "sans-serif text on a small white card. The names, spelled exactly:\n"
            "  Pakistan (north-west)\n"
            "  Maldives (south-west)\n"
            "  Sri Lanka (south, across Palk Strait)\n"
            "  Bangladesh (east)\n"
            "  Myanmar (east)\n"
            "  Thailand (south-east)\n"
            "  Indonesia (south-east)\n"
            "\n"
            "Show four sea channels as dashed blue lines with labels:\n"
            "  '10° Channel' between Andaman and Nicobar islands\n"
            "  '9° Channel' within Lakshadweep\n"
            "  '8° Channel' between Lakshadweep (Minicoy) and Maldives\n"
            "  '6° Channel' between Great Nicobar and Indonesia\n"
            "\n"
            "Title at top: 'INDIA · SEVEN MARITIME NEIGHBOURS'. Footer: "
            "'TNPSC Group 1 · Geography'. \n\n"
            "Important: spell every country name exactly as above. Do not invent "
            "any extra countries. Do not label India's land neighbours like Nepal "
            "or Bhutan. Landscape composition, premium quality."
        ),
    },

    # ---- 5. Palk Strait / Adam's Bridge ----
    "map-palk": {
        "size": "1536x1024",
        "must_have_labels": [
            "Tamil Nadu", "Sri Lanka", "Palk Strait", "Gulf of Mannar",
            "Adam's Bridge", "Rameswaram", "Dhanushkodi", "Mannar",
        ],
        "prompt": (
            "A clean modern educational close-up map of the southeast Tamil Nadu "
            "coast and the north-west tip of Sri Lanka. Style: flat vector, "
            "pale blue ocean, Tamil Nadu in warm terracotta labelled 'TAMIL NADU "
            "(Ramanathapuram district)', Sri Lanka in rose-pink labelled "
            "'SRI LANKA'. \n\n"
            "Show a chain of small gold dots running from the Indian coast at "
            "'Dhanushkodi' to the Sri Lankan coast at 'Mannar' — label this chain "
            "'Adam's Bridge (Ram Setu) — limestone shoals'. \n\n"
            "Place a clear label box NORTH of the chain in the water reading "
            "'PALK STRAIT'. Place another label box SOUTH of the chain reading "
            "'GULF OF MANNAR (Marine Biosphere)'. \n\n"
            "Also mark and label these towns with small navy dots: "
            "'Rameswaram', 'Dhanushkodi', 'Pamban Bridge', 'Mannar', 'Talaimannar'. \n\n"
            "Title at top: 'PALK STRAIT · TAMIL NADU ↔ SRI LANKA'. Footer: "
            "'TNPSC Group 1 · Geography'. \n\n"
            "Important: spell every name exactly as listed. Place the Palk "
            "Strait label NORTH of the shoal chain and the Gulf of Mannar SOUTH "
            "of it — this is the most-tested fact. Landscape composition."
        ),
    },
}


def gen(name, spec):
    print(f"\n=== Generating: {name} ===")
    print(f"    Expected labels: {spec['must_have_labels']}")
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
        with urllib.request.urlopen(req, timeout=300) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:600]}")
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
    print(f"  No image data: {json.dumps(item)[:300]}")
    return None


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for name, spec in PROMPTS.items():
        if only and name != only:
            continue
        gen(name, spec)
