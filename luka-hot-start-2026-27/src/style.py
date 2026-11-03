"""Viktor Berg NBA data story template: 1080x1350 layout, exported at 2x."""
import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.collections import LineCollection
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from PIL import Image

WORK = os.environ.get("NBA_WORK", ".")
for w in (400, 500, 600, 700):
    fm.fontManager.addfont(f"{WORK}/fonts/Inter-{w}.ttf")
plt.rcParams["font.family"] = "Inter"

SURFACE = "#fbfaf7"; INK = "#0b0b0b"; INK2 = "#45443f"; MUTED = "#7d7b74"
GRID = "#e4e2da"; AXIS = "#b9b7ae"
GOOD = "#12a150"; BAD = "#b3261e"; NEUTRAL = "#c9c6bc"; NEUTRAL_DK = "#8f8c83"
W, H, DPI_LAYOUT, EXPORT_SCALE, M = 1080, 1350, 150, 2, 64
AUTHOR = "Viktor Berg"

def pt(px): return px * 72 / DPI_LAYOUT          # font size (pt) for a pixel height at 1080 width
def fx(px): return px / W
def fy(px_from_top): return 1 - px_from_top / H

def load_logo(abbr, box=88):
    im = Image.open(f"{WORK}/logos/{abbr}.png").convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox()).convert("RGBa")   # premultiplied: no halo
    im.thumbnail((box, box), Image.LANCZOS)
    return np.asarray(im.convert("RGBA"))

def new_fig():
    return plt.figure(figsize=(W / DPI_LAYOUT, H / DPI_LAYOUT), dpi=DPI_LAYOUT, facecolor=SURFACE)

def canvas(fig):
    """Full-figure axes in layout pixels, y down (0,0 = top-left)."""
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off"); return ax

def header(fig, kicker, title, subtitle, title_lines=2):
    fig.text(fx(M), fy(58), kicker.upper(), fontsize=pt(22), fontweight=600, color=MUTED, va="top")
    fig.text(fx(M), fy(100), title, fontsize=pt(62), fontweight=700, color=INK, va="top", linespacing=1.05)
    sub_top = 100 + title_lines * 66 + 22
    fig.text(fx(M), fy(sub_top), subtitle, fontsize=pt(29), color=INK2, va="top", linespacing=1.3)
    arr = load_logo("NBA", 192); h_px = 96; w_px = h_px * arr.shape[1] / arr.shape[0]
    a = fig.add_axes([fx(W - M - w_px), fy(52 + h_px), fx(w_px), h_px / H]); a.imshow(arr, interpolation="antialiased"); a.axis("off")
    return sub_top          # subtitle top y (px); 1-line subtitle ends ~sub_top+38

def footer(fig, source):
    fig.add_artist(plt.Line2D([fx(M), fx(W - M)], [fy(1282), fy(1282)], transform=fig.transFigure, color=GRID, lw=1))
    fig.text(fx(M), fy(1300), source, fontsize=pt(21), color=MUTED, va="top")
    fig.text(fx(W - M), fy(1298), AUTHOR, fontsize=pt(24), fontweight=700, color=INK2, va="top", ha="right")

def save(fig, path):
    fig.savefig(path, dpi=DPI_LAYOUT * EXPORT_SCALE, facecolor=SURFACE); plt.close(fig)
    Image.open(path).convert("RGB").save(path, optimize=True)

def hbar(ax, x0, yc, length, thick, color, r=5):
    """Horizontal bar, rounded data end, square at baseline; negative length grows left."""
    if abs(length) < 1e-9: return
    s = 1 if length > 0 else -1; L = abs(length); left = x0 if s > 0 else x0 - L
    if L <= 2 * r: ax.add_patch(Rectangle((left, yc - thick / 2), L, thick, color=color, lw=0)); return
    ax.add_patch(FancyBboxPatch((left, yc - thick / 2), L, thick, boxstyle=f"round,pad=0,rounding_size={r}", fc=color, ec="none"))
    ax.add_patch(Rectangle((x0 if s > 0 else x0 - 2 * r, yc - thick / 2), 2 * r, thick, color=color, lw=0))

