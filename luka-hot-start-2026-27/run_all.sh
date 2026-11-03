#!/usr/bin/env bash
# Rebuild every number, table, slide and the workbook. Run from this folder after ./setup.sh
set -euo pipefail
python3 src/pull_espn.py        # 2026-27 box scores from ESPN (games through Nov. 2, 2026)
python3 src/parse_espn.py       # -> data/box2027.parquet, data/team2027.parquet
python3 src/leaders.py          # per-player season totals, scoring leaders, team records
python3 src/hist.py             # 2002-03..2025-26 box scores (All-Star games, NBA Cup finals removed)
python3 src/hot.py              # player-season table + scoring-champion QA
python3 src/hot2.py             # hot-start analysis + regression model
python3 src/proj.py             # leave-one-out validation + Luka projection
python3 src/gap.py              # No.1 - No.2 scoring gap after two weeks, every season
python3 src/profile.py          # Luka's ranks among qualified players
python3 src/mvp.py              # MVP seasons since 2002-03 (PPG, team wins)
python3 src/eff.py              # plus-minus, on/off, TS% vs 30-PPG seasons
python3 src/get_headshots.py
for s in src/slide*.py; do python3 "$s"; done
python3 -c "import sys; sys.path.insert(0,'src'); from style import build_pdf; build_pdf([f'slides/Luka_vs_NBA_{i}.png' for i in range(1,6)], 'slides/Luka_vs_NBA_carousel.pdf')"
python3 src/workbook.py
python3 src/export_csv.py
