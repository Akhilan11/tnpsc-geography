"""
Ch 3 maps — clearer v2.

Improvements vs v1:
- Larger figures (higher DPI, more pixels)
- Stronger colours, less wash
- Smart label placement so arrows don't cross each other
- Cleaner basemap (water blue, land beige, India highlighted)
- Bigger fonts, bigger markers
"""
import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = "/Users/aniket/Documents/TNPSC-Geography/assets/images/ch03"
os.makedirs(OUT, exist_ok=True)

# Stronger, clearer palette
PAGE_BG     = "#f7f9fc"
WATER       = "#d9eaf7"
LAND_OTHER  = "#f4ede0"   # beige neighbours
INDIA_FILL  = "#bcd6f7"   # light but distinct blue for India
INDIA_EDGE  = "#1a3d80"
RIVER       = "#1e6fb8"
PEAK_GOLD   = "#ffc107"
PASS_RED    = "#d04967"
LABEL_BG    = "white"
LABEL_BORDER = "#1a3d80"
TEXT_FG     = "#0d1b2a"
GRID        = "#e2e8f1"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.facecolor": WATER,
    "figure.facecolor": PAGE_BG,
    "savefig.facecolor": PAGE_BG,
    "axes.edgecolor": "#cad4e2",
    "axes.linewidth": 0.6,
})

print("Loading Natural Earth data...")
countries = gpd.read_file("/tmp/ne_50m_admin_0_countries.shp")
rivers    = gpd.read_file("/tmp/ne_10m_rivers_lake_centerlines.shp")

india = countries[countries["ADMIN"] == "India"].copy()
NB = ["Pakistan", "China", "Nepal", "Bhutan", "Bangladesh",
      "Myanmar", "Afghanistan"]
neighbours = countries[countries["ADMIN"].isin(NB)].copy()


def basemap(ax, extent):
    minx, maxx, miny, maxy = extent
    # Other countries — pale grey-beige
    other = countries[(~countries["ADMIN"].isin(NB)) & (countries["ADMIN"] != "India")]
    other.plot(ax=ax, color="#efe6d5", edgecolor="#cbb893", linewidth=0.4)
    neighbours.plot(ax=ax, color=LAND_OTHER, edgecolor="#c1a974", linewidth=0.6)
    india.plot(ax=ax, color=INDIA_FILL, edgecolor=INDIA_EDGE, linewidth=1.5)
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(int(minx), int(maxx)+1, 4))
    ax.set_yticks(np.arange(int(miny), int(maxy)+1, 2))
    ax.tick_params(labelsize=8, color="#cad4e2", labelcolor="#6b6b66")
    ax.grid(True, color=GRID, linewidth=0.4, alpha=0.6)
    for s in ax.spines.values():
        s.set_color("#cad4e2"); s.set_linewidth(0.6)


def title(ax, t, s=None):
    ax.set_title(t, fontsize=15, fontweight=700, color=INDIA_EDGE,
                 pad=14, loc="left")
    if s:
        ax.text(0, 1.02, s, transform=ax.transAxes,
                fontsize=10.5, color="#56657a", style="italic")


# Add country name annotations on the map
def label_country(ax, lon, lat, name, size=10, color="#9d8155"):
    ax.text(lon, lat, name, fontsize=size, color=color, ha="center",
            fontweight=600, style="italic", alpha=0.85)


