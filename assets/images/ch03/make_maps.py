"""
Generate accurate maps for Chapter 3 — The Himalayas.

Source data:
  - Natural Earth 1:50m & 1:10m public domain
  - Peak / pass coordinates from open geographic references

Produces 4 PNGs into /Users/aniket/Documents/TNPSC-Geography/assets/images/ch03/
"""
import os
import geopandas as gpd
import matplotlib.pyplot as plt

OUT = "/Users/aniket/Documents/TNPSC-Geography/assets/images/ch03"
os.makedirs(OUT, exist_ok=True)

PLT_BG = "#f7f9fc"
LAND_FILL = "#eef3fb"
NEIGHBOUR_FILL = "#f3f3f0"
INDIA_FILL = "#d5e4fc"
INDIA_EDGE = "#1a3d80"
RIVER_BLUE = "#3b78e7"
PEAK_GOLD = "#ffd400"
ACCENT_RED = "#d04967"
TEXT_FG = "#0d1b2a"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.facecolor": PLT_BG,
    "figure.facecolor": PLT_BG,
    "savefig.facecolor": PLT_BG,
    "axes.edgecolor": "#cad4e2",
    "axes.linewidth": 0.6,
})

print("Loading Natural Earth data...")
countries = gpd.read_file("/tmp/ne_50m_admin_0_countries.shp")
states = gpd.read_file("/tmp/ne_10m_admin_1_states_provinces.shp")
rivers = gpd.read_file("/tmp/ne_10m_rivers_lake_centerlines.shp")

india = countries[countries["ADMIN"] == "India"].copy()
india_states = states[states["admin"] == "India"].copy()

NB = ["Pakistan", "China", "Nepal", "Bhutan", "Bangladesh", "Myanmar", "Afghanistan"]
neighbours = countries[countries["ADMIN"].isin(NB)].copy()

# Himalaya viewing extent (longitude, latitude)
HIM_EXTENT = (72, 98, 24, 38)


def style(ax, title=None, subtitle=None, extent=HIM_EXTENT):
    minx, maxx, miny, maxy = extent
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_aspect("equal")
    ax.set_xticks(range(int(minx), int(maxx)+1, 4))
    ax.set_yticks(range(int(miny), int(maxy)+1, 2))
    ax.tick_params(axis="both", labelsize=7, color="#cad4e2",
                   labelcolor="#6b6b66")
    ax.grid(True, color="#e2e8f1", linewidth=0.4, alpha=0.7)
    for s in ax.spines.values():
        s.set_color("#cad4e2"); s.set_linewidth(0.6)
    if title:
        ax.set_title(title, fontsize=12, fontweight=700,
                     color=INDIA_EDGE, pad=12, loc="left")
    if subtitle:
        ax.text(0, 1.018, subtitle, transform=ax.transAxes,
                fontsize=9, color="#56657a", style="italic")


def label(ax, lon, lat, text, color=TEXT_FG, **kw):
    ax.scatter([lon], [lat], s=70, color=PEAK_GOLD, edgecolor=INDIA_EDGE,
               linewidth=1.5, zorder=6)
    ax.annotate(text, xy=(lon, lat),
                xytext=(lon + kw.get("dx", 0.4), lat + kw.get("dy", 0.4)),
                fontsize=8, fontweight=600, color=color,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor=INDIA_EDGE, lw=0.8, alpha=0.95),
                arrowprops=dict(arrowstyle="-", color=INDIA_EDGE, lw=0.5))


