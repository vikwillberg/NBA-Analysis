import pandas as pd
p = pd.read_parquet("data/box2027.parquet"); t = pd.read_parquet("data/team2027.parquet")
g = p.groupby(["pid","name"]).agg(team=("team","last"), gp=("game_id","nunique"), min=("min","sum"), pts=("pts","sum"), reb=("reb","sum"), ast=("ast","sum"), fgm=("fgm","sum"), fga=("fga","sum"), tpm=("tpm","sum"), tpa=("tpa","sum"), ftm=("ftm","sum"), fta=("fta","sum"), tov=("tov","sum"), pm=("pm","sum"), stl=("stl","sum"), blk=("blk","sum")).reset_index()
tg = t.groupby("team").size()
g["team_gp"] = g.team.map(tg)
for c in ["min","pts","reb","ast","pm","tov","stl","blk"]: g[c+"_pg"] = g[c]/g.gp
g["efg"] = (g.fgm + 0.5*g.tpm)/g.fga; g["ts"] = g.pts/(2*(g.fga+0.44*g.fta))
q = g[(g.gp >= 0.7*g.team_gp) & (g.min_pg >= 20)].copy()
print(len(q), "qualified")
print(q.sort_values("pts_pg", ascending=False).head(20)[["name","team","gp","min_pg","pts_pg","reb_pg","ast_pg","efg","ts","pm_pg"]].round(3).to_string())
rec = t.groupby("team").agg(w=("win","sum"), gp=("win","size"), pf=("pf","mean"), pa=("pa","mean")); rec["diff"]=rec.pf-rec.pa
print(rec.sort_values("diff", ascending=False).round(1).to_string())
g.to_parquet("data/players2027.parquet")
