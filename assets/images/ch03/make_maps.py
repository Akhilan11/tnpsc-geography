"""
Ch 3 maps — v3 with proper India context.

Fixes:
- Show FULL India (not just the Himalayan strip) — so viewers can
  orient themselves
- Draw state boundaries so peaks/passes sit clearly inside states
- State name labels on the relevant Himalayan states
- Strong colour contrast between India, neighbours and ocean
"""
import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUT = "/Users/aniket/Documents/TNPSC-Geography/assets/images/ch03"
os.makedirs(OUT, exist_ok=True)

PAGE_BG     = "#f7f9fc"
WATER       = "#cfe3f7"      # bluer sea
LAND_OTHER  = "#f0e6cf"      # beige neighbours
INDIA_FILL  = "#fff8e7"      # pale warm cream for India (so highlights pop)
INDIA_EDGE  = "#1a3d80"
STATE_EDGE  = "#9aaecb"
HIMALAYA_BG = "#dbe9fb"      # light blue for Himalayan strip
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
states    = gpd.read_file("/tmp/ne_10m_admin_1_states_provinces.shp")
rivers    = gpd.read_file("/tmp/ne_10m_rivers_lake_centerlines.shp")

india = countries[countries["ADMIN"] == "India"].copy()
india_states = states[states["admin"] == "India"].copy()

NB = ["Pakistan", "China", "Nepal", "Bhutan", "Bangladesh",
      "Myanmar", "Afghanistan"]
neighbours = countries[countries["ADMIN"].isin(NB)].copy()

HIMALAYAN_STATES = ["Jammu and Kashmir", "Ladakh", "Himachal Pradesh",
                    "Uttarakhand", "Sikkim", "Arunachal Pradesh",
                    "Assam", "West Bengal"]


def basemap(ax, extent, show_states=True, highlight_himalayan=True):
    minx, maxx, miny, maxy = extent
    # Other countries
    other = countries[(~countries["ADMIN"].isin(NB)) & (countries["ADMIN"] != "India")]
    other.plot(ax=ax, color="#e8dcc4", edgecolor="#b9a474", linewidth=0.4)
    neighbours.plot(ax=ax, color=LAND_OTHER, edgecolor="#a48e58", linewidth=0.7)
    # India base
    india.plot(ax=ax, color=INDIA_FILL, edgecolor=INDIA_EDGE, linewidth=1.6)
    if show_states:
        # State boundaries inside India
        india_states.plot(ax=ax, color="none", edgecolor=STATE_EDGE,
                          linewidth=0.6, alpha=0.9)
    if highlight_himalayan:
        him_states = india_states[india_states["name"].isin(HIMALAYAN_STATES)]
        him_states.plot(ax=ax, color=HIMALAYA_BG, edgecolor=INDIA_EDGE,
                        linewidth=1.0, alpha=0.85, zorder=2)

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
    ax.set_title(t, fontsize=16, fontweight=800, color=INDIA_EDGE,
                 pad=14, loc="left")
    if s:
        ax.text(0, 1.02, s, transform=ax.transAxes,
                fontsize=11, color="#56657a", style="italic")


def state_labels(ax, names, color="#1a3d80", size=8.5):
    for n in names:
        rows = india_states[india_states["name"] == n]
        if len(rows) == 0: continue
        c = rows.iloc[0].geometry.representative_point()
        ax.text(c.x, c.y, n.upper(), fontsize=size, fontweight=700,
                color=color, ha="center", va="center", alpha=0.85,
                bbox=dict(boxstyle="round,pad=0.18", fc="white",
                          ec="none", alpha=0.65))


def country_labels(ax, items, size=10):
    for lo, la, n in items:
        ax.text(lo, la, n, fontsize=size, color="#7a5a1c", ha="center",
                fontweight=700, style="italic", alpha=0.85)