# ====================== FIG 3.1 — Three parallel ranges (schematic profile) ======================
def fig_three_ranges():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=160)
    # Profile schematic — silhouettes of three ranges, north→south
    import numpy as np
    x = np.linspace(0, 10, 500)

    # Himadri (back) — tallest, snow-capped
    himadri_y = 8.5 + 0.6 * np.sin(x*1.4) + 0.4 * np.sin(x*3.2)
    ax.fill_between(x, himadri_y, 0, color="#cfdce8", alpha=0.95, zorder=1)
    ax.plot(x, himadri_y, color="#1a3d80", linewidth=1.2, zorder=2)
    # Snow caps
    for px in [2, 3.5, 5.2, 6.8, 8.3]:
        ax.fill_between(np.linspace(px-0.3, px+0.3, 30),
                        8.5 + 0.6*np.sin(np.linspace(px-0.3, px+0.3, 30)*1.4) +
                              0.4*np.sin(np.linspace(px-0.3, px+0.3, 30)*3.2),
                        9.5, color="white", zorder=3)

    # Himachal (middle)
    himachal_y = 6.0 + 0.5 * np.sin(x*1.8 + 1) + 0.3 * np.sin(x*4)
    ax.fill_between(x, himachal_y, 0, color="#9fb6d4", alpha=0.95, zorder=4)
    ax.plot(x, himachal_y, color="#1a3d80", linewidth=1.2, zorder=5)

    # Shivalik (front)
    shivalik_y = 3.0 + 0.4 * np.sin(x*2.2 + 2)
    ax.fill_between(x, shivalik_y, 0, color="#5e92ee", alpha=0.95, zorder=6)
    ax.plot(x, shivalik_y, color="#1a3d80", linewidth=1.2, zorder=7)

    # Labels with elevation ranges
    ax.text(5, 9.4, "HIMADRI · GREATER HIMALAYAS", ha="center",
            fontsize=12, fontweight=800, color="#1a3d80")
    ax.text(5, 9.05, "6,000 m+ · perennial snow · Everest · Kanchenjunga",
            ha="center", fontsize=9, color="#56657a")

    ax.text(5, 6.8, "HIMACHAL · LESSER HIMALAYAS", ha="center",
            fontsize=12, fontweight=800, color="#1a3d80")
    ax.text(5, 6.5, "3,700 – 4,500 m · hill stations · Pir Panjal · Dhauladhar",
            ha="center", fontsize=9, color="#56657a")

    ax.text(5, 3.6, "SHIVALIK · OUTER HIMALAYAS", ha="center",
            fontsize=12, fontweight=800, color="#1a3d80")
    ax.text(5, 3.3, "900 – 1,100 m · youngest · sediment-rich · Duns",
            ha="center", fontsize=9, color="#56657a")

    # N → S arrow
    ax.annotate("", xy=(9.5, 0.5), xytext=(9.5, 9.5),
                arrowprops=dict(arrowstyle="->", color="#56657a", lw=1.5))
    ax.text(9.65, 5, "S\n←\nN", fontsize=10, fontweight=700,
            color="#56657a", va="center")

    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 10.5)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    ax.set_title("Himalayas · three parallel ranges (schematic profile, north to south)",
                 fontsize=13, fontweight=700, color="#1a3d80",
                 pad=14, loc="left")

    plt.tight_layout()
    p = f"{OUT}/fig-three-ranges.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PLT_BG)
    plt.close()
    print("✓", p)