# ====================== FIG 3.1 — Three parallel ranges (v3, redrawn cleanly) ======================
def fig_three_ranges():
    """Three stacked horizontal bands showing the three ranges N→S,
    each with a mountain silhouette inside its own band so labels never
    collide with the mountains."""
    fig, ax = plt.subplots(figsize=(15, 9), dpi=180)
    ax.set_facecolor(PAGE_BG)

    x = np.linspace(0, 10, 500)

    # 3 bands, top = Himadri, middle = Himachal, bottom = Shivalik
    bands = [
        # (y_base, y_top, fill, mountain_height_func, snow, title, line2, text_col)
        (6.8, 9.6, "#cfdce8",  lambda x: 1.6 + 0.4*np.sin(x*1.6) + 0.25*np.sin(x*3.5),
         True,
         "01 · HIMADRI · GREATER HIMALAYAS",
         "6,000 m +  ·  perennial snow  ·  Everest · Kanchenjunga · Nanda Devi",
         "#1a3d80"),
        (3.8, 6.6, "#7ea7e8",  lambda x: 1.2 + 0.35*np.sin(x*1.9 + 1) + 0.2*np.sin(x*4),
         False,
         "02 · HIMACHAL · LESSER HIMALAYAS",
         "3,700 – 4,500 m  ·  Pir Panjal · Dhauladhar · Mussoorie · hill stations",
         "#1a3d80"),
        (0.8, 3.6, "#3b78e7", lambda x: 0.8 + 0.25*np.sin(x*2.4 + 2),
         False,
         "03 · SHIVALIK · OUTER HIMALAYAS",
         "900 – 1,100 m  ·  youngest range  ·  Duns  ·  sediment-rich",
         "white"),
    ]

    for y_base, y_top, fill, ht_fn, snow, t1, t2, txt_col in bands:
        # Background band
        ax.axhspan(y_base, y_top, color=fill, alpha=0.18, zorder=0)
        # Mountain silhouette inside this band, with crests anchored to y_base
        crests = ht_fn(x) + y_base
        ax.fill_between(x, crests, y_base, color=fill, zorder=2)
        ax.plot(x, crests, color="#1a3d80", lw=1.4, zorder=3)
        if snow:
            for px in [1.6, 3.0, 4.5, 6.0, 7.4, 8.7]:
                xs = np.linspace(px-0.25, px+0.25, 24)
                ys = ht_fn(xs) + y_base
                ax.fill_between(xs, ys, y_top, color="white", alpha=0.9, zorder=4)
        # Title and subline — pinned to top of the band, well above any crest
        ax.text(0.25, y_top - 0.35, t1, fontsize=16, fontweight=900,
                color=txt_col, va="top")
        ax.text(0.25, y_top - 0.85, t2, fontsize=11, color=txt_col,
                va="top", alpha=0.95)

    # N → S indicator – placed inside the canvas, not at the edge
    ax.annotate("", xy=(10.2, 1.1), xytext=(10.2, 9.3),
                arrowprops=dict(arrowstyle="->", color="#56657a", lw=2.5))
    ax.text(10.55, 8.7, "N", fontsize=14, fontweight=900,
            color="#56657a", ha="left", va="center")
    ax.text(10.55, 1.7, "S", fontsize=14, fontweight=900,
            color="#56657a", ha="left", va="center")
    ax.text(10.55, 5.2, "north\n→\nsouth", fontsize=9, color="#6b6b66",
            ha="left", va="center", style="italic")

    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 10)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    ax.set_title("Himalayas · three parallel ranges",
                 fontsize=17, fontweight=800, color="#1a3d80",
                 pad=16, loc="left")
    ax.text(0, 1.025, "Schematic profile from north (Greater Himalayas) "
            "to south (Outer Himalayas) · each range is younger than the one north of it.",
            transform=ax.transAxes, fontsize=11, color="#56657a", style="italic")

    plt.tight_layout()
    p = f"{OUT}/fig-three-ranges.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PAGE_BG)
    plt.close()
    print("✓", p)


# ====================== FIG 3.2 — Four regional divisions (cleaner) ======================
def fig_regional_divisions():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=180)
    basemap(ax, (71, 99, 23, 39))

    # Vertical bands as background shading
    bands = [
        (72, 77,  "#fff4d6", "01 · PUNJAB",
         "560 km", "Indus → Sutlej", "Karakoram · Pir Panjal", "#8a6a00"),
        (77, 81,  "#fde7eb", "02 · KUMAON",
         "320 km", "Sutlej → Kali", "Nanda Devi 7,816 m", "#9a2c45"),
        (81, 88,  "#dcecf2", "03 · NEPAL",
         "800 km", "Kali → Tista",  "Everest 8,848.86 m", "#1e4a86"),
        (88, 98,  "#e6efd9", "04 · ASSAM",
         "750 km", "Tista → Brahmaputra", "Sikkim · Arunachal", "#1d6b40"),
    ]
    for lon1, lon2, color, name, length, span, hero, txt_col in bands:
        ax.axvspan(lon1, lon2, ymin=0.10, ymax=0.96, alpha=0.55,
                   color=color, zorder=1.5)
        midlon = (lon1 + lon2) / 2
        # Top label block — boxed for clarity
        ax.text(midlon, 38.4, name, ha="center", fontsize=15,
                fontweight=900, color=txt_col)
        ax.text(midlon, 37.85, length, ha="center", fontsize=10.5,
                color=txt_col, fontweight=700)
        ax.text(midlon, 37.45, span, ha="center", fontsize=9.5,
                color="#3a3a3a", style="italic")
        ax.text(midlon, 37.05, hero, ha="center", fontsize=9.5,
                color="#3a3a3a")

    # River markers at the dividing longitudes
    for lon, river_name in [(77, "Sutlej"), (81, "Kali"), (88, "Tista")]:
        ax.axvline(lon, ymin=0.05, ymax=0.65, color="#1a3d80",
                   linewidth=1.4, linestyle=(0,(4,3)), alpha=0.7)
        ax.text(lon, 23.6, f"  {river_name}  ", ha="center", fontsize=10,
                color=RIVER, fontweight=800,
                bbox=dict(boxstyle="round,pad=0.3", fc="white",
                          ec=RIVER, lw=1.2))

    # Country annotations
    for lo, la, n in [(73, 30, "PAKISTAN"), (87, 35, "CHINA"),
                      (85, 28, "NEPAL"), (90.5, 27.5, "BHUTAN"),
                      (90, 24, "BANGLADESH"), (95, 22.5, "MYANMAR")]:
        label_country(ax, lo, la, n)

    title(ax,
          "Himalayas · four regional divisions",
          "Sliced by three rivers — Sutlej, Kali, Tista — into Punjab → Kumaon → Nepal → Assam")
    plt.tight_layout()
    p = f"{OUT}/fig-regional-divisions.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PAGE_BG)
    plt.close()
    print("✓", p)


