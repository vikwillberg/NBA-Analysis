import json, glob, pandas as pd
OUT = "data/espn"
events = {e[1]: e for e in json.load(open(f"{OUT}/events.json"))}
rows, teams = [], []
for gid, e in events.items():
    s = json.load(open(f"{OUT}/{gid}.json"))
    comp = s["header"]["competitions"][0]
    sc = {c["team"]["abbreviation"]: (int(c["score"]), c.get("winner"), c["homeAway"]) for c in comp["competitors"]}
    for tb in s["boxscore"]["players"]:
        ab = tb["team"]["abbreviation"]; opp = [k for k in sc if k != ab][0]
        teams.append(dict(game_id=gid, date=e[0], team=ab, opp=opp, pf=sc[ab][0], pa=sc[opp][0], win=sc[ab][1], home=sc[ab][2]))
        st = tb["statistics"][0]; keys = st["keys"]
        for a in st["athletes"]:
            if a.get("didNotPlay") or not a.get("stats"): continue
            r = dict(zip(keys, a["stats"])); r.update(game_id=gid, date=e[0], team=ab, opp=opp, pid=a["athlete"]["id"], name=a["athlete"]["displayName"], win=sc[ab][1])
            rows.append(r)
p = pd.DataFrame(rows); t = pd.DataFrame(teams)
print(p.columns.tolist())
def split(col, a, b):
    x = p[col].str.split("-", expand=True); p[a] = x[0].astype(int); p[b] = x[1].astype(int)
split("fieldGoalsMade-fieldGoalsAttempted", "fgm", "fga"); split("threePointFieldGoalsMade-threePointFieldGoalsAttempted", "tpm", "tpa"); split("freeThrowsMade-freeThrowsAttempted", "ftm", "fta")
ren = {"minutes": "min", "points": "pts", "rebounds": "reb", "assists": "ast", "turnovers": "tov", "steals": "stl", "blocks": "blk", "plusMinus": "pm", "offensiveRebounds": "orb", "defensiveRebounds": "drb"}
p = p.rename(columns=ren)
for c in ren.values(): p[c] = pd.to_numeric(p[c].astype(str).str.replace("+", ""), errors="coerce")
p.to_parquet("data/box2027.parquet"); t.to_parquet("data/team2027.parquet")
print(p.shape, t.shape, t.groupby("team").size().describe())
l = p[p.name == "Luka Doncic"].sort_values("date"); print(l[["date","opp","min","pts","reb","ast","fgm","fga","tpm","tpa","ftm","fta","tov","pm","win"]].to_string())
