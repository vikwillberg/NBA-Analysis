from common import *
import pandas as pd
g = pd.read_parquet("data/players2027.parquet"); q = g[(g.gp >= 0.7*g.team_gp) & (g.min_pg >= 20)].copy(); n = len(q)
top = q.sort_values("pm_pg", ascending=False).head(8).reset_index(drop=True)
L = q[q.name == "Luka Doncic"].iloc[0]
hist = pd.read_parquet("data/ts30_hist.parquet").head(5)
ids = {"Stephen Curry": 3975, "Shai Gilgeous-Alexander": 4278073, "Joel Embiid": 3059318, "Giannis Antetokounmpo": 3032977}
teams = {(2016,"Stephen Curry"): "GS", (2026,"Shai Gilgeous-Alexander"): "OKC", (2021,"Stephen Curry"): "GS", (2023,"Joel Embiid"): "PHI", (2024,"Giannis Antetokounmpo"): "MIL"}
league_ts = 0.5717693113795027
fig, ax = setup("Luka vs NBA  ·  3/5", "Winning his minutes by 16,\nat 68% true shooting", "Plus-minus and true shooting %, 2026-27 (thru Nov. 2)")
short = lambda s: s.replace("Shai Gilgeous-Alexander", "S. Gilgeous-Alexander").replace("Giannis Antetokounmpo", "G. Antetokounmpo").replace("Victor Wembanyama", "V. Wembanyama")
# ---- Panel A: plus-minus leaders
note(ax, M, 356, "Plus-minus per game, top 8", size=25, weight=700)
chip = f"Luka: #2 of {n}"; tw = len(chip)*13 + 28
pill(ax, W - M - tw, 352, tw, 36, r=10, z=1); ax.text(W - M - tw/2, 370, chip, fontsize=pt(22), fontweight=700, color=INK, ha="center", va="center", zorder=2)
x0, sc, y0, rh = 452, 25.0, 422, 43
for i, r in top.iterrows():
    cy = y0 + i*rh; me = r["name"] == "Luka Doncic"
    if me: pill(ax, M - 8, cy - 21, W - 2*M + 16, 42, z=0)
    ax.text(M + 18, cy, str(i+1), fontsize=pt(22), color=INK2 if me else MUTED, ha="right", va="center", fontweight=600)
    headshot(ax, int(r.pid), 116, cy, d=40, badge=r.team, ring=LUKA_C if me else None, ring_w=2.5)
    ax.text(148, cy, short(r["name"]), fontsize=pt(23), color=INK, ha="left", va="center", fontweight=700 if me else 500)
    hbar(ax, x0, cy, r.pm_pg*sc, 24 if me else 20, LUKA_C if me else NEUTRAL)
    ax.text(x0 + r.pm_pg*sc + 10, cy, f"+{r.pm_pg:.1f}", fontsize=pt(27 if me else 24), fontweight=700 if me else 600, color=LUKA_TXT if me else INK2, ha="left", va="center")
# on/off strip
yb = 778
ax.text(M, yb, "+21.7", fontsize=pt(56), fontweight=700, color=GOOD, ha="left", va="top")
note(ax, M + 196, yb + 8, "Lakers per 48 minutes\nwith Luka on the floor", size=22, weight=600, color=INK)
ax.text(548, yb, "-39.6", fontsize=pt(56), fontweight=700, color=BAD, ha="left", va="top")
note(ax, 548 + 186, yb + 8, "with him on the bench\n(86 min, small sample)", size=22, weight=600, color=INK)
ax.plot([M, W - M], [894, 894], color=GRID, lw=1)
# ---- Panel B: TS% vs the best 30-point seasons
note(ax, M, 914, "True shooting %: Luka now vs the best 30-PPG seasons", size=25, weight=700)
note(ax, M, 950, "Since 2002-03 (min. 50 games). His TS% is #1 among the 11 players scoring 25+ now", size=21, weight=400, color=MUTED)
rows = [("Luka 2026-27 (7 games)", L.ts, LUKA, "LAL", True)] + [(f"{short(r.athlete_display_name).replace('Stephen ', 'S. ')} {r.season-1}-{str(r.season)[2:]}", r.ts, ids[r.athlete_display_name], teams[(r.season, r.athlete_display_name)], False) for r in hist.itertuples()]
X = lambda v: 452 + (v - 0.55)/(0.70 - 0.55)*(940 - 452)
ya, rh2 = 1008, 44
lx = X(league_ts)
ax.plot([lx, lx], [ya - 26, ya + rh2*5 + 20], color=INK2, lw=2, zorder=1)
ax.text(lx, ya + rh2*5 + 24, f"NBA average {league_ts*100:.1f}%", fontsize=pt(21), color=INK2, ha="center", va="top", fontweight=600)
for i, (lab, v, pid, tm, me) in enumerate(rows):
    cy = ya + i*rh2
    if me: pill(ax, M - 8, cy - 21, W - 2*M + 16, 42, z=0)
    headshot(ax, int(pid), M + 22, cy, d=40, badge=tm, ring=LUKA_C if me else None, ring_w=2.5)
    ax.text(M + 56, cy, lab, fontsize=pt(22), color=INK, ha="left", va="center", fontweight=700 if me else 500)
    ax.plot([lx, X(v)], [cy, cy], color=LUKA_C if me else NEUTRAL, lw=6 if me else 5, solid_capstyle="round", zorder=2)
    ax.add_patch(Circle((X(v), cy), 10 if me else 8, fc=LUKA_C if me else NEUTRAL_DK, ec="white", lw=2, zorder=3))
    ax.text(X(v) + 18, cy, f"{v*100:.1f}%", fontsize=pt(26 if me else 23), fontweight=700 if me else 600, color=LUKA_TXT if me else INK2, ha="left", va="center")
footer(fig, "TS% = PTS / (2 x (FGA + 0.44 x FTA)) · on/off from box-score +/- · ESPN")
save(fig, "slides/Luka_vs_NBA_3.png")
