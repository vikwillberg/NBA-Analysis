"""Team vs NBA look: team-color header band, TEAM vs NBA lockup, team in color vs grayscale league."""
from style import *
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
WHITE = "#ffffff"; BAND_H = 330
TEAM = "PHI"; TEAM_C = "#006BB6"; TEAM_TINT = "#e3eef8"; KICK_C = "#cfe3f4"; SUB_C = "#e6f0f9"

def _mix(hex_c, t):   # blend a color toward white by t (0..1)
    c = np.array([int(hex_c[i:i + 2], 16) for i in (1, 3, 5)]); m = c + (255 - c) * t
    return "#" + "".join(f"{int(round(v)):02x}" for v in m)

def set_team(abbr, color):
    """Story team + its primary color (white text on it must reach contrast >= 4.5)."""
    global TEAM, TEAM_C, TEAM_TINT, KICK_C, SUB_C
    TEAM, TEAM_C = abbr, color
    TEAM_TINT, KICK_C, SUB_C = _mix(color, 0.89), _mix(color, 0.80), _mix(color, 0.90)

def gray_logo(abbr, box=88, alpha=0.8):
    im = Image.open(f"{WORK}/logos/{abbr}.png").convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    a = im.getchannel("A"); g = im.convert("L").point(lambda v: int(70 + v * 0.6))   # lift darks: black logos stay visible
    out = Image.merge("RGBA", (g, g, g, a.point(lambda v: int(v * alpha)))).convert("RGBa")
    out.thumbnail((box, box), Image.LANCZOS)
    return np.asarray(out.convert("RGBA"))

def logo_any(ax, abbr, cx, cy, size=44, z=6, gray=False, alpha=0.8):
    arr = gray_logo(abbr, 2 * size, alpha) if gray else load_logo(abbr, 2 * size)
    h, w = arr.shape[:2]; s = size / max(h, w)
    ax.imshow(arr, extent=(cx - w * s / 2, cx + w * s / 2, cy + h * s / 2, cy - h * s / 2), zorder=z, interpolation="antialiased")

def team_logo_ring(ax, cx, cy, r=38, ring=3.5, z=9):
    """Story team logo, full color, on a white circle with a team-color ring."""
    ax.add_patch(Circle((cx, cy), r, fc=WHITE, ec=TEAM_C, lw=ring, zorder=z)); logo_at(ax, TEAM, cx, cy, size=int(r * 1.5), z=z + 1)

def band_header(fig, ax, kicker, title, subtitle):
    """Use instead of header(): kicker like '76ers vs NBA  ·  2/4'."""
    ax.add_patch(Rectangle((0, 0), W, BAND_H, color=TEAM_C, lw=0, zorder=0))
    fig.text(fx(M), fy(58), kicker.upper(), fontsize=pt(22), fontweight=700, color=KICK_C, va="top")
    fig.text(fx(M), fy(100), title, fontsize=pt(62), fontweight=700, color=WHITE, va="top", linespacing=1.05)
    fig.text(fx(M), fy(254), subtitle, fontsize=pt(29), color=SUB_C, va="top", linespacing=1.3)
    cy = 66; d = 64                                   # lockup: [TEAM]  VS  [NBA] in the kicker row
    nba = load_logo("NBA", 160); nh = 52; nw = nh * nba.shape[1] / nba.shape[0]
    chip_w = nw + 18; x_nba = W - M - chip_w
    ax.add_patch(FancyBboxPatch((x_nba, cy - d / 2), chip_w, d, boxstyle="round,pad=0,rounding_size=12", fc=WHITE, ec="none", zorder=2))
    ax.imshow(nba, extent=(x_nba + 9, x_nba + 9 + nw, cy + nh / 2, cy - nh / 2), zorder=3, interpolation="antialiased")
    ax.text(x_nba - 16, cy + 1, "VS", fontsize=pt(24), fontweight=700, color=WHITE, ha="right", va="center", zorder=3)
    cx = x_nba - 58 - d / 2
    ax.add_patch(Circle((cx, cy), d / 2, fc=WHITE, ec="none", zorder=2)); logo_at(ax, TEAM, cx, cy, size=50, z=3)

def pill(ax, x, y, w, h, fc=None, r=10, z=0):
    """Light team-tint highlight behind the story team's row or total."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc or TEAM_TINT, ec="none", zorder=z))
