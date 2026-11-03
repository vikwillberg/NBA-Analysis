from style_team import *
from matplotlib.patches import Circle
set_team("LAL", "#552583")
import style_team as _st
TEAM_C, TEAM_TINT, KICK_C, SUB_C, TEAM = _st.TEAM_C, _st.TEAM_TINT, _st.KICK_C, _st.SUB_C, _st.TEAM
LUKA = 3945274
def headshot(ax, pid, cx, cy, d=44, badge=None, ring=None, z=6, ring_w=3):
    ax.imshow(head_img(pid), extent=(cx - d/2, cx + d/2, cy + d/2, cy - d/2), zorder=z, interpolation="antialiased")
    if ring: ax.add_patch(Circle((cx, cy), d/2, fc="none", ec=ring, lw=ring_w, zorder=z+1))
    if badge:
        r = max(9, d*0.2); bx, by = cx + d*0.38, cy + d*0.36
        ax.add_patch(Circle((bx, by), r, fc="white", ec=GRID, lw=0.8, zorder=z+2)); logo_at(ax, badge, bx, by, size=int(r*1.45), z=z+3)
def setup(kicker, title, subtitle):
    fig = new_fig(); ax = canvas(fig); band_header(fig, ax, kicker, title, subtitle); return fig, ax

def pill(ax, x, y, w, h, fc=None, r=10, z=0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}', fc=fc or TEAM_TINT, ec='none', zorder=z))

# Luka = green marks (his identity on the data); Lakers purple stays in the header band
LUKA_C = GOOD; LUKA_TINT = _st._mix(GOOD, 0.88); LUKA_TXT = "#0b6b34"
def pill(ax, x, y, w, h, fc=None, r=10, z=0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}', fc=fc or LUKA_TINT, ec='none', zorder=z))
def band_header(fig, ax, kicker, title, subtitle):
    """LUKA vs NBA lockup: Luka's face (white ring, small Lakers badge) + VS + NBA chip."""
    ax.add_patch(Rectangle((0, 0), W, _st.BAND_H, color=_st.TEAM_C, lw=0, zorder=0))
    fig.text(fx(M), fy(58), kicker.upper(), fontsize=pt(22), fontweight=700, color=_st.KICK_C, va="top")
    fig.text(fx(M), fy(100), title, fontsize=pt(62), fontweight=700, color="white", va="top", linespacing=1.05)
    fig.text(fx(M), fy(254), subtitle, fontsize=pt(29), color=_st.SUB_C, va="top", linespacing=1.3)
    cy = 66; d = 72
    nba = load_logo("NBA", 160); nh = 52; nw = nh * nba.shape[1] / nba.shape[0]
    chip_w = nw + 18; x_nba = W - M - chip_w
    ax.add_patch(FancyBboxPatch((x_nba, cy - 32), chip_w, 64, boxstyle="round,pad=0,rounding_size=12", fc="white", ec="none", zorder=2))
    ax.imshow(nba, extent=(x_nba + 9, x_nba + 9 + nw, cy + nh / 2, cy - nh / 2), zorder=3, interpolation="antialiased")
    ax.text(x_nba - 16, cy + 1, "VS", fontsize=pt(24), fontweight=700, color="white", ha="right", va="center", zorder=3)
    cx = x_nba - 66 - d / 2
    ax.add_patch(Circle((cx, cy), d / 2 + 3, fc="white", ec="none", zorder=2))
    ax.imshow(head_img(LUKA), extent=(cx - d/2, cx + d/2, cy + d/2, cy - d/2), zorder=3, interpolation="antialiased")
    bx, by = cx + d * 0.38, cy + d * 0.36
    ax.add_patch(Circle((bx, by), 14, fc="white", ec="none", zorder=4)); logo_at(ax, "LAL", bx, by, size=22, z=5)
def setup(kicker, title, subtitle):
    fig = new_fig(); ax = canvas(fig); band_header(fig, ax, kicker, title, subtitle); return fig, ax
