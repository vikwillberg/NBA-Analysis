import json, urllib.request, sys, os, time
OUT = "data/espn"
def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)
        except Exception as e: time.sleep(2); err = e
    raise err
import datetime as dt
d = dt.date(2026, 10, 20); events = []
while d <= dt.date(2026, 11, 2):   # data snapshot: games through Nov. 2, 2026
    sb = get(f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={d:%Y%m%d}&limit=50")
    for e in sb["events"]:
        st = e["status"]["type"]
        events.append((str(d), e["id"], e["shortName"], st["completed"], e["season"]["type"]))
    d += dt.timedelta(days=1)
json.dump(events, open(f"{OUT}/events.json", "w"))
done = [e for e in events if e[3]]
print(len(events), "events;", len(done), "completed; season types", set(e[4] for e in events))
for e in done:
    p = f"{OUT}/{e[1]}.json"
    if not os.path.exists(p): json.dump(get(f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={e[1]}"), open(p, "w"))
print("last dates:", [e for e in events if e[0] >= "2026-11-02"])
