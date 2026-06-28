"""
Generate high-quality, factually accurate maps for Chapter 2.

Source data:
  - Natural Earth 1:50m & 1:10m public domain (https://www.naturalearthdata.com)
  - Indian govt official figures for coordinates

All output written to /Users/aniket/Documents/TNPSC-Geography/assets/images/ch02/
"""
import os, sys
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.lines import Line2D

OUT = "/Users/aniket/Documents/TNPSC-Geography/assets/images/ch02"
os.makedirs(OUT, exist_ok=True)

# Style
PLT_BG = "#fdfeff"
INDIA_FILL = "#d5e4fc"
INDIA_EDGE = "#1a3d80"
WATER = "#eaf2ff"
ACCENT = "#1a3d80"
ACCENT2 = "#d04967"
HIGHLIGHT = "#ffd400"
TEXT_FG = "#0d1b2a"
GRAT = "#e2e8f1"

plt.rcParams.update({
    "font.family": "Inter",
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

# Filter
india = countries[countries["ADMIN"] == "India"].copy()
india_states = states[states["admin"] == "India"].copy()
print(f"India geometry rows: {len(india)}; states: {len(india_states)}")
print(f"State names (first 10): {sorted(india_states['name'].tolist())[:10]}")

# Neighbours of interest
NB_LAND = ["Pakistan", "China", "Nepal", "Bhutan", "Bangladesh", "Myanmar", "Afghanistan"]
NB_MAR = ["Sri Lanka", "Maldives", "Indonesia", "Thailand"]
neighbours_land = countries[countries["ADMIN"].isin(NB_LAND)].copy()
neighbours_mar = countries[countries["ADMIN"].isin(NB_MAR)].copy()

# Common extent
INDIA_EXTENT = (66, 99, 5, 38)  # minlon, maxlon, minlat, maxlat

def style_ax(ax, title=None, subtitle=None, extent=INDIA_EXTENT, grid=True, water=True):
    minx, maxx, miny, maxy = extent
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_aspect("equal")
    if water:
        ax.set_facecolor(WATER)
    if grid:
        ax.set_xticks(range(int(minx), int(maxx)+1, 5))
        ax.set_yticks(range(int(miny), int(maxy)+1, 5))
        ax.tick_params(axis="both", labelsize=7, color="#cad4e2", labelcolor="#6b6b66")
        ax.grid(True, color=GRAT, linewidth=0.4, alpha=0.7)
    else:
        ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#cad4e2"); s.set_linewidth(0.6)
    if title:
        ax.set_title(title, fontsize=12, fontweight=700, color=ACCENT, pad=12, loc="left")
    if subtitle:
        ax.text(0, 1.018, subtitle, transform=ax.transAxes,
                fontsize=9, color="#56657a", style="italic")

# ===================== FIG 2.2 — Extreme Points Map =====================
def fig_extreme_points():
    fig, ax = plt.subplots(figsize=(10, 11), dpi=160)
    # Surrounding countries grey
    other = countries[(~countries["ADMIN"].isin(NB_LAND)) & (countries["ADMIN"] != "India")]
    other.plot(ax=ax, color="#f3f3f0", edgecolor="#d8d6cc", linewidth=0.3)
    neighbours_land.plot(ax=ax, color="#f0e6cf", edgecolor="#bdbab0", linewidth=0.5)
    neighbours_mar.plot(ax=ax, color="#f0e6cf", edgecolor="#bdbab0", linewidth=0.5)
    india.plot(ax=ax, color=INDIA_FILL, edgecolor=INDIA_EDGE, linewidth=1.2)

    # Tropic of Cancer
    ax.axhline(23.5, color=ACCENT2, linewidth=1.2, linestyle=(0,(6,4)), alpha=0.85)
    ax.text(98.5, 23.7, "Tropic of Cancer · 23.5°N", color=ACCENT2,
            fontsize=9, fontweight=700, ha="right", va="bottom")

    # Standard Meridian
    ax.axvline(82.5, color="#2d5e7a", linewidth=1.0, linestyle=(0,(3,2)), alpha=0.8)
    ax.text(82.7, 37.4, "82°30′E · IST", color="#2d5e7a", fontsize=8, va="top")

    # Extreme points (real coordinates)
    points = [
        ("NORTH", "Indira Col\n(Karakoram, Ladakh)", "37°6′N · 77°10′E", 77.17, 37.10, (-50, -10)),
        ("SOUTH (mainland)", "Kanyakumari", "8°4′N · 77°34′E", 77.55, 8.08, (10, -25)),
        ("SOUTH (territory)", "Indira Point\n(Great Nicobar)", "6°45′N · 93°50′E", 93.83, 6.75, (-10, -25)),
        ("WEST", "Guhar Moti\n(Sir Creek, Gujarat)", "23°42′N · 68°7′E", 68.12, 23.70, (-65, 12)),
        ("EAST", "Kibithoo\n(Arunachal Pradesh)", "28°1′N · 97°25′E", 97.42, 28.02, (8, 8)),
    ]
    for tag, name, coord, lon, lat, off in points:
        ax.scatter([lon], [lat], s=160, color=HIGHLIGHT, edgecolor=ACCENT,
                   linewidth=2.0, zorder=5)
        ax.scatter([lon], [lat], s=40, color=ACCENT, zorder=6)
        box = dict(boxstyle="round,pad=0.5", facecolor="white",
                   edgecolor=ACCENT, linewidth=1.0, alpha=0.95)
        ax.annotate(f"{tag}\n{name}\n{coord}",
                    xy=(lon, lat), xytext=(lon+off[0]/15.0, lat+off[1]/15.0),
                    fontsize=8, color=TEXT_FG, fontweight=600,
                    bbox=box, ha="center",
                    arrowprops=dict(arrowstyle="-", color=ACCENT, lw=1.0))

    # Country labels (small, in distinct colour)
    label_pts = {
        "Pakistan": (70.5, 30.0), "China": (88, 35), "Nepal": (84, 28.3),
        "Bhutan": (90.7, 27.5), "Bangladesh": (90.2, 23.7),
        "Myanmar": (96, 22), "Sri Lanka": (80.7, 7.7), "Afghanistan": (67.5, 33.5)
    }
    for k, (lo, la) in label_pts.items():
        ax.text(lo, la, k, fontsize=7, color="#6b6b66", style="italic",
                ha="center", fontweight=500)

    style_ax(ax,
             title="India · the four extreme points",
             subtitle="Source: Natural Earth 1:50m. Coordinates as per Survey of India.")
    ax.set_extent if False else None
    plt.tight_layout()
    p = f"{OUT}/fig-extreme-points.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PLT_BG)
    plt.close()
    print("✓", p)

# ===================== FIG 2.5 — Tropic of Cancer states =====================
def fig_tropic_states():
    fig, ax = plt.subplots(figsize=(11, 9), dpi=160)
    other = countries[(~countries["ADMIN"].isin(NB_LAND)) & (countries["ADMIN"] != "India")]
    other.plot(ax=ax, color="#f3f3f0", edgecolor="#d8d6cc", linewidth=0.3)
    neighbours_land.plot(ax=ax, color="#f0e6cf", edgecolor="#bdbab0", linewidth=0.5)

    # All Indian states light
    india_states.plot(ax=ax, color="#eef3fb", edgecolor="#b6cffa", linewidth=0.4)

    # Highlight Tropic of Cancer states - 8 of them
    TROPIC_STATES = ["Gujarat", "Rajasthan", "Madhya Pradesh", "Chhattisgarh",
                     "Jharkhand", "West Bengal", "Tripura", "Mizoram"]
    tropic_gdf = india_states[india_states["name"].isin(TROPIC_STATES)]
    tropic_gdf.plot(ax=ax, color=ACCENT2, edgecolor="white", linewidth=0.8, alpha=0.85)

    # Tropic of Cancer line
    ax.axhline(23.5, color=ACCENT2, linewidth=1.6, linestyle=(0,(7,4)), alpha=0.9)
    ax.text(98.5, 23.7, "TROPIC OF CANCER · 23°30′N", color=ACCENT2,
            fontsize=11, fontweight=800, ha="right", va="bottom")

    # Number the states by west→east order
    for i, name in enumerate(TROPIC_STATES, start=1):
        row = tropic_gdf[tropic_gdf["name"] == name].iloc[0]
        c = row.geometry.representative_point()
        ax.scatter([c.x], [c.y], s=260, color="white", edgecolor=ACCENT2,
                   linewidth=2.0, zorder=5)
        ax.text(c.x, c.y, str(i), fontsize=11, fontweight=800,
                color=ACCENT2, ha="center", va="center", zorder=6)
        ax.text(c.x, c.y - 0.7, name, fontsize=7.5, fontweight=600,
                color=TEXT_FG, ha="center", va="top")

    style_ax(ax,
             title="Tropic of Cancer · the eight states it crosses",
             subtitle="Numbered 1→8 west to east — the exam-tested order",
             extent=(67, 100, 17, 30))
    plt.tight_layout()
    p = f"{OUT}/fig-tropic-states.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PLT_BG)
    plt.close()
    print("✓", p)

# ===================== FIG 2.4 — Standard Meridian =====================
def fig_standard_meridian():
    fig, ax = plt.subplots(figsize=(11, 9), dpi=160)
    other = countries[(~countries["ADMIN"].isin(NB_LAND)) & (countries["ADMIN"] != "India")]
    other.plot(ax=ax, color="#f3f3f0", edgecolor="#d8d6cc", linewidth=0.3)
    neighbours_land.plot(ax=ax, color="#f0e6cf", edgecolor="#bdbab0", linewidth=0.5)

    india_states.plot(ax=ax, color="#eef3fb", edgecolor="#b6cffa", linewidth=0.4)

    # Highlight 5 states crossed by 82°30'E
    SM_STATES = ["Uttar Pradesh", "Madhya Pradesh", "Chhattisgarh", "Odisha", "Andhra Pradesh"]
    sm_gdf = india_states[india_states["name"].isin(SM_STATES)]
    sm_gdf.plot(ax=ax, color="#3b78e7", edgecolor="white", linewidth=0.8, alpha=0.85)

    # Standard Meridian line
    ax.axvline(82.5, color="#1a3d80", linewidth=2, linestyle=(0,(8,3)), alpha=0.95)
    ax.text(82.7, 9, "STANDARD MERIDIAN · 82°30′E", color="#1a3d80",
            fontsize=11, fontweight=800, rotation=90, va="bottom")

    # Number states north → south
    for i, name in enumerate(SM_STATES, start=1):
        row = sm_gdf[sm_gdf["name"] == name].iloc[0]
        c = row.geometry.representative_point()
        ax.scatter([c.x], [c.y], s=280, color="white", edgecolor="#1a3d80",
                   linewidth=2.2, zorder=5)
        ax.text(c.x, c.y, str(i), fontsize=12, fontweight=800,
                color="#1a3d80", ha="center", va="center", zorder=6)
        ax.text(c.x, c.y - 0.7, name, fontsize=7.5, fontweight=600,
                color=TEXT_FG, ha="center", va="top")

    # Mirzapur marker
    ax.scatter([82.57], [25.15], s=160, color=HIGHLIGHT, edgecolor="#1a3d80",
               linewidth=2, zorder=7)
    ax.annotate("Mirzapur\n(82°30′E, 25°9′N)\nlandmark city",
                xy=(82.57, 25.15), xytext=(89, 28),
                fontsize=8.5, color=TEXT_FG, fontweight=600,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                          edgecolor="#1a3d80", lw=1.2),
                arrowprops=dict(arrowstyle="->", color="#1a3d80", lw=1.0),
                ha="center")

    # IST formula corner box
    txt = "INDIAN STANDARD TIME\n\nUTC + 5:30\n\n82°30′ ÷ 15° = 5 hr 30 min ahead of GMT"
    ax.text(0.02, 0.02, txt, transform=ax.transAxes,
            fontsize=10, color="white", fontweight=700,
            ha="left", va="bottom",
            bbox=dict(boxstyle="round,pad=0.8", facecolor="#1a3d80",
                      edgecolor="#ffd400", linewidth=2))

    style_ax(ax,
             title="Standard Meridian · 82°30′E through five states",
             subtitle="UP → MP → Chhattisgarh → Odisha → Andhra Pradesh (north to south)",
             extent=(67, 100, 7, 38))
    plt.tight_layout()
    p = f"{OUT}/fig-standard-meridian.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PLT_BG)
    plt.close()
    print("✓", p)

# ===================== FIG 2.7 — Maritime Neighbours =====================
def fig_maritime():
    fig, ax = plt.subplots(figsize=(11, 11), dpi=160)
    other = countries[(~countries["ADMIN"].isin(NB_LAND+NB_MAR)) & (countries["ADMIN"] != "India")]
    other.plot(ax=ax, color="#f3f3f0", edgecolor="#d8d6cc", linewidth=0.3)
    neighbours_land.plot(ax=ax, color="#f0e6cf", edgecolor="#bdbab0", linewidth=0.5)
    neighbours_mar.plot(ax=ax, color="#fbe2e7", edgecolor=ACCENT2, linewidth=0.7)
    india.plot(ax=ax, color=INDIA_FILL, edgecolor=INDIA_EDGE, linewidth=1.2)

    # Label all 7 maritime neighbours
    mar_label = {
        "Pakistan": (66.0, 27.5, "1 · Pakistan", "Arabian Sea (NW)"),
        "Maldives": (73.0, 4.0, "2 · Maldives", "8° Channel (SW)"),
        "Sri Lanka": (80.7, 7.7, "3 · Sri Lanka", "Palk Strait — TN coast"),
        "Bangladesh": (90.0, 23.5, "4 · Bangladesh", "Bay of Bengal (E)"),
        "Myanmar": (96.0, 21.0, "5 · Myanmar", "Andaman Sea (E)"),
        "Thailand": (99.0, 13.5, "6 · Thailand", "Andaman Sea (SE)"),
        "Indonesia": (97.0, 4.0, "7 · Indonesia", "6° Channel (SE)"),
    }
    for k, (lo, la, n1, n2) in mar_label.items():
        ax.scatter([lo], [la], s=80, color=ACCENT2, edgecolor="white",
                   linewidth=2, zorder=6)
        ax.text(lo+0.5, la, f"{n1}\n{n2}", fontsize=8, fontweight=600,
                color=TEXT_FG,
                bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                          edgecolor=ACCENT2, alpha=0.95, lw=1))

    # Channels — annotate visually
    chan = [
        (10.5, 92.5, "Ten Degree Channel", "Andaman ↔ Nicobar"),
        (9.0, 73.5, "Nine Degree Channel", "Minicoy ↔ Lakshadweep"),
        (8.0, 73.0, "Eight Degree Channel", "India ↔ Maldives"),
        (6.0, 94.5, "Six Degree Channel", "India ↔ Indonesia"),
    ]
    for la, lo, name, desc in chan:
        ax.axhline(la, xmin=(lo-2-66)/(105-66), xmax=(lo+2-66)/(105-66),
                   color="#3b78e7", linewidth=1.4, linestyle="--")
        ax.text(lo, la-0.3, name, fontsize=7, color="#1a3d80",
                fontweight=700, ha="center", va="top")

    # Adam's Bridge / Palk Strait
    ax.annotate("Adam's Bridge\n(Ram Setu)", xy=(79.5, 9.1), xytext=(76.5, 11),
                fontsize=8, color="#b18a2e", fontweight=700,
                arrowprops=dict(arrowstyle="->", color="#b18a2e"))

    style_ax(ax,
             title="Maritime neighbours · the seven across the seas",
             subtitle="Plus the four sea channels — labelled by latitude (10°, 9°, 8°, 6°)",
             extent=(65, 105, 0, 38))
    plt.tight_layout()
    p = f"{OUT}/fig-maritime.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PLT_BG)
    plt.close()
    print("✓", p)