# ====================== FIG 3.2 — Four regional divisions ======================
def fig_regional_divisions():
    fig, ax = plt.subplots(figsize=(13, 7), dpi=160)
    other = countries[(~countries["ADMIN"].isin(NB)) & (countries["ADMIN"] != "India")]
    other.plot(ax=ax, color=NEIGHBOUR_FILL, edgecolor="#d8d6cc", linewidth=0.3)
    neighbours.plot(ax=ax, color="#f0e6cf", edgecolor="#bdbab0", linewidth=0.5)
    india.plot(ax=ax, color=INDIA_FILL, edgecolor=INDIA_EDGE, linewidth=1.2)

    # Vertical bands shading the four regional divisions
    # Punjab Himalayas: Indus to Sutlej, roughly 72-77 E
    # Kumaon: Sutlej to Kali, 77-81 E
    # Nepal: Kali to Tista, 81-88 E
    # Assam: Tista to Brahmaputra, 88-97 E
    bands = [
        (72, 77, "#fff4d6", "PUNJAB HIMALAYAS", "560 km · Indus→Sutlej · Karakoram, Pir Panjal"),
        (77, 81, "#fde7eb", "KUMAON HIMALAYAS", "320 km · Sutlej→Kali · Nanda Devi 7,816 m"),
        (81, 88, "#e6efd9", "NEPAL HIMALAYAS", "800 km · Kali→Tista · Everest 8,848.86 m"),
        (88, 97, "#dcecf2", "ASSAM HIMALAYAS", "750 km · Tista→Brahmaputra · Sikkim, Arunachal"),
    ]
    for lon1, lon2, color, name, desc in bands:
        ax.axvspan(lon1, lon2, ymin=0.55, ymax=0.95, alpha=0.55, color=color, zorder=1)
        midlon = (lon1 + lon2) / 2
        # Label at top
        ax.text(midlon, 37.5, name, ha="center", fontsize=10,
                fontweight=800, color="#1a3d80")
        ax.text(midlon, 37.0, desc, ha="center", fontsize=7.5,
                color="#56657a", style="italic", wrap=True)

    # Draw the four boundary rivers
    boundary_rivers = ["Indus", "Sutlej", "Kali", "Tista", "Brahmaputra"]
    for r in boundary_rivers:
        seg = rivers[rivers["name"].fillna("").str.contains(r, case=False, na=False)]
        if len(seg) > 0:
            seg.plot(ax=ax, color=RIVER_BLUE, linewidth=1.2, alpha=0.9, zorder=3)

    # Boundary longitude markers
    for lon, river_label in [(77, "Sutlej"), (81, "Kali"), (88, "Tista")]:
        ax.axvline(lon, ymin=0.05, ymax=0.55, color="#1a3d80",
                   linewidth=0.8, linestyle=(0,(3,2)), alpha=0.4)
        ax.text(lon, 24.5, river_label, ha="center", fontsize=8,
                color=RIVER_BLUE, fontweight=700,
                bbox=dict(boxstyle="round,pad=0.2", fc="white",
                          ec=RIVER_BLUE, lw=0.5))

    style(ax,
          title="Himalayas · four regional divisions, west to east",
          subtitle="Punjab → Kumaon → Nepal → Assam (divided by the rivers Sutlej, Kali, Tista)")
    plt.tight_layout()
    p = f"{OUT}/fig-regional-divisions.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PLT_BG)
    plt.close()
    print("✓", p)


# ====================== FIG 3.3 — Major peaks ======================
def fig_peaks():
    fig, ax = plt.subplots(figsize=(13, 7), dpi=160)
    other = countries[(~countries["ADMIN"].isin(NB)) & (countries["ADMIN"] != "India")]
    other.plot(ax=ax, color=NEIGHBOUR_FILL, edgecolor="#d8d6cc", linewidth=0.3)
    neighbours.plot(ax=ax, color="#f0e6cf", edgecolor="#bdbab0", linewidth=0.5)
    india.plot(ax=ax, color=INDIA_FILL, edgecolor=INDIA_EDGE, linewidth=1.2)

    # Major peaks — verified coordinates
    peaks = [
        ("Mt. Everest", "8,848.86 m", 86.925, 27.988, (1.5, 0.7)),
        ("K2 (Godwin Austen)", "8,611 m", 76.513, 35.881, (-3, 0.5)),
        ("Kanchenjunga", "8,586 m", 88.147, 27.702, (1.5, -0.6)),
        ("Nanga Parbat", "8,126 m", 74.589, 35.237, (-2.5, -0.8)),
        ("Nanda Devi", "7,816 m", 79.970, 30.376, (1.2, 0.7)),
        ("Namcha Barwa", "7,782 m", 95.060, 29.620, (1.2, 0.7)),
        ("Saser Kangri", "7,672 m", 77.752, 34.870, (-2.7, 0.5)),
        ("Kamet", "7,756 m", 79.594, 30.920, (1.2, 0.6)),
    ]
    for name, height, lon, lat, off in peaks:
        ax.scatter([lon], [lat], s=200, color=PEAK_GOLD,
                   edgecolor="#1a3d80", linewidth=2, zorder=6)
        # small triangle marker
        ax.scatter([lon], [lat], marker="^", s=40, color="#1a3d80", zorder=7)
        ax.annotate(f"{name}\n{height}",
                    xy=(lon, lat),
                    xytext=(lon + off[0], lat + off[1]),
                    fontsize=8, fontweight=600, color=TEXT_FG,
                    bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                              edgecolor="#1a3d80", lw=1, alpha=0.95),
                    arrowprops=dict(arrowstyle="-", color="#1a3d80", lw=0.7),
                    ha="center")

    style(ax,
          title="Himalayas · major peaks",
          subtitle="Real coordinates plotted. Everest (Nepal–China), Kanchenjunga (Sikkim), K2 (PoK).",
          extent=(72, 98, 25, 38))
    plt.tight_layout()
    p = f"{OUT}/fig-peaks.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PLT_BG)
    plt.close()
    print("✓", p)


