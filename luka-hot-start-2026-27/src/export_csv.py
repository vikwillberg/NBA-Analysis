"""Write the analysis tables as plain CSVs (committed to the repo)."""
import pandas as pd, json
g = pd.read_parquet("data/players2027.parquet"); q = g[(g.gp >= 0.7*g.team_gp) & (g.min_pg >= 20)]
p = pd.read_parquet("data/box2027.parquet")
p[p.name == "Luka Doncic"].sort_values("date")[["date","opp","win","min","pts","reb","ast","fgm","fga","tpm","tpa","ftm","fta","tov","pm"]].to_csv("data/luka_game_log_2026_27.csv", index=False)
q.drop(columns=["pid"]).sort_values("pts_pg", ascending=False).round(4).to_csv("data/qualified_players_2026_27.csv", index=False)
pd.read_parquet("data/gap_hist.parquet").round(3).to_csv("data/scoring_gap_two_weeks_2003_2026.csv", index=False)
s = pd.read_parquet("data/seasons.parquet"); s[(s.g7 == 7) & (s.gr >= 30) & (s.p7 >= 25)][["season","name","p7","pr","ppg","gp","prev_ppg"]].round(3).to_csv("data/hot_starts_25ppg_2003_2026.csv", index=False)
pd.read_parquet("data/hot_model.parquet")[["season","name","p7","pr","prev_ppg","pred","loo"]].round(3).to_csv("data/hot_start_model_fit.csv", index=False)
pd.read_parquet("data/ts30_hist.parquet").round(4).to_csv("data/ts_30ppg_seasons_2003_2026.csv", index=False)
pd.read_parquet("data/mvp_hist.parquet").drop(columns=["pid"]).round(3).to_csv("data/mvp_seasons_2003_2026.csv", index=False)
json.dump(json.load(open("data/proj.json")), open("data/projection.json", "w"), indent=2)
print("csv export done")