# ===================== FIG 2.9 — Palk Strait close-up =====================
def fig_palk():
    fig, ax = plt.subplots(figsize=(11, 8), dpi=160)
    countries.plot(ax=ax, color="#f3f3f0", edgecolor="#d8d6cc", linewidth=0.3)
    india.plot(ax=ax, color=INDIA_FILL, edgecolor=INDIA_EDGE, linewidth=1.2)
    countries[countries["ADMIN"] == "Sri Lanka"].plot(
        ax=ax, color="#fbe2e7", edgecolor=ACCENT2, linewidth=1.2)

    # Adam's Bridge - actual coordinates of the shoal chain
    bridge = [(79.21, 9.18), (79.32, 9.15), (79.45, 9.12), (79.58, 9.10),
              (79.72, 9.09), (79.85, 9.08)]
    for lon, lat in bridge:
        ax.scatter([lon], [lat], s=50, color="#b18a2e", edgecolor="white",
                   linewidth=0.8, zorder=5)
    ax.plot([b[0] for b in bridge], [b[1] for b in bridge],
            color="#b18a2e", linewidth=1.0, linestyle=":", alpha=0.6)

    # Key place markers
    sites = [
        ("Dhanushkodi", 79.42, 9.15, (10, 22)),
        ("Rameswaram", 79.30, 9.29, (10, 8)),
        ("Pamban Bridge", 79.20, 9.30, (-50, 10)),
        ("Mannar (SL)", 79.91, 8.98, (8, -25)),
        ("Talaimannar (SL)", 79.74, 9.10, (8, -22)),
    ]
    for name, lo, la, off in sites:
        ax.scatter([lo], [la], s=70, color=ACCENT, edgecolor="white",
                   linewidth=1.5, zorder=6)
        ax.annotate(name, xy=(lo, la),
                    xytext=(lo+off[0]/40.0, la+off[1]/40.0),
                    fontsize=8.5, fontweight=600, color=TEXT_FG,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                              edgecolor=ACCENT, lw=0.8),
                    arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.6))

    # Region labels
    ax.text(78.5, 10.5, "PALK STRAIT\n(north of bridge)", fontsize=10, fontweight=800,
            color="#1a3d80", ha="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=WATER, alpha=0.8))
    ax.text(79.0, 8.3, "GULF OF MANNAR\n(south of bridge)", fontsize=10, fontweight=800,
            color="#1a3d80", ha="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=WATER, alpha=0.8))
    ax.text(77.5, 9.5, "TAMIL NADU\n(Ramanathapuram)", fontsize=11, fontweight=800,
            color="#1a3d80", ha="center")
    ax.text(80.5, 7.5, "SRI LANKA", fontsize=12, fontweight=800,
            color=ACCENT2, ha="center")

    style_ax(ax,
             title="Tamil Nadu — Sri Lanka · Palk Strait region",
             subtitle="Adam's Bridge (Ram Setu) – shoal chain ~30 km long between Dhanushkodi and Mannar",
             extent=(77, 81.5, 7, 10.8))
    plt.tight_layout()
    p = f"{OUT}/fig-palk.png"
    plt.savefig(p, dpi=200, bbox_inches="tight", facecolor=PLT_BG)
    plt.close()
    print("✓", p)

if __name__ == "__main__":
    fig_extreme_points()
    fig_tropic_states()
    fig_standard_meridian()
    fig_maritime()
    fig_palk()
    print("\nAll maps generated in:", OUT)
