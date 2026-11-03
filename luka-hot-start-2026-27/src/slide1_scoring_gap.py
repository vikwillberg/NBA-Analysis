from common import *
import pandas as pd
p = pd.read_parquet("data/players2027.parquet"); q = p[(p.gp >= 0.7*p.team_gp) & (p.min_pg >= 20)].sort_values("pts_pg", ascending=False).head(10).reset_index(drop=True)
gap = pd.read_parquet("data/gap_hist.parquet")
fig, ax = setup("Luka vs NBA  ·  1/5", "Luka leads the NBA in\nscoring by 8.3 a game", "Points per game, first two weeks of 2026-27 (thru Nov. 2)")
x0, sc, y0, rh = 452, 11.6, 384, 45
for i, r in q.iterrows():
    cy = y0 + i*rh; me = r["name"] == "Luka Doncic"
    if me: pill(ax, M - 8, cy - 22, W - 2*M + 16, 44, z=0)
    ax.text(M + 18, cy, str(i+1), fontsize=pt(22), color=INK2 if me else MUTED, ha="right", va="center", fontweight=600)
    headshot(ax, int(r.pid), 116, cy, d=42, badge=r.team, ring=LUKA_C if me else None, ring_w=2.5)
    nm = r["name"].replace("Shai Gilgeous-Alexander", "S. Gilgeous-Alexander").replace("Giannis Antetokounmpo", "G. Antetokounmpo")
    ax.text(148, cy, nm, fontsize=pt(23), color=INK, ha="left", va="center", fontweight=700 if me else 500)
    L = r.pts_pg*sc
    hbar(ax, x0, cy, L, 26 if me else 22, LUKA_C if me else NEUTRAL)
    if i == 1:
        gw = (q.pts_pg[0] - r.pts_pg)*sc
        ax.add_patch(FancyBboxPatch((x0 + L + 4, cy - 11), gw - 4, 22, boxstyle="round,pad=0,rounding_size=5", fc=LUKA_TINT, ec=LUKA_C, lw=1.4, zorder=3))
        ax.text(x0 + L + gw/2 + 2, cy, "+8.3", fontsize=pt(21), fontweight=700, color=LUKA_TXT, ha="center", va="center", zorder=4)
        ax.text(x0 + L + gw + 10, cy, f"{r.pts_pg:.1f}", fontsize=pt(25), fontweight=600, color=INK2, ha="left", va="center")
    else:
        ax.text(x0 + L + 10, cy, f"{r.pts_pg:.1f}", fontsize=pt(27 if me else 25), fontweight=700 if me else 600, color=LUKA_TXT if me else INK2, ha="left", va="center")
# ---- bottom panel: gap history
ax.plot([M, W - M], [852, 852], color=GRID, lw=1)
note(ax, M, 874, "Gap between the No. 1 and No. 2 scorer after two weeks", size=25, weight=700)
note(ax, M, 908, "Every season since 2002-03", size=22, weight=400, color=MUTED)
seasons = list(gap.season) + [2027]; vals = list(gap.gap) + [q.pts_pg[0] - q.pts_pg[1]]
base, ps = 1196, 25.5; xl, xr = M + 20, W - M - 20; step = (xr - xl)/(len(seasons) - 1); bw = 22
avg = gap.gap.mean()
for k, (s, v) in enumerate(zip(seasons, vals)):
    cx = xl + k*step; col = LUKA_C if s == 2027 else (NEUTRAL_DK if s == 2018 else NEUTRAL)
    vbar(ax, cx, base, max(v*ps, 3), bw, col, r=4)
    if s in (2003, 2008, 2013, 2018, 2023): ax.text(cx - (12 if s == 2003 else 0), base + 12, f"{s-1}-{str(s)[2:]}", fontsize=pt(21), color=MUTED, ha="left" if s == 2003 else "center", va="top")
    if s == 2027:
        ax.text(cx, base + 12, "Now", fontsize=pt(21), color=INK, fontweight=700, ha="center", va="top")
        ax.text(cx, base - v*ps - 10, f"{v:.1f}", fontsize=pt(46), fontweight=700, color=LUKA_C, ha="center", va="bottom")
    if s == 2018:
        x18, y18 = cx, base - v*ps - 6
ax.plot([M, W - M - 44], [base - avg*ps]*2, color=INK2, lw=1.6, zorder=1, solid_capstyle="butt")
ax.text(M, base - avg*ps - 6, f"Average gap: {avg:.1f}", fontsize=pt(21), color=INK2, ha="left", va="bottom", fontweight=600)
ax.plot([M, W - M], [base, base], color=AXIS, lw=1)
note(ax, x18 - 330, 958, "Previous high: 5.2\n(Giannis, 2017-18)", size=23)
arrow(ax, (x18 - 92, 1016), (x18 - 6, y18), rad=-0.3)
note(ax, W - M - 46, 1000, "Biggest in 24\nseasons of data", size=23, ha="right")
swipe_cue(ax, y=1250, text="Swipe: can he keep it up?")
footer(fig, "Qualified: 70% of team games, 20+ MPG · Data: ESPN box scores")
save(fig, "slides/Luka_vs_NBA_1.png")
