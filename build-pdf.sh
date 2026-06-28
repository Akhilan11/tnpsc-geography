#!/bin/bash
# Build a single combined HTML from all chapters, then produce a PDF.

set -e
cd "$(dirname "$0")"

OUT_HTML="book-print.html"
OUT_PDF="TNPSC-Geography-Book.pdf"

echo "[1/3] Building combined HTML..."

# Head
cat > "$OUT_HTML" <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Indian Geography — TNPSC Group 1 Master Volume</title>
<link rel="stylesheet" href="assets/css/fonts.css">
<link rel="stylesheet" href="assets/css/book.css">
<style>
@page { size: A4; margin: 18mm 15mm; }
body { background: white; }
.topbar, .chapter-nav, .chapter-aside { display: none !important; }
.chapter-shell { display: block; padding: 0 0 30px; max-width: 100%; }
.chapter-body { max-width: 100%; }
h1.chapter-title { page-break-before: always; }
.cover { text-align: center; padding: 80px 0; page-break-after: always; }
.cover h1 { font-family: 'Inter Tight', sans-serif; font-weight: 900; font-size: 64px; line-height: 1; letter-spacing: -0.03em; margin: 0 0 24px; }
.cover .sub { font-size: 22px; color: #2b2b2b; margin-bottom: 60px; }
.cover .meta { font-family: monospace; font-size: 12px; letter-spacing: 0.2em; color: #6b6b66; }
.cover .accent-bar { width: 100px; height: 6px; background: linear-gradient(135deg, #3b78e7, #224fa8); margin: 24px auto; }
.section-divider { page-break-before: always; padding: 100px 0; text-align: center; }
.section-divider h2 { font-family: 'Inter Tight', sans-serif; font-weight: 900; font-size: 48px; letter-spacing: -0.03em; margin: 0; }
.section-divider .label { font-family: monospace; font-size: 12px; color: #3b78e7; letter-spacing: 0.2em; }
.mcq__ans { display: block !important; }
.mcq__ans summary { display: none; }
.mcq__ans p { margin-top: 8px !important; }
</style>
</head>
<body>

<div class="cover">
  <div class="meta">TNPSC GROUP 1 · GEOGRAPHY · EDITION 2026</div>
  <h1>Indian<br>Geography.</h1>
  <div class="accent-bar"></div>
  <div class="sub">A Master Volume — 30 chapters, ~500 pages, 340+ MCQs</div>
  <div class="meta">A complete textbook for the serious TNPSC Group 1 aspirant</div>
</div>

EOF

# Append each chapter's <main>...</main> body
for f in chapters/ch*.html; do
  echo "  Adding $f..."
  python3 - "$f" >> "$OUT_HTML" <<'PYEOF'
import sys, re
with open(sys.argv[1]) as f:
    html = f.read()
m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
if m:
    body = m.group(1)
    # Remove chapter-aside block
    body = re.sub(r'<aside class="chapter-aside".*?</aside>', '', body, flags=re.DOTALL)
    # Convert <details><summary>...</summary>...</details> to inline visible
    body = re.sub(r'<details class="mcq__ans"[^>]*>\s*<summary[^>]*>[^<]*</summary>', '<div class="mcq__ans">', body)
    body = body.replace('</details>', '</div>')
    print(body)
PYEOF
done

echo "</body></html>" >> "$OUT_HTML"

echo "[2/3] Combined HTML written → $OUT_HTML ($(wc -l < "$OUT_HTML") lines)"

echo "[3/3] Generating PDF with Chrome headless..."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$OUT_PDF" \
  --print-to-pdf-no-header \
  --virtual-time-budget=10000 \
  "file://$(pwd)/$OUT_HTML"

ls -lh "$OUT_PDF"
echo ""
echo "Done! PDF saved at: $(pwd)/$OUT_PDF"
