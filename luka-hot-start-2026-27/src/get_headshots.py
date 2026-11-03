"""Download ESPN headshots for every player drawn on the slides."""
import os, urllib.request, pandas as pd
os.makedirs("heads", exist_ok=True)
g = pd.read_parquet("data/players2027.parquet"); q = g[(g.gp >= 0.7*g.team_gp) & (g.min_pg >= 20)]
ids = set(q.sort_values("pts_pg", ascending=False).head(10).pid) | set(q.sort_values("pm_pg", ascending=False).head(8).pid)
names = ["Luka Doncic","Victor Wembanyama","Shai Gilgeous-Alexander","Jayson Tatum","Nikola Jokic","Tyrese Maxey","Giannis Antetokounmpo","Cooper Flagg"]
ids |= set(g[g.name.isin(names)].pid)
ids |= {"3975", "4278073", "3059318", "3032977"}          # best 30-PPG TS% seasons (Curry, SGA, Embiid, Giannis)
g[g.name.isin(names)][["name","pid","team"]].to_csv("data/heads.csv", index=False)
for pid in sorted(map(str, ids)):
    p = f"heads/{pid}.png"
    if not os.path.exists(p): urllib.request.urlretrieve(f"https://a.espncdn.com/i/headshots/nba/players/full/{pid}.png", p)
print(len(ids), "headshots")