# ====================== FIG 3.4 — Important passes ======================
def fig_passes():
    fig, ax = plt.subplots(figsize=(13, 7), dpi=160)
    other = countries[(~countries["ADMIN"].isin(NB)) & (countries["ADMIN"] != "India")]
    other.plot(ax=ax, color=NEIGHBOUR_FILL, edgecolor="#d8d6cc", linewidth=0.3)
    neighbours.plot(ax=ax, color="#f0e6cf", edgecolor="#bdbab0", linewidth=0.5)
    india.plot(ax=ax, color=INDIA_FILL, edgecolor=INDIA_EDGE, linewidth=1.2)

    passes = [
        ("Karakoram Pass", 77.82, 35.51, (-3, 0.6)),
        ("Khardung La", 77.605, 34.279, (1.5, -0.4)),
        ("Zoji La", 75.475, 34.281, (-2.7, 0.7)),
        ("Banihal Pass", 75.183, 33.490, (-2.5, -0.7)),
        ("Rohtang La", 77.246, 32.372, (1.5, -0.4)),
        ("Shipki La", 78.748, 31.819, (1.5, 0.6)),
        ("Bara-lacha La", 77.426, 32.762, (-2.6, 0.7)),
        ("Lipulekh Pass", 80.838, 30.244, (1.4, -0.6)),
        ("Niti Pass", 79.973, 30.770, (-2.3, 0.5)),
        ("Mana Pass", 79.398, 31.082, (-2.0, 0.7)),
        ("Nathu La", 88.832, 27.388, (1.3, -0.6)),
        ("Jelep La", 88.701, 27.382, (-2.2, 0.5)),
        ("Bom Di La", 92.412, 27.262, (1.4, 0.5)),
    ]
    for name, lon, lat, off in passes:
        ax.scatter([lon], [lat], s=110, color="#fde7eb",
                   edgecolor=ACCENT_RED, linewidth=1.6, zorder=6)
        ax.scatter([lon], [lat], marker="x", s=30, color=ACCENT_RED, zorder=7)
        ax.annotate(name, xy=(lon, lat),
                    xytext=(lon + off[0], lat + off[1]),
                    fontsize=7.5, fontweight=600, color=TEXT_FG,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                              edgecolor=ACCENT_RED, lw=0.8, alpha=0.95),
                    arrowprops=dict(arrowstyle="-", color=ACCENT_RED, lw=0.5),
                    ha="center")

    style(ax,
          title="Himalayas · important passes",
          subtitle="Strategic gaps used for trade, pilgrimage, and military movement",
          extent=(72, 98, 26, 37))
    plt.tight_layout()
    p = f"{OUT}/fig-passes.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PLT_BG)
    plt.close()
    print("✓", p)


if __name__ == "__main__":
    fig_three_ranges()
    fig_regional_divisions()
    fig_peaks()
    fig_passes()
    print(f"\nAll Ch 3 maps generated in {OUT}")
