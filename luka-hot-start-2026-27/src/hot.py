import pandas as pd, numpy as np
h = pd.read_parquet("data/hist_all.parquet")
h["pts"] = h.points.astype(float); h["date"] = pd.to_datetime(h.game_date)
h = h.sort_values(["season","athlete_id","date"])
h["gn"] = h.groupby(["season","athlete_id"]).cumcount() + 1
# team games per season
tg = h.groupby(["season","team_abbreviation"]).game_id.nunique().groupby("season").median()
s = h.groupby(["season","athlete_id"]).agg(name=("athlete_display_name","last"), gp=("game_id","nunique"), pts=("pts","sum"), mins=("minutes","sum")).reset_index()
s["ppg"] = s.pts/s.gp; s["team_g"] = s.season.map(tg)
f7 = h[h.gn <= 7].groupby(["season","athlete_id"]).agg(g7=("pts","size"), p7=("pts","mean"))
rest = h[h.gn > 7].groupby(["season","athlete_id"]).agg(gr=("pts","size"), pr=("pts","mean"))
s = s.join(f7, on=["season","athlete_id"]).join(rest, on=["season","athlete_id"])
# prior season ppg
prev = s[["season","athlete_id","ppg","gp"]].copy(); prev["season"] += 1; prev = prev.rename(columns={"ppg":"prev_ppg","gp":"prev_gp"})
s = s.merge(prev, on=["season","athlete_id"], how="left")
s.to_parquet("data/seasons.parquet")
# QA: scoring leaders by season (>=70% team games)
q = s[s.gp >= 0.7*s.team_g]
print(q.loc[q.groupby("season").ppg.idxmax(), ["season","name","gp","ppg"]].round(1).to_string(index=False))
