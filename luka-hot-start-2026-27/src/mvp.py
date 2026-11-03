import pandas as pd, numpy as np
h = pd.read_parquet("data/hist_all.parquet"); s = pd.read_parquet("data/seasons.parquet")
mvp = {2003:"Tim Duncan",2004:"Kevin Garnett",2005:"Steve Nash",2006:"Steve Nash",2007:"Dirk Nowitzki",2008:"Kobe Bryant",2009:"LeBron James",2010:"LeBron James",2011:"Derrick Rose",2012:"LeBron James",2013:"LeBron James",2014:"Kevin Durant",2015:"Stephen Curry",2016:"Stephen Curry",2017:"Russell Westbrook",2018:"James Harden",2019:"Giannis Antetokounmpo",2020:"Giannis Antetokounmpo",2021:"Nikola Jokic",2022:"Nikola Jokic",2023:"Joel Embiid",2024:"Nikola Jokic",2025:"Shai Gilgeous-Alexander",2026:"Shai Gilgeous-Alexander"}
tw = h.drop_duplicates(["game_id","team_abbreviation"]).groupby(["season","team_abbreviation"]).agg(w=("team_winner","sum"), g=("game_id","nunique")).reset_index()
rows = []
for yr, n in mvp.items():
    x = h[(h.season==yr)&(h.athlete_display_name==n)]
    assert len(x), (yr, n)
    team = x.team_abbreviation.mode()[0]; t = tw[(tw.season==yr)&(tw.team_abbreviation==team)].iloc[0]
    rows.append(dict(season=yr, name=n, team=team, gp=x.game_id.nunique(), ppg=x.points.mean(), apg=x.assists.mean(), rpg=x.rebounds.mean(), team_w=t.w, team_g=t.g, wpct=t.w/t.g, pid=x.athlete_id.iloc[0]))
m = pd.DataFrame(rows); m["w82"] = m.wpct*82
print(m.round(3).to_string(index=False))
print("avg ppg %.1f  avg wins82 %.1f  min wins82 %.1f  min gp %d  avg gp %.1f" % (m.ppg.mean(), m.w82.mean(), m.w82.min(), m.gp.min(), m.gp.mean()))
print("MVPs with team win% < 46.5/82 (.567):", (m.wpct < 46.5/82).sum(), m[m.wpct < .6][["season","name","w82"]])
m.to_parquet("data/mvp_hist.parquet")