def vbar(ax, xc, y0, height, width, color, r=6):
    """Column from baseline y0 upward by height px, rounded top."""
    ax.add_patch(FancyBboxPatch((xc - width / 2, y0 - height), width, height, boxstyle=f"round,pad=0,rounding_size={r}", fc=color, ec="none"))
    ax.add_patch(Rectangle((xc - width / 2, y0 - 2 * r), width, 2 * r, color=color, lw=0))

def logo_at(ax, abbr, cx, cy, size=44, z=6):
    arr = load_logo(abbr, 2 * size); h, w = arr.shape[:2]; s = size / max(h, w)
    ax.imshow(arr, extent=(cx - w * s / 2, cx + w * s / 2, cy + h * s / 2, cy - h * s / 2), zorder=z, interpolation="antialiased")

def legend(ax, y, items, x=None, gap=48):
    """items: [(color, label, 'line'|'box'), ...] in one row."""
    x = M if x is None else x; fp = FontProperties(family="Inter", size=pt(24))
    for col, lab, kind in items:
        if kind == "line": ax.plot([x, x + 28], [y, y], color=col, lw=4, solid_capstyle="round")
        else: ax.add_patch(FancyBboxPatch((x + 3, y - 11), 22, 22, boxstyle="round,pad=0,rounding_size=4", fc=col, ec="none"))
        ax.text(x + 40, y, lab, fontsize=pt(24), color=INK2, va="center", ha="left")
        x += 40 + TextPath((0, 0), lab, prop=fp).get_extents().width * DPI_LAYOUT / 72 + gap

def note(ax, x, y, text, ha="left", size=25, weight=600, color=None, va="top"):
    ax.text(x, y, text, fontsize=pt(size), fontweight=weight, color=color or INK, ha=ha, va=va, linespacing=1.25, zorder=8)

def arrow(ax, xy_from, xy_to, rad=0.0, color=None):
    ax.annotate("", xy=xy_to, xytext=xy_from, zorder=8, arrowprops=dict(arrowstyle="-|>,head_length=0.55,head_width=0.32",
                color=color or INK, lw=2.2, shrinkA=0, shrinkB=0, connectionstyle=f"arc3,rad={rad}"))

def swipe_cue(ax, y=1236, text="Swipe to see why"):
    ax.text(W - M - 52, y, text, fontsize=pt(24), fontweight=700, color=INK, ha="right", va="center")
    ax.annotate("", xy=(W - M, y + 1), xytext=(W - M - 40, y + 1),
                arrowprops=dict(arrowstyle="-|>,head_length=0.55,head_width=0.32", color=INK, lw=2.6, shrinkA=0, shrinkB=0))

def hand_oval(ax, p1, p2, pad=48, minor=64, color=None):
    """Thin, tapered, hand-drawn-looking oval around two points (layout px). Returns outline x, y."""
    p1, p2 = np.asarray(p1, float), np.asarray(p2, float); c = (p1 + p2) / 2; v = p2 - p1; ang = np.arctan2(v[1], v[0])
    A = np.hypot(*v) / 2 + pad; tt = np.linspace(-0.15, 2 * np.pi + 0.35, 600)
    wob = 1 + 0.012 * np.sin(2 * tt + 0.8) + 0.075 * (tt / (2 * np.pi))       # gentle spiral so the loop overshoots
    ex, ey = A * wob * np.cos(tt), minor * wob * np.sin(tt)
    px = c[0] + ex * np.cos(ang) - ey * np.sin(ang); py = c[1] + ex * np.sin(ang) + ey * np.cos(ang)
    segs = np.stack([np.column_stack([px[:-1], py[:-1]]), np.column_stack([px[1:], py[1:]])], axis=1)
    u = np.linspace(0, 1, len(segs)); taper = np.minimum(1, np.minimum(u / 0.08, (1 - u) / 0.12))
    ax.add_collection(LineCollection(segs, linewidths=0.6 + 2.2 * taper, colors=color or GOOD, capstyle="round", zorder=7))
    return px, py

