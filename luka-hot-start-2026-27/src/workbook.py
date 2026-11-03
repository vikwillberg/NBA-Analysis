import pandas as pd, numpy as np, json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as CL
BLUE, BLACK, GREEN = Font(color="0000FF"), Font(color="000000"), Font(color="008000")
B = Font(bold=True); HDR = PatternFill("solid", fgColor="E3DCEC")
wb = Workbook()
def sheet(name, df, start=1):
    ws = wb.create_sheet(name)
    for j, c in enumerate(df.columns, 1):
        x = ws.cell(start, j, c); x.font = B; x.fill = HDR
    for i, row in enumerate(df.itertuples(index=False), start + 1):
        for j, v in enumerate(row, 1):
            v = v.item() if hasattr(v, "item") else v
            if isinstance(v, float) and np.isnan(v): v = None
            ws.cell(i, j, v).font = BLUE
    for j in range(1, len(df.columns) + 1): ws.column_dimensions[CL(j)].width = 16
    return ws
# README
ws = wb.active; ws.title = "README"
lines = ["Luka vs NBA: 2026-27 hot start (LinkedIn carousel, 5 slides) · Viktor Berg · built Nov. 3, 2026",
 "Color code: blue = hardcoded input, black = formula, green = cross-sheet link.",
 "SOURCES: ESPN box scores via site.api.espn.com (2026-27, games through Nov. 2, 107 games, all completed);",
 "  sportsdataverse ESPN player box scores 2002-03 to 2025-26 (All-Star games and NBA Cup finals removed);",
 "  MVP odds: opening night = DraftKings via ESPN (Oct. 20, 2026), now = Kalshi market (Nov. 3, 2026). Lakers win total 46.5 (Fanatics, Oct. 21).",
 "QUALIFIED PLAYER: played 70%+ of his team's games and 20+ minutes per game (190 players).",
 "SLIDE 1: points per game leaders; gap No.1 - No.2 at the same point (opening day + 13 days) in every season since 2002-03.",
 "SLIDE 2: Luka's rank among qualified players. eFG% = (FGM + 0.5*3PM)/FGA; TS% = PTS/(2*(FGA+0.44*FTA)).",
 "SLIDE 3: plus-minus per game leaders; Lakers net per 48 with Luka on/off (on-court minutes and +/- from box scores; off = team margin - on); TS% vs every 30+ PPG season since 2002-03 (50+ games).",
 "SLIDE 4: 216 player-seasons with 25+ PPG in their first 7 games and 30+ games after. Model: rest-of-season PPG = a + b*first7 + c*prior-season PPG",
 "  (n=197 with a 40+ game prior season). Leave-one-out avg miss 2.2 PPG (RMSE 2.8), vs 3.1 for 'keeps the hot start'. 80% range from LOO residuals.",
 "  Season average assumes 70 games (65 or 75 changes it by under 0.1).",
 "SLIDE 5: opening odds converted to implied probability and normalized over the 20 listed players (vig ~17%).",
 "QA: scoring champions 2002-03..2025-26 reproduced from the box scores (e.g., Harden 36.1 in 2018-19, Luka 33.9 in 2023-24, SGA 32.7 in 2024-25);",
 "  Luka's 7 games sum to 268 pts = 38.3 PPG (matches public reporting); team game counts 5-8 per team, no duplicate game ids.",
 "CAVEATS: 7-game samples are noisy; plus-minus is lineup-dependent; early seasons (2002-04) miss a few games in the source data;",
 "  prediction-market prices move daily; the 65-game award rule can be appealed (Luka was granted eligibility in 2025-26 at 64 games)."]
for i, t in enumerate(lines, 1): ws.cell(i, 1, t)
ws.column_dimensions["A"].width = 150
# Luka game log
p = pd.read_parquet("data/box2027.parquet"); L = p[p.name == "Luka Doncic"].sort_values("date")[["date","opp","win","min","pts","reb","ast","fgm","fga","tpm","tpa","ftm","fta","tov","pm"]]
ws = sheet("Luka_GameLog", L); n = len(L) + 1; r = n + 2
ws.cell(r, 1, "Per game").font = B
for j, c in enumerate(L.columns, 1):
    if j >= 4: ws.cell(r, j, f"=AVERAGE({CL(j)}2:{CL(j)}{n})").font = BLACK
