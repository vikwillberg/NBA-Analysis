from common import *
import pandas as pd
open_odds = {"Victor Wembanyama":205,"Shai Gilgeous-Alexander":380,"Luka Doncic":475,"Nikola Jokic":650,"Jayson Tatum":1200,"Giannis Antetokounmpo":1400,"Anthony Edwards":1600,"Cade Cunningham":3000,"Jalen Brunson":5000,"Tyrese Maxey":9000,"Jaylen Brown":9000,"Donovan Mitchell":10000,"Tyrese Haliburton":12000,"Devin Booker":15000,"Stephen Curry":17000,"Kawhi Leonard":17000,"Kevin Durant":20000,"Joel Embiid":20000,"Paolo Banchero":25000,"Cooper Flagg":25000}
imp = {k: 100/(v+100) for k, v in open_odds.items()}; tot = sum(imp.values()); opn = {k: v/tot*100 for k, v in imp.items()}
now = {"Luka Doncic":38,"Victor Wembanyama":30,"Shai Gilgeous-Alexander":15,"Jayson Tatum":9,"Nikola Jokic":6,"Tyrese Maxey":5,"Giannis Antetokounmpo":4,"Cooper Flagg":3}
heads = pd.read_csv("data/heads.csv").set_index("name")
df = pd.DataFrame([dict(name=k, now=v, open=opn[k], pid=heads.loc[k,"pid"], team=heads.loc[k,"team"]) for k, v in now.items()])
df.to_csv("data/mvp_market.csv", index=False); print(df.round(1), "vig total", round(tot,3))
fig, ax = setup("Luka vs NBA  ·  5/5", "From 3rd choice to the\nMVP favorite in two weeks", "Chance to win MVP: opening-night odds vs today's market")
xa, xb = 438, 948; X = lambda v: xa + v/40*(xb - xa)
ly = 372
ax.add_patch(Circle((M + 10, ly), 9, fc=SURFACE, ec=INK2, lw=2.5)); ax.text(M + 28, ly, "Opening night (Oct. 20)", fontsize=pt(22), color=INK2, va="center")
ax.add_patch(Circle((M + 340, ly), 10, fc=INK2, ec="none")); ax.text(M + 358, ly, "Now (Nov. 3)", fontsize=pt(22), color=INK2, va="center")
for v in (0, 10, 20, 30, 40):
    ax.plot([X(v)]*2, [410, 966], color=GRID, lw=1, zorder=0); ax.text(X(v), 972, f"{v}%", fontsize=pt(21), color=MUTED, ha="center", va="top")
y0, rh = 444, 72
for i, r in df.iterrows():
    cy = y0 + i*rh; me = r["name"] == "Luka Doncic"
    if me: pill(ax, M - 8, cy - 31, W - 2*M + 16, 62, z=0)
    headshot(ax, int(r.pid), M + 28, cy, d=50, badge=r.team, ring=LUKA_C if me else None, ring_w=2.5)
    nm = r["name"].replace("Shai Gilgeous-Alexander", "S. Gilgeous-Alex.").replace("Giannis Antetokounmpo", "G. Antetokounmpo").replace("Victor Wembanyama", "V. Wembanyama")
    ax.text(M + 66, cy, nm, fontsize=pt(23), color=INK, va="center", fontweight=700 if me else 500)
    c = LUKA_C if me else NEUTRAL_DK
    ax.plot([X(r.open), X(r.now)], [cy, cy], color=LUKA_C if me else NEUTRAL, lw=5 if me else 4, solid_capstyle="round", zorder=2)
    ax.add_patch(Circle((X(r.open), cy), 9, fc=SURFACE, ec=c, lw=2.5, zorder=3))
    ax.add_patch(Circle((X(r.now), cy), 12 if me else 10, fc=LUKA_C if me else INK2, ec="white", lw=2, zorder=4))
    up = r.now >= r.open; lo_x, hi_x = sorted([X(r.open), X(r.now)])
    nl = f"{r.now:.0f}%"; ol = f"{r.open:.0f}%" if r.open >= 1 else "<1%"
    ax.text(hi_x + 18, cy, nl if up else ol, fontsize=pt(27 if (me and up) else 23), fontweight=700 if up else 400, color=(LUKA_TXT if me else INK) if up else MUTED, va="center")
    ax.text(lo_x - 18, cy, ol if up else nl, fontsize=pt(23), fontweight=400 if up else 700, color=MUTED if up else INK, va="center", ha="right")
# what he still needs
ax.plot([M, W - M], [1030, 1030], color=GRID, lw=1)
note(ax, M, 1050, "What he still needs", size=25, weight=700)
cols = [("65", "games played", "Award minimum. He's\nplayed 7 of 8 so far"), ("47+", "team wins", "No MVP since 2002-03\nwon fewer. Lakers: 6-2"), ("33.5", "projected PPG", "Most by an MVP since\nJordan's 35.0 in 1987-88")]
cw = (W - 2*M)/3
for k, (big, lab, sub) in enumerate(cols):
    x = M + k*cw
    ax.text(x, 1092, big, fontsize=pt(58), fontweight=700, color=LUKA_C, ha="left", va="top")
    ax.text(x + (len(big.replace('.', ''))*36 + (14 if '.' in big else 0) + 12), 1106, lab, fontsize=pt(22), fontweight=700, color=INK, ha="left", va="top")
    ax.text(x, 1176, sub, fontsize=pt(21), color=INK2, ha="left", va="top", linespacing=1.25)
footer(fig, "Opening: DraftKings via ESPN, vig removed · Now: Kalshi")
save(fig, "slides/Luka_vs_NBA_5.png")
