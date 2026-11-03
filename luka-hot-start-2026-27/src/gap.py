import pandas as pd, numpy as np
h = pd.read_parquet("data/hist_all.parquet"); h["date"] = pd.to_datetime(h.game_date); h["pts"]=h.points.astype(float)
out = []
for s, d in h.groupby("season"):
    op = d.date.min(); cut = d[d.date <= op + pd.Timedelta(days=13)]
    tgm = cut.groupby("team_abbreviation").game_id.nunique()
    g = cut.groupby(["athlete_id","athlete_display_name","team_abbreviation"]).agg(gp=("game_id","nunique"), pts=("pts","mean"), mins=("minutes","mean")).reset_index()
    g["tg"] = g.team_abbreviation.map(tgm); q = g[(g.gp >= 0.7*g.tg) & (g.mins >= 20)].sort_values("pts", ascending=False)
    out.append(dict(season=s, leader=q.iloc[0].athlete_display_name, p1=q.iloc[0].pts, second=q.iloc[1].athlete_display_name, p2=q.iloc[1].pts, gap=q.iloc[0].pts-q.iloc[1].pts, avg_team_g=tgm.mean()))
o = pd.DataFrame(out)
# final scoring champ
ss = pd.read_parquet("data/seasons.parquet"); q = ss[ss.gp >= 0.7*ss.team_g]
champ = q.loc[q.groupby("season").ppg.idxmax(), ["season","name","ppg"]].rename(columns={"name":"champ","ppg":"champ_ppg"})
o = o.merge(champ, on="season"); o["leader_won"] = o.leader == o.champ
print(o.round(1).to_string(index=False)); print("leader won title:", o.leader_won.mean(), "avg gap", o.gap.mean())
o.to_parquet("data/gap_hist.parquet")
