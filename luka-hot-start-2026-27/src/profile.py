import pandas as pd, numpy as np
g = pd.read_parquet("data/players2027.parquet")
q = g[(g.gp >= 0.7*g.team_gp) & (g.min_pg >= 20)].copy()
stats = {"pts_pg":"PTS","ast_pg":"AST","reb_pg":"REB","efg":"eFG","ts":"TS","pm_pg":"+/-","tov_pg":"TOV"}
L = q[q.name=="Luka Doncic"].iloc[0]
for c,lab in stats.items():
    r = (q[c] > L[c]).sum()+1; print(lab, round(L[c],3), "rank", r, "of", len(q), "pctile", round((q[c] < L[c]).mean()*100,1), "median", round(q[c].median(),3), "max other", q[q.name!="Luka Doncic"].sort_values(c, ascending=False).iloc[0][["name",c]].tolist())
print("30/7/7:", q[(q.pts_pg>=25)&(q.reb_pg>=7)&(q.ast_pg>=7)][["name","pts_pg","reb_pg","ast_pg"]])
# eFG among high-volume (>=20 FGA/g)
q["fga_pg"] = q.fga/q.gp; v = q[q.fga_pg>=18].sort_values("efg", ascending=False); print("eFG among 18+ FGA:", len(v)); print(v[["name","fga_pg","efg","ts"]].head(8).round(3))
print(q[q.name.str.contains("Jok|Wemb|Gilgeous|Tatum|Maxey")][["name","gp","team_gp","pts_pg","reb_pg","ast_pg","efg","pm_pg"]].round(3))
print(g[g.name.str.contains("Jok")][["name","gp","team","pts_pg"]])
# Luka on/off proxy: Lakers record with/without
t = pd.read_parquet("data/team2027.parquet"); p = pd.read_parquet("data/box2027.parquet")
lg = set(p[p.name=="Luka Doncic"].game_id); lt = t[t.team=="LAL"].copy(); lt["luka"] = lt.game_id.isin(lg)
print(lt[["date","opp","pf","pa","win","luka"]].sort_values("date"))
# league avg eFG
tot = p[["fgm","tpm","fga"]].sum(); print("league eFG", (tot.fgm+0.5*tot.tpm)/tot.fga, "league TS", p.pts.sum()/(2*(p.fga.sum()+0.44*p.fta.sum())))
