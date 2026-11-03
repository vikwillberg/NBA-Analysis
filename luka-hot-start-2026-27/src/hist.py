import pandas as pd, numpy as np, glob
fr = []
for f in sorted(glob.glob("data/hist/pb*.parquet")):
    d = pd.read_parquet(f, columns=["game_id","season","season_type","game_date","athlete_id","athlete_display_name","team_abbreviation","minutes","points","field_goals_made","field_goals_attempted","three_point_field_goals_made","free_throws_attempted","rebounds","assists","plus_minus","did_not_play","team_winner"])
    fr.append(d)
h = pd.concat(fr); h = h[h.season_type == 2]
h = h[h.did_not_play != True]; h = h[h.minutes.fillna(0) > 0]
h = h.drop_duplicates(["game_id","athlete_id"])
real = h.groupby(["season","team_abbreviation"]).size(); real = real[real > 500].reset_index()[["season","team_abbreviation"]]
h = h.merge(real, on=["season","team_abbreviation"])
h = h[~h.game_id.astype(int).isin([401607495, 401734908, 401809839])]
print(h.groupby("season").agg(rows=("game_id","size"), games=("game_id","nunique"), players=("athlete_id","nunique")).to_string())
h.to_parquet("data/hist_all.parquet")