# ====================== FIG 3.1 — Three parallel ranges (re-use v2, it was fine) ======================
def fig_three_ranges():
    fig, ax = plt.subplots(figsize=(15, 9), dpi=180)
    ax.set_facecolor(PAGE_BG)
    x = np.linspace(0, 10, 500)
    bands = [
        (6.8, 9.6, "#cfdce8",
         lambda x: 1.6 + 0.4*np.sin(x*1.6) + 0.25*np.sin(x*3.5), True,
         "01 · HIMADRI · GREATER HIMALAYAS",
         "6,000 m +  ·  perennial snow  ·  Everest · Kanchenjunga · Nanda Devi",
         "#1a3d80"),
        (3.8, 6.6, "#7ea7e8",
         lambda x: 1.2 + 0.35*np.sin(x*1.9 + 1) + 0.2*np.sin(x*4), False,
         "02 · HIMACHAL · LESSER HIMALAYAS",
         "3,700 – 4,500 m  ·  Pir Panjal · Dhauladhar · Mussoorie · hill stations",
         "#1a3d80"),
        (0.8, 3.6, "#3b78e7",
         lambda x: 0.8 + 0.25*np.sin(x*2.4 + 2), False,
         "03 · SHIVALIK · OUTER HIMALAYAS",
         "900 – 1,100 m  ·  youngest range  ·  Duns  ·  sediment-rich",
         "white"),
    ]
    for y_base, y_top, fill, ht_fn, snow, t1, t2, txt_col in bands:
        ax.axhspan(y_base, y_top, color=fill, alpha=0.18, zorder=0)
        crests = ht_fn(x) + y_base
        ax.fill_between(x, crests, y_base, color=fill, zorder=2)
        ax.plot(x, crests, color="#1a3d80", lw=1.4, zorder=3)
        if snow:
            for px in [1.6, 3.0, 4.5, 6.0, 7.4, 8.7]:
                xs = np.linspace(px-0.25, px+0.25, 24)
                ys = ht_fn(xs) + y_base
                ax.fill_between(xs, ys, y_top, color="white", alpha=0.9, zorder=4)
        ax.text(0.25, y_top - 0.35, t1, fontsize=16, fontweight=900,
                color=txt_col, va="top")
        ax.text(0.25, y_top - 0.85, t2, fontsize=11, color=txt_col,
                va="top", alpha=0.95)
    ax.annotate("", xy=(10.2, 1.1), xytext=(10.2, 9.3),
                arrowprops=dict(arrowstyle="->", color="#56657a", lw=2.5))
    ax.text(10.55, 8.7, "N", fontsize=14, fontweight=900, color="#56657a")
    ax.text(10.55, 1.7, "S", fontsize=14, fontweight=900, color="#56657a")
    ax.text(10.55, 5.2, "north\n→\nsouth", fontsize=9, color="#6b6b66",
            ha="left", va="center", style="italic")
    ax.set_xlim(0, 11.5); ax.set_ylim(0, 10)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title("Himalayas · three parallel ranges",
                 fontsize=17, fontweight=800, color="#1a3d80", pad=16, loc="left")
    ax.text(0, 1.025, "Schematic profile · north (Greater Himalayas) → south (Outer Himalayas).",
            transform=ax.transAxes, fontsize=11, color="#56657a", style="italic")
    plt.tight_layout()
    p = f"{OUT}/fig-three-ranges.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PAGE_BG)
    plt.close()
    print("✓", p)