def repel(anchors, fixed=None, size=38, iters=4000, floor_y=None):
    """Spread overlapping logo positions (layout px) while pulling each back to its true point.
    Draw a light leader line (#c9c6bc, 1px) + small dot at the true point when a logo moved >12px.
    To keep an area clear (a story team's gap bar or big logo), append invisible fixed obstacle points to the anchors."""
    anch = np.asarray(anchors, float); pos = anch + np.random.default_rng(7).normal(0, 1.0, anch.shape)
    fixed = np.zeros(len(pos), bool) if fixed is None else np.asarray(fixed); pos[fixed] = anch[fixed]; D = size + 6
    for _ in range(iters):
        mv = np.zeros_like(pos)
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                d = pos[i] - pos[j]; dist = np.hypot(*d)
                if dist < D:
                    u = d / dist if dist > 1e-6 else np.array([1.0, 0.0]); mv[i] += u * (D - dist) / 2; mv[j] -= u * (D - dist) / 2
        mv += (anch - pos) * 0.01; mv[fixed] = 0; pos += mv * 0.6
        if floor_y is not None: pos[:, 1] = np.minimum(pos[:, 1], floor_y)
    return pos

def build_pdf(pngs, out_pdf):
    import img2pdf
    layout = img2pdf.get_layout_fun((img2pdf.in_to_pt(10.8), img2pdf.in_to_pt(13.5)))
    open(out_pdf, "wb").write(img2pdf.convert(sorted(pngs), layout_fun=layout))

# ESPN headshots: https://a.espncdn.com/i/headshots/nba/players/full/{espn_id}.png -> $WORK/heads/{espn_id}.png (600x436 RGBA)
HEAD_BG = "#e9e6dd"
def head_img(espn_id, px=240, bg=HEAD_BG):
    """Circular avatar: square crop around the face (finds the head top from alpha), light warm-gray fill."""
    from PIL import ImageDraw
    im = Image.open(f"{WORK}/heads/{int(espn_id)}.png").convert("RGBA")
    a = np.asarray(im)[:, :, 3]; top = np.where(a.max(1) > 20)[0][0]
    cols = np.where(a[top + 40:top + 200].max(0) > 20)[0]; cx = (cols[0] + cols[-1]) / 2
    s = 330; x0 = int(round(cx - s / 2)); y0 = max(0, int(top - 0.07 * s))
    x0 = min(max(x0, 0), im.width - s)
    base = Image.new("RGBA", (s, s), bg); base.alpha_composite(im.crop((x0, y0, x0 + s, y0 + s)))
    big = base.resize((px * 4, px * 4), Image.LANCZOS)
    mask = Image.new("L", big.size, 0); ImageDraw.Draw(mask).ellipse((0, 0, big.size[0] - 1, big.size[1] - 1), fill=255)
    big.putalpha(mask)
    return np.asarray(big.convert("RGBa").resize((px, px), Image.LANCZOS).convert("RGBA"))

def headshot_at(ax, espn_id, cx, cy, d=50, badge=None, z=6):
    """Headshot circle (d px). badge = team abbr for a small logo chip at the bottom-right (team left / joined)."""
    from matplotlib.patches import Circle
    ax.imshow(head_img(espn_id), extent=(cx - d / 2, cx + d / 2, cy + d / 2, cy - d / 2), zorder=z, interpolation="antialiased")
    if badge:
        bx, by = cx + d * 0.38, cy + d * 0.34
        ax.add_patch(Circle((bx, by), 14, fc="white", ec=GRID, lw=1, zorder=z + 1)); logo_at(ax, badge, bx, by, size=20, z=z + 2)