# ====================== FIG 3.3 — Major peaks (cleaner with side legend) ======================
def fig_peaks():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=180)
    basemap(ax, (71, 99, 25, 38))

    peaks = [
        # (key, name, height, lon, lat, side ['L'|'R'|'T'|'B'])
        ("01", "Mt. Everest",        "8,848.86 m", 86.925, 27.988, "B"),
        ("02", "K2 (Godwin Austen)", "8,611 m",    76.513, 35.881, "L"),
        ("03", "Kanchenjunga",       "8,586 m",    88.147, 27.702, "R"),
        ("04", "Nanga Parbat",       "8,126 m",    74.589, 35.237, "L"),
        ("05", "Nanda Devi",         "7,816 m",    79.970, 30.376, "T"),
        ("06", "Kamet",              "7,756 m",    79.594, 30.920, "L"),
        ("07", "Saser Kangri",       "7,672 m",    77.752, 34.870, "T"),
        ("08", "Namcha Barwa",       "7,782 m",    95.060, 29.620, "T"),
    ]

    # Plot peak markers (numbered gold badges)
    for key, name, ht, lon, lat, side in peaks:
        ax.scatter([lon], [lat], s=520, color=PEAK_GOLD,
                   edgecolor=INDIA_EDGE, linewidth=2.2, zorder=8)
        ax.text(lon, lat, key, fontsize=10, fontweight=900,
                color=INDIA_EDGE, ha="center", va="center", zorder=9)

    # Country annotations
    for lo, la, n in [(73, 30, "PAKISTAN"), (88, 36, "CHINA"),
                      (85, 28, "NEPAL"), (90.5, 27.4, "BHUTAN")]:
        label_country(ax, lo, la, n)

    # Side legend panel (right side, inside the figure)
    legend_x, legend_y0 = 100.2, 37.5
    ax.text(legend_x, legend_y0, "PEAK · HEIGHT · WHERE",
            fontsize=11, fontweight=800, color=INDIA_EDGE,
            ha="left", va="top",
            bbox=dict(boxstyle="round,pad=0.4", fc="white",
                      ec=INDIA_EDGE, lw=1.4))
    where_map = {
        "Mt. Everest":       "Nepal – China border",
        "K2 (Godwin Austen)":"PoK · Karakoram",
        "Kanchenjunga":      "Sikkim – Nepal",
        "Nanga Parbat":      "Western Himalayas (PoK)",
        "Nanda Devi":        "Uttarakhand · Garhwal",
        "Kamet":             "Uttarakhand",
        "Saser Kangri":      "Ladakh · Karakoram",
        "Namcha Barwa":      "Tibet (Brahmaputra bend)",
    }
    for i, (key, name, ht, *_rest) in enumerate(peaks):
        y = legend_y0 - 1.1 - i*1.35
        # number badge
        ax.scatter([legend_x+0.35], [y], s=320, color=PEAK_GOLD,
                   edgecolor=INDIA_EDGE, linewidth=1.8, zorder=8)
        ax.text(legend_x+0.35, y, key, fontsize=9, fontweight=900,
                color=INDIA_EDGE, ha="center", va="center", zorder=9)
        ax.text(legend_x+1.0, y+0.18, name, fontsize=10.5,
                fontweight=700, color=TEXT_FG, va="center")
        ax.text(legend_x+1.0, y-0.15, f"{ht}  ·  {where_map[name]}",
                fontsize=9, color="#56657a", va="center")

    # Expand x-limit to fit the legend
    ax.set_xlim(71, 112)
    title(ax,
          "Himalayas · major peaks",
          "Numbered gold badges show real GPS positions. Full names in side legend.")
    plt.tight_layout()
    p = f"{OUT}/fig-peaks.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PAGE_BG)
    plt.close()
    print("✓", p)