ws.cell(r+2, 1, "eFG%"); ws.cell(r+2, 2, f"=(SUM(H2:H{n})+0.5*SUM(J2:J{n}))/SUM(I2:I{n})")
ws.cell(r+3, 1, "TS%"); ws.cell(r+3, 2, f"=SUM(E2:E{n})/(2*(SUM(I2:I{n})+0.44*SUM(M2:M{n})))")
ws.cell(r+4, 1, "Lakers record in his games"); ws.cell(r+4, 2, f'=COUNTIF(C2:C{n},TRUE)&"-"&COUNTIF(C2:C{n},FALSE)')
# Slide 1
g = pd.read_parquet("data/players2027.parquet"); q = g[(g.gp >= 0.7*g.team_gp) & (g.min_pg >= 20)].sort_values("pts_pg", ascending=False)
top = q.head(10)[["name","team","gp","pts"]].copy()
ws = sheet("S1_Scorers", top); ws.cell(1, 5, "PPG").font = B
for i in range(2, 12): ws.cell(i, 5, f"=D{i}/C{i}").font = BLACK
ws.cell(13, 1, "Gap No.1 - No.2").font = B; ws.cell(13, 5, "=E2-E3")
gh = pd.read_parquet("data/gap_hist.parquet")[["season","leader","p1","second","p2","champ","champ_ppg"]].copy()
gh["season"] = gh.season.map(lambda s: f"{s-1}-{str(s)[2:]}")
gh = pd.concat([gh, pd.DataFrame([dict(season="2026-27", leader="Luka Doncic", p1=q.pts_pg.iloc[0], second="Stephen Curry", p2=q.pts_pg.iloc[1], champ=None, champ_ppg=None)])])
ws = sheet("S1_GapHistory", gh); k = len(gh) + 1; ws.cell(1, 8, "gap").font = B
for i in range(2, k + 1): ws.cell(i, 8, f"=C{i}-E{i}").font = BLACK
ws.cell(k+2, 1, "Average gap 2002-03..2025-26"); ws.cell(k+2, 8, f"=AVERAGE(H2:H{k-1})")
ws.cell(k+3, 1, "Previous high"); ws.cell(k+3, 8, f"=MAX(H2:H{k-1})")
ws.cell(k+4, 1, "Early leader won scoring title (share)"); ws.cell(k+4, 8, f"=SUMPRODUCT((B2:B{k-1}=F2:F{k-1})*1)/{k-2}")
# Slide 2
q2 = q[["name","team","gp","min_pg","pts_pg","ast_pg","reb_pg","pm_pg","efg","ts"]].copy()
q2["fga_pg"] = (q.fga/q.gp).values
ws = sheet("S2_Qualified", q2, start=6); last = 6 + len(q2)
li = 7 + list(q2.name).index("Luka Doncic")
ws.cell(1, 1, "Luka rank among qualified players").font = B
for j, (c, col) in enumerate([("PTS","E"),("AST","F"),("REB","G"),("+/-","H"),("eFG","I"),("TS","J")], 2):
    ws.cell(2, j, c).font = B
    ws.cell(3, j, f"=RANK({col}{li},{col}7:{col}{last},0)").font = BLACK
    ws.cell(4, j, f"=MEDIAN({col}7:{col}{last})").font = BLACK
ws.cell(3, 1, "Rank"); ws.cell(4, 1, "League median")
ws.cell(2, 9, "Players 25-7-7").font = B; ws.cell(3, 9, f"=COUNTIFS(E7:E{last},\">=25\",G7:G{last},\">=7\",F7:F{last},\">=7\")")
ws.cell(2, 10, "eFG rank, 18+ FGA").font = B; ws.cell(3, 10, f"=COUNTIFS(K7:K{last},\">=18\",I7:I{last},\">\"&I{li})+1")
ws.cell(2, 11, "of").font = B; ws.cell(3, 11, f"=COUNTIF(K7:K{last},\">=18\")")

