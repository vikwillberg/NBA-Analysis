from common import *
import pandas as pd, json
z = pd.read_parquet("data/hot_model.parquet"); s = pd.read_parquet("data/seasons.parquet")
x_all = s[(s.g7 == 7) & (s.gr >= 30) & (s.p7 >= 25)]
pj = json.load(open("data/proj.json")); mu = pj["mu"]; lo_r, hi_r = mu + pj["loo_p10"], mu + pj["loo_p90"]
G = pj["G"]; season = (268 + mu*(G-7))/G; s_lo = (268 + lo_r*(G-7))/G; s_hi = (268 + hi_r*(G-7))/G
fig, ax = setup("Luka vs NBA  ·  4/5", "History says he cools off,\nbut only to about 33 a game", "216 hot starts since 2002-03: first 7 games vs the rest")
X0, X1, Y0, Y1 = 150, 905, 1190, 392; xa, xb, ya, yb = 25, 40, 12, 40
X = lambda v: X0 + (v - xa)/(xb - xa)*(X1 - X0); Y = lambda v: Y0 - (v - ya)/(yb - ya)*(Y0 - Y1)
for v in range(15, 41, 5):
    ax.plot([X0, X1 + 20], [Y(v)]*2, color=GRID, lw=1, zorder=0); ax.text(X0 - 14, Y(v), str(v), fontsize=pt(21), color=MUTED, ha="right", va="center")
for v in range(25, 41, 5):
    ax.plot([X(v)]*2, [Y0, Y1], color=GRID, lw=1, zorder=0); ax.text(X(v), Y0 + 14, str(v), fontsize=pt(21), color=MUTED, ha="center", va="top")
ax.plot([X0, X1 + 20], [Y0, Y0], color=AXIS, lw=1)
ax.text(X0 + (X1 - X0)/2, Y0 + 46, "Points per game, first 7 games", fontsize=pt(22), color=INK2, ha="center", va="top", fontweight=600)
ax.text(76, Y(28), "Points per game, rest of season", fontsize=pt(22), color=INK2, ha="center", va="center", rotation=90, fontweight=600)
# lines
ax.plot([X(25), X(39.6)], [Y(25), Y(39.6)], color=INK, lw=2.5, zorder=3, solid_capstyle="round")
ang = np.degrees(np.arctan((Y(25) - Y(40))/(X(40) - X(25))))
ax.text(X(25.5), Y(25.5) - 12, "Kept the hot start", fontsize=pt(22), color=INK, rotation=ang, ha="left", va="bottom", fontweight=600, rotation_mode="anchor", bbox=dict(boxstyle="round,pad=0.15", fc=SURFACE, ec="none", alpha=0.9), zorder=5)
b1, b0 = np.polyfit(x_all.p7, x_all.pr, 1)
ax.plot([X(25), X(39)], [Y(b0 + b1*25), Y(b0 + b1*39)], color=NEUTRAL_DK, lw=4, zorder=3, solid_capstyle="round")
ang2 = np.degrees(np.arctan((Y(b0+b1*25) - Y(b0+b1*40))/(X(40) - X(25))))
ax.text(X(26.0), Y(b0 + b1*26.0) + 14, "Typical hot start", fontsize=pt(22), color=INK2, rotation=ang2, ha="left", va="top", fontweight=600, rotation_mode="anchor", zorder=5, bbox=dict(boxstyle="round,pad=0.15", fc=SURFACE, ec="none", alpha=0.9))
oth = x_all[~x_all.name.str.contains("Luka Don")]
ax.scatter([X(v) for v in oth.p7], [Y(v) for v in oth.pr], s=60, c=NEUTRAL_DK, alpha=0.42, lw=0, zorder=2)
lk = x_all[x_all.name.str.contains("Luka Don") & (x_all.p7 >= 36)]
lg = x_all[x_all.name.str.contains("Luka Don") & (x_all.p7 < 36)]
ax.scatter([X(v) for v in lg.p7], [Y(v) for v in lg.pr], s=60, c=NEUTRAL_DK, alpha=0.42, lw=0, zorder=2)
for _, r in lk.iterrows():
    ax.scatter([X(r.p7)], [Y(r.pr)], s=150, c=LUKA_C, lw=2, edgecolors="white", zorder=6)
    ax.text(X(r.p7) - 14, Y(r.pr) + 2, f"Luka {r.season-1}-{str(r.season)[2:]}: {r.p7:.1f} to {r.pr:.1f}", fontsize=pt(21), color=INK2, ha="right", va="center", fontweight=600, zorder=7,
            bbox=dict(boxstyle="round,pad=0.15", fc=SURFACE, ec="none", alpha=0.85))
h = x_all[(x_all.name == "James Harden") & (x_all.season == 2020)].iloc[0]
ax.scatter([X(h.p7)], [Y(h.pr)], s=70, c=INK2, lw=0, zorder=5)
ax.text(X(h.p7) - 14, Y(h.pr), "Harden 2019-20", fontsize=pt(21), color=INK2, ha="right", va="center", fontweight=600, zorder=7, bbox=dict(boxstyle="round,pad=0.15", fc=SURFACE, ec="none", alpha=0.9))
# projection
px = X(268/7)
ax.add_patch(FancyBboxPatch((px - 9, Y(hi_r)), 18, Y(lo_r) - Y(hi_r), boxstyle="round,pad=0,rounding_size=9", fc=LUKA_TINT, ec=LUKA_C, lw=1.6, zorder=7))
ax.scatter([px], [Y(mu)], s=230, c=LUKA_C, lw=2.5, edgecolors="white", zorder=9)
ax.plot([px + 12, 940], [Y(mu), Y(mu)], color=LUKA_C, lw=1.5, zorder=8)
headshot(ax, LUKA, 966, Y(mu), d=60, ring=LUKA_C, z=10)
ax.text(966, Y(mu) + 40, "First 7\ngames:\n38.3", fontsize=pt(21), color=INK, ha="center", va="top", fontweight=700, linespacing=1.1)
ax.text(px, Y(hi_r) - 10, f"{hi_r:.0f}", fontsize=pt(21), color=MUTED, ha="center", va="bottom"); ax.text(px, Y(lo_r) + 10, f"{lo_r:.0f}", fontsize=pt(21), color=MUTED, ha="center", va="top")
# hero callout (empty lower-right)
hx = 600
ax.text(hx, 925, f"{mu:.1f}", fontsize=pt(76), fontweight=700, color=LUKA_C, ha="left", va="top")
note(ax, hx + 2, 1019, "projected the rest of the way", size=26, weight=700)
note(ax, hx + 2, 1056, f"Season average about {season:.1f}\n80% range: {lo_r:.0f} to {hi_r:.0f}\nOdds he stays at 38+: about 1 in 40", size=22, weight=400, color=INK2)
arrow(ax, (hx + 300, 935), (px - 6, Y(lo_r) + 40), rad=0.2, color=LUKA_C)
footer(fig, "Model: first 7 games + last season's PPG (avg miss 2.2) · ESPN")
save(fig, "slides/Luka_vs_NBA_4.png")
print(season, s_lo, s_hi, lo_r, hi_r)