# ====================== FIG 3.4 — Important passes (cleaner with legend) ======================
def fig_passes():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=180)
    basemap(ax, (71, 99, 26, 38))

    passes = [
        ("01", "Karakoram Pass",  77.82,  35.51,  "Karakoram · Ladakh → Xinjiang"),
        ("02", "Khardung La",     77.605, 34.279, "Ladakh · Leh → Nubra"),
        ("03", "Zoji La",         75.475, 34.281, "Zanskar · Srinagar → Leh"),
        ("04", "Banihal Pass",    75.183, 33.490, "Pir Panjal · Jammu → Srinagar"),
        ("05", "Bara-lacha La",   77.426, 32.762, "Zanskar · Manali → Leh"),
        ("06", "Rohtang La",      77.246, 32.372, "Pir Panjal · Manali → Lahaul"),
        ("07", "Shipki La",       78.748, 31.819, "Zanskar · HP → Tibet"),
        ("08", "Mana Pass",       79.398, 31.082, "Garhwal · India → Tibet"),
        ("09", "Niti Pass",       79.973, 30.770, "Kumaon · Uttarakhand → Tibet"),
        ("10", "Lipulekh Pass",   80.838, 30.244, "Kumaon · Kailash-Mansarovar route"),
        ("11", "Nathu La",        88.832, 27.388, "Sikkim → Tibet · old Silk Road"),
        ("12", "Jelep La",        88.701, 27.382, "Sikkim → Tibet"),
        ("13", "Bom Di La",       92.412, 27.262, "Arunachal · Tezpur → Tawang"),
    ]

    for key, name, lon, lat, _ in passes:
        ax.scatter([lon], [lat], s=400, color="#fde7eb",
                   edgecolor=PASS_RED, linewidth=2, zorder=8)
        ax.text(lon, lat, key, fontsize=9, fontweight=900,
                color=PASS_RED, ha="center", va="center", zorder=9)

    # Country annotations
    for lo, la, n in [(73, 30, "PAKISTAN"), (88, 36, "CHINA"),
                      (85, 28, "NEPAL"), (90.5, 27.4, "BHUTAN")]:
        label_country(ax, lo, la, n)

    # Side legend
    legend_x, legend_y0 = 100.2, 37.5
    ax.text(legend_x, legend_y0, "PASS · LOCATION · ROUTE",
            fontsize=11, fontweight=800, color=PASS_RED,
            ha="left", va="top",
            bbox=dict(boxstyle="round,pad=0.4", fc="white",
                      ec=PASS_RED, lw=1.4))
    for i, (key, name, _, _, route) in enumerate(passes):
        y = legend_y0 - 0.9 - i*0.85
        ax.scatter([legend_x+0.35], [y], s=240, color="#fde7eb",
                   edgecolor=PASS_RED, linewidth=1.6, zorder=8)
        ax.text(legend_x+0.35, y, key, fontsize=8, fontweight=900,
                color=PASS_RED, ha="center", va="center", zorder=9)
        ax.text(legend_x+1.0, y+0.1, name, fontsize=10,
                fontweight=700, color=TEXT_FG, va="center")
        ax.text(legend_x+1.0, y-0.15, route, fontsize=8.5,
                color="#56657a", va="center")

    ax.set_xlim(71, 116)
    title(ax,
          "Himalayas · important passes",
          "Strategic gaps — trade, pilgrimage, military. Numbered on the map; named in the legend.")
    plt.tight_layout()
    p = f"{OUT}/fig-passes.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PAGE_BG)
    plt.close()
    print("✓", p)


if __name__ == "__main__":
    fig_three_ranges()
    fig_regional_divisions()
    fig_peaks()
    fig_passes()
    print("\nDone.")
