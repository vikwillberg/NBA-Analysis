import pandas as pd, numpy as np
g = pd.read_parquet("data/players2027.parquet"); q = g[(g.gp >= 0.7*g.team_gp) & (g.min_pg >= 20)].copy()
print(q.sort_values("pm_pg", ascending=False).head(10)[["name","pid","team","gp","pm_pg","min_pg"]].round(2).to_string())
s = q[q.pts_pg >= 20].sort_values("ts", ascending=False); print(s[["name","team","pts_pg","ts","efg"]].head(10).round(3).to_string())
print("TS rank among 25+:", (q[q.pts_pg>=25].ts > q[q.name=="Luka Doncic"].ts.iloc[0]).sum()+1, "of", (q.pts_pg>=25).sum())
# on/off
p = pd.read_parquet("data/box2027.parquet"); t = pd.read_parquet("data/team2027.parquet")
lg = p[p.name=="Luka Doncic"]; gids = set(lg.game_id)
lal = p[(p.team=="LAL") & p.game_id.isin(gids)]
tm = lal.groupby("game_id")["min"].sum()/5; print("team game minutes", tm.to_dict())
tt = t[(t.team=="LAL") & t.game_id.isin(gids)]; diff = (tt.pf - tt.pa).sum()
on_min = lg["min"].sum(); on = lg.pm.sum(); off_min = tm.sum() - on_min; off = diff - on
print("on min", on_min, "on +/-", on, "per48 %.1f" % (on/on_min*48), "off min", off_min, "off", off, "per48 %.1f" % (off/off_min*48), "team diff", diff)
# historical TS for 30+ PPG seasons
h = pd.read_parquet("data/hist_all.parquet")
a = h.groupby(["season","athlete_id","athlete_display_name"]).agg(gp=("game_id","nunique"), pts=("points","sum"), fga=("field_goals_attempted","sum"), fta=("free_throws_attempted","sum")).reset_index()
a["ppg"] = a.pts/a.gp; a["ts"] = a.pts/(2*(a.fga+0.44*a.fta))
x = a[(a.ppg >= 30) & (a.gp >= 50)].sort_values("ts", ascending=False); print(len(x)); print(x.head(8)[["season","athlete_display_name","ppg","ts","gp"]].round(3).to_string())
x.to_parquet("data/ts30_hist.parquet")
# league TS
print("league TS", p.pts.sum()/(2*(p.fga.sum()+0.44*p.fta.sum())))