# ====================== FIG 3.2 — Regional divisions on FULL INDIA map ======================
def fig_regional_divisions():
    fig, ax = plt.subplots(figsize=(16, 13), dpi=170)
    # Full India view so users can orient
    basemap(ax, (66, 99, 6, 38), show_states=True, highlight_himalayan=False)

    # Highlight ONLY the four Himalayan bands inside the Himalayan-state strip
    # We shade the whole vertical longitude band, but bounded by Himalayan latitudes
    bands = [
        (72, 77,  "#fff4d6", "01 · PUNJAB",  "560 km", "Indus → Sutlej", "#8a6a00"),
        (77, 81,  "#fde7eb", "02 · KUMAON",  "320 km", "Sutlej → Kali",  "#9a2c45"),
        (81, 88,  "#dcecf2", "03 · NEPAL",   "800 km", "Kali → Tista",   "#1e4a86"),
        (88, 97,  "#e6efd9", "04 · ASSAM",   "750 km", "Tista → Brahmaputra", "#1d6b40"),
    ]
    # Lower-band labels (length + river span) just below the title
    # Place the band shading only across the Himalayan latitudes
    HIM_LAT_LO, HIM_LAT_HI = 26, 37
    for lon1, lon2, color, name, length, span, col in bands:
        # band rectangle in the Himalaya latitudes
        rect = mpatches.Rectangle((lon1, HIM_LAT_LO), lon2-lon1,
                                  HIM_LAT_HI-HIM_LAT_LO,
                                  facecolor=color, alpha=0.55,
                                  edgecolor="none", zorder=1.5)
        ax.add_patch(rect)
        midlon = (lon1 + lon2) / 2
        # Title above the strip (above 37 N)
        ax.text(midlon, 37.6, name, ha="center", fontsize=14, fontweight=900, color=col)
        ax.text(midlon, 37.2, length, ha="center", fontsize=10, fontweight=700, color=col)
        ax.text(midlon, 36.85, span, ha="center", fontsize=9.5, color="#3a3a3a", style="italic")

    # Dividing-river vertical guides only inside Himalayan latitudes
    for lon, river_name in [(77, "Sutlej"), (81, "Kali"), (88, "Tista")]:
        ax.plot([lon, lon], [HIM_LAT_LO, HIM_LAT_HI], color="#1a3d80",
                lw=1.4, ls=(0,(4,3)), alpha=0.7, zorder=4)
        ax.text(lon, HIM_LAT_LO - 0.5, river_name, ha="center", fontsize=10,
                color="#1e6fb8", fontweight=800,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#1e6fb8", lw=1.2))

    state_labels(ax,
                 ["Jammu and Kashmir", "Ladakh", "Himachal Pradesh",
                  "Uttarakhand", "Sikkim", "Arunachal Pradesh"],
                 color="#1a3d80", size=8)
    country_labels(ax, [
        (71, 28, "PAKISTAN"), (88, 36, "CHINA"), (84, 28.5, "NEPAL"),
        (90.5, 27.5, "BHUTAN"), (90, 23.7, "BANGLADESH"), (95, 22, "MYANMAR")
    ])

    title(ax,
          "Himalayas · four regional divisions",
          "Punjab → Kumaon → Nepal → Assam · sliced by the rivers Sutlej, Kali, Tista")
    plt.tight_layout()
    p = f"{OUT}/fig-regional-divisions.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PAGE_BG)
    plt.close()
    print("✓", p)


# ====================== FIG 3.3 — Major peaks on FULL Himalayan India map with state lines ======================
def fig_peaks():
    fig, ax = plt.subplots(figsize=(17, 10), dpi=180)
    basemap(ax, (71, 99, 24, 38), show_states=True, highlight_himalayan=True)

    peaks = [
        ("01", "Mt. Everest",        "8,848.86 m", 86.925, 27.988, "Nepal – China border"),
        ("02", "K2 (Godwin Austen)", "8,611 m",    76.513, 35.881, "PoK · Karakoram"),
        ("03", "Kanchenjunga",       "8,586 m",    88.147, 27.702, "Sikkim – Nepal"),
        ("04", "Nanga Parbat",       "8,126 m",    74.589, 35.237, "Western Himalayas (PoK)"),
        ("05", "Nanda Devi",         "7,816 m",    79.970, 30.376, "Uttarakhand · Garhwal"),
        ("06", "Kamet",              "7,756 m",    79.594, 30.920, "Uttarakhand"),
        ("07", "Saser Kangri",       "7,672 m",    77.752, 34.870, "Ladakh · Karakoram"),
        ("08", "Namcha Barwa",       "7,782 m",    95.060, 29.620, "Tibet (Brahmaputra bend)"),
    ]
    for key, name, ht, lon, lat, _ in peaks:
        ax.scatter([lon], [lat], s=540, color="#ffc107",
                   edgecolor=INDIA_EDGE, linewidth=2.4, zorder=8)
        ax.text(lon, lat, key, fontsize=10, fontweight=900,
                color=INDIA_EDGE, ha="center", va="center", zorder=9)

    state_labels(ax,
                 ["Ladakh", "Jammu and Kashmir", "Himachal Pradesh",
                  "Uttarakhand", "Sikkim", "Arunachal Pradesh"],
                 color="#1a3d80", size=8.5)
    country_labels(ax, [
        (72, 30, "PAKISTAN"), (88, 36, "CHINA"), (85, 28, "NEPAL"),
        (90.5, 27.4, "BHUTAN")
    ])

    # Side legend
    legend_x, legend_y0 = 100.5, 37.5
    ax.text(legend_x, legend_y0, "PEAK · HEIGHT · WHERE",
            fontsize=11, fontweight=800, color=INDIA_EDGE,
            ha="left", va="top",
            bbox=dict(boxstyle="round,pad=0.4", fc="white",
                      ec=INDIA_EDGE, lw=1.4))
    for i, (key, name, ht, _, _, where) in enumerate(peaks):
        y = legend_y0 - 1.1 - i * 1.45
        ax.scatter([legend_x + 0.35], [y], s=320, color="#ffc107",
                   edgecolor=INDIA_EDGE, linewidth=1.8, zorder=8)
        ax.text(legend_x + 0.35, y, key, fontsize=9, fontweight=900,
                color=INDIA_EDGE, ha="center", va="center", zorder=9)
        ax.text(legend_x + 1.0, y + 0.2, name, fontsize=10.5,
                fontweight=700, color=TEXT_FG, va="center")
        ax.text(legend_x + 1.0, y - 0.18, f"{ht}  ·  {where}",
                fontsize=9, color="#56657a", va="center")

    ax.set_xlim(71, 113)
    title(ax,
          "Himalayas · major peaks",
          "Numbered gold badges show real GPS positions on Indian states · names in side legend.")
    plt.tight_layout()
    p = f"{OUT}/fig-peaks.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PAGE_BG)
    plt.close()
    print("✓", p)


# ====================== FIG 3.4 — Important passes ======================
def fig_passes():
    fig, ax = plt.subplots(figsize=(17, 10), dpi=180)
    basemap(ax, (71, 99, 25, 38), show_states=True, highlight_himalayan=True)

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
        ax.scatter([lon], [lat], s=380, color="#fde7eb",
                   edgecolor="#d04967", linewidth=2, zorder=8)
        ax.text(lon, lat, key, fontsize=9, fontweight=900,
                color="#d04967", ha="center", va="center", zorder=9)

    state_labels(ax,
                 ["Ladakh", "Jammu and Kashmir", "Himachal Pradesh",
                  "Uttarakhand", "Sikkim", "Arunachal Pradesh"],
                 color="#1a3d80", size=8.5)
    country_labels(ax, [
        (72, 30, "PAKISTAN"), (88, 36, "CHINA"), (85, 28, "NEPAL"),
        (90.5, 27.4, "BHUTAN")
    ])

    legend_x, legend_y0 = 100.5, 37.5
    ax.text(legend_x, legend_y0, "PASS · LOCATION · ROUTE",
            fontsize=11, fontweight=800, color="#d04967",
            ha="left", va="top",
            bbox=dict(boxstyle="round,pad=0.4", fc="white",
                      ec="#d04967", lw=1.4))
    for i, (key, name, _, _, route) in enumerate(passes):
        y = legend_y0 - 0.9 - i * 0.85
        ax.scatter([legend_x + 0.35], [y], s=240, color="#fde7eb",
                   edgecolor="#d04967", linewidth=1.6, zorder=8)
        ax.text(legend_x + 0.35, y, key, fontsize=8, fontweight=900,
                color="#d04967", ha="center", va="center", zorder=9)
        ax.text(legend_x + 1.0, y + 0.1, name, fontsize=10,
                fontweight=700, color=TEXT_FG, va="center")
        ax.text(legend_x + 1.0, y - 0.15, route, fontsize=8.5,
                color="#56657a", va="center")

    ax.set_xlim(71, 116)
    title(ax,
          "Himalayas · important passes",
          "Strategic gaps marked on real state boundaries · routes in side legend")
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
