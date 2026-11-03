from common import *
import pandas as pd
p = pd.read_parquet("data/players2027.parquet"); q = p[(p.gp >= 0.7*p.team_gp) & (p.min_pg >= 20)].copy(); n = len(q)
q["fga_pg"] = q.fga/q.gp
L = q[q.name == "Luka Doncic"].iloc[0]
rows = [("pts_pg","Points per game", lambda v: f"{v:.1f}", None),
        ("ast_pg","Assists per game", lambda v: f"{v:.1f}", None),
        ("reb_pg","Rebounds per game", lambda v: f"{v:.1f}", None),
        ("pm_pg","Plus-minus per game", lambda v: f"{v:+.1f}", None),
        ("efg","Effective FG%", lambda v: f"{v*100:.1f}%", "#1 of 14 players with 18+ shots a game"),
        ("ts","True shooting %", lambda v: f"{v*100:.1f}%", None)]
fig, ax = setup("Luka vs NBA  ·  2/5", "The only player at 25-7-7,\nand he's at 38-8-8", f"Luka vs all {n} qualified players, per game, 2026-27")
rng = np.random.default_rng(3); xl, xr = 92, 988; y0, rh = 372, 148
for i, (c, lab, f, extra) in enumerate(rows):
    top = y0 + i*rh; cy = top + 74
    vals = q[c].values; lo, hi = np.percentile(vals, 0), vals.max()
    if c == "pm_pg": lo = max(lo, -20)
    if c in ("efg","ts"): lo = max(lo, 0.38)
    X = lambda v: xl + (np.clip(v, lo, hi) - lo)/(hi - lo)*(xr - xl)
    rank = int((q[c] > L[c]).sum() + 1)
    if i: ax.plot([M, W - M], [top - 20, top - 20], color=GRID, lw=1, zorder=0)
    note(ax, M, top, lab, size=25, weight=700)
    chip = f"#{rank} of {n}"
    tw = len(chip)*13.2 + 26
    pill(ax, W - M - tw, top - 4, tw, 36, r=10, z=1)
    ax.text(W - M - tw/2, top + 14, chip, fontsize=pt(22), fontweight=700, color=INK, ha="center", va="center", zorder=2)
    if extra: ax.text(W - M - tw - 14, top + 14, extra, fontsize=pt(21), color=INK2, ha="right", va="center", fontweight=600)
    ax.plot([xl, xr], [cy, cy], color=GRID, lw=1, zorder=1)
    jit = rng.uniform(-15, 15, len(vals))
    others = q.name.values != "Luka Doncic"
    ax.scatter([X(v) for v in vals[others]], cy + jit[others], s=34, c=NEUTRAL_DK, alpha=0.38, lw=0, zorder=2)
    med = np.median(vals); mx = X(med)
    ax.plot([mx, mx], [cy - 24, cy + 24], color=INK2, lw=2, zorder=3)
    ax.text(mx, cy + 30, f"NBA median {f(med)}", fontsize=pt(21), color=MUTED, ha="center", va="top")
    lx = X(L[c]); headshot(ax, LUKA, lx, cy, d=54, ring=LUKA_C, z=6)
    vlabel = f(L[c]); right = lx + 42
    if lx > 880: ax.text(lx - 42, cy - 4, vlabel, fontsize=pt(30), fontweight=700, color=LUKA_TXT, ha="right", va="center", zorder=8,
                         bbox=dict(boxstyle="round,pad=0.18", fc=SURFACE, ec="none"))
    else: ax.text(right, cy - 4, vlabel, fontsize=pt(30), fontweight=700, color=LUKA_TXT, ha="left", va="center", zorder=8, bbox=dict(boxstyle="round,pad=0.18", fc=SURFACE, ec="none"))
footer(fig, "Qualified: 70% of team games, 20+ MPG · thru Nov. 2 · ESPN")
save(fig, "slides/Luka_vs_NBA_2.png")