# Slide 3: plus-minus and TS
pm = q.sort_values("pm_pg", ascending=False)[["name","team","gp","pm"]].head(10).copy()
ws = sheet("S3_PlusMinus", pm); ws.cell(1, 5, "+/- per game").font = B
for i in range(2, 12): ws.cell(i, 5, f"=D{i}/C{i}").font = BLACK
bl = pd.read_parquet("data/box2027.parquet"); lk = bl[bl.name == "Luka Doncic"]; gids = set(lk.game_id)
tb = pd.read_parquet("data/team2027.parquet"); tt = tb[(tb.team == "LAL") & tb.game_id.isin(gids)]
lal = bl[(bl.team == "LAL") & bl.game_id.isin(gids)]; tmin = float(lal["min"].sum()/5)
r0 = 14
for k, (a, v) in enumerate([("Luka minutes", float(lk["min"].sum())), ("Luka on-court +/-", int(lk.pm.sum())), ("Lakers game minutes (his 7 games)", tmin), ("Lakers margin (his 7 games)", int((tt.pf - tt.pa).sum()))]):
    ws.cell(r0 + k, 1, a); ws.cell(r0 + k, 2, v).font = BLUE
for k, (a, f) in enumerate([("On: net per 48", f"=B{r0+1}/B{r0}*48"), ("Off minutes", f"=B{r0+2}-B{r0}"), ("Off +/-", f"=B{r0+3}-B{r0+1}"), ("Off: net per 48", f"=B{r0+6}/B{r0+5}*48")], 4):
    ws.cell(r0 + k, 1, a); ws.cell(r0 + k, 2, f).font = BLACK
ts = pd.read_parquet("data/ts30_hist.parquet")[["season","athlete_display_name","gp","pts","fga","fta"]].copy(); ts["season"] = ts.season.map(lambda s: f"{s-1}-{str(s)[2:]}")
Lr = g[g.name == "Luka Doncic"].iloc[0]
ts = pd.concat([pd.DataFrame([dict(season="2026-27 (7 g)", athlete_display_name="Luka Doncic", gp=int(Lr.gp), pts=float(Lr.pts), fga=float(Lr.fga), fta=float(Lr.fta))]), ts])
ws = sheet("S3_TS_30PPG", ts); n2 = len(ts) + 1; ws.cell(1, 7, "PPG").font = B; ws.cell(1, 8, "TS%").font = B
for i in range(2, n2 + 1): ws.cell(i, 7, f"=D{i}/C{i}").font = BLACK; ws.cell(i, 8, f"=D{i}/(2*(E{i}+0.44*F{i}))").font = BLACK
ws.cell(n2 + 2, 1, "Best TS% of a 30+ PPG season since 2002-03 (50+ g)"); ws.cell(n2 + 2, 8, f"=MAX(H3:H{n2})")
ws.cell(n2 + 3, 1, "Luka TS% rank among players scoring 25+ now"); ws.cell(n2 + 3, 8, f'=COUNTIFS(S2_Qualified!E7:E196,">=25",S2_Qualified!J7:J196,">"&H2)+1').font = GREEN
ws.cell(n2 + 4, 1, "League TS% (all players, 2026-27)"); ws.cell(n2 + 4, 8, round(float(bl.pts.sum()/(2*(bl.fga.sum()+0.44*bl.fta.sum()))), 4)).font = BLUE
# Slide 4
z = pd.read_parquet("data/hot_model.parquet")[["season","name","p7","pr","prev_ppg","gp","loo"]].copy(); z["season"] = z.season.map(lambda s: f"{s-1}-{str(s)[2:]}")
pj = json.load(open("data/proj.json"))
ws = sheet("S4_HotStarts", z, start=12); last = 12 + len(z)
lab = ["Intercept a", "b (first 7 PPG)", "c (prior-season PPG)", "Luka first 7 PPG", "Luka 2025-26 PPG", "Games assumed", "Projected rest of season", "Projected season avg", "LOO 10th pct", "LOO 90th pct", "Range low / high (rest)"]
vals = [pj["coef"][0], pj["coef"][1], pj["coef"][2], "=268/7", 33.5, 70, "=B1+B2*B4+B3*B5", "=(268+B7*(B6-7))/B6", f"=PERCENTILE(G13:G{last},0.1)", f"=PERCENTILE(G13:G{last},0.9)", "=B7+B9"]
for i, (a, v) in enumerate(zip(lab, vals), 1):
    ws.cell(i, 1, a); c = ws.cell(i, 2, v); c.font = BLACK if isinstance(v, str) else BLUE
ws.cell(11, 3, "=B7+B10").font = BLACK
ws.cell(1, 4, "LOO mean abs error"); ws.cell(1, 5, f"=SUMPRODUCT(ABS(G13:G{last}))/COUNT(G13:G{last})")
ws.cell(2, 4, "P(season >= 38.3)"); ws.cell(2, 5, f"=COUNTIF(G13:G{last},\">=\"&((38.3*B6-268)/(B6-7)-B7))/COUNT(G13:G{last})")
ws.cell(3, 4, "P(season >= 30)"); ws.cell(3, 5, f"=COUNTIF(G13:G{last},\">=\"&((30*B6-268)/(B6-7)-B7))/COUNT(G13:G{last})")
s_all = pd.read_parquet("data/seasons.parquet"); xa = s_all[(s_all.g7 == 7) & (s_all.gr >= 30) & (s_all.p7 >= 25)][["season","name","p7","pr"]].copy()
xa["season"] = xa.season.map(lambda s: f"{s-1}-{str(s)[2:]}"); sheet("S4_AllHotStarts_216", xa)
# Slide 4
mk = pd.read_csv("data/mvp_market.csv")
odds = {"Victor Wembanyama":205,"Shai Gilgeous-Alexander":380,"Luka Doncic":475,"Nikola Jokic":650,"Jayson Tatum":1200,"Giannis Antetokounmpo":1400,"Anthony Edwards":1600,"Cade Cunningham":3000,"Jalen Brunson":5000,"Tyrese Maxey":9000,"Jaylen Brown":9000,"Donovan Mitchell":10000,"Tyrese Haliburton":12000,"Devin Booker":15000,"Stephen Curry":17000,"Kawhi Leonard":17000,"Kevin Durant":20000,"Joel Embiid":20000,"Paolo Banchero":25000,"Cooper Flagg":25000}
nowd = dict(zip(mk.name, mk.now))
od = pd.DataFrame([dict(player=k, opening_american=v, kalshi_now_pct=nowd.get(k)) for k, v in odds.items()])
ws = sheet("S5_MVPMarket", od); n = len(od) + 1
ws.cell(1, 4, "implied").font = B; ws.cell(1, 5, "opening % (no vig)").font = B
for i in range(2, n + 1):
    ws.cell(i, 4, f"=100/(B{i}+100)").font = BLACK; ws.cell(i, 5, f"=D{i}/SUM($D$2:$D${n})*100").font = BLACK
ws.cell(n+2, 1, "Book overround"); ws.cell(n+2, 4, f"=SUM(D2:D{n})")
mh = pd.read_parquet("data/mvp_hist.parquet")[["season","name","team","gp","ppg","apg","rpg","team_w","team_g"]].copy(); mh["season"] = mh.season.map(lambda s: f"{s-1}-{str(s)[2:]}")
ws = sheet("S5_MVPHistory", mh); n = len(mh) + 1; ws.cell(1, 10, "wins per 82").font = B
for i in range(2, n + 1): ws.cell(i, 10, f"=H{i}/I{i}*82").font = BLACK
ws.cell(n+2, 1, "Fewest wins per 82"); ws.cell(n+2, 10, f"=MIN(J2:J{n})")
ws.cell(n+3, 1, "Highest MVP PPG since 2002-03"); ws.cell(n+3, 5, f"=MAX(E2:E{n})")
ws.cell(n+4, 1, "Fewest games by an MVP"); ws.cell(n+4, 4, f"=MIN(D2:D{n})")
ws.cell(n+5, 1, "Link: Luka projected season avg"); c = ws.cell(n+5, 5, "=S4_HotStarts!B8"); c.font = GREEN
wb.save("data/Luka_vs_NBA_data.xlsx")
