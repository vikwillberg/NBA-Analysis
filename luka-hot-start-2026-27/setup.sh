#!/usr/bin/env bash
# One-time setup: Python packages, Inter font, NBA/team logos, historical box scores.
set -euo pipefail
pip install -q pandas numpy pyarrow matplotlib pillow fonttools brotli img2pdf openpyxl
mkdir -p fonts logos heads data/hist data/espn slides
if [ ! -f fonts/Inter-700.ttf ]; then
  npm pack @fontsource/inter@5 --silent && tar xzf fontsource-inter-*.tgz
  python3 -c "
from fontTools.ttLib import TTFont
for w in (400, 500, 600, 700):
    f = TTFont(f'package/files/inter-latin-{w}-normal.woff2'); f.flavor = None; f.save(f'fonts/Inter-{w}.ttf')"
  rm -rf package fontsource-inter-*.tgz
fi
curl -sS -o logos/NBA.png https://a.espncdn.com/i/teamlogos/leagues/500/nba.png
for t in atl bos bkn cha chi cle dal den det gs hou ind lac lal mem mia mil min no ny okc orl phi phx por sac sa tor utah wsh; do
  curl -sS --retry 3 -o logos/$(echo $t | tr a-z A-Z).png https://a.espncdn.com/i/teamlogos/nba/500/$t.png; done
REL=https://github.com/sportsdataverse/sportsdataverse-data/releases/download
for y in $(seq 2003 2026); do curl -sSL --retry 3 -o data/hist/pb$y.parquet $REL/espn_nba_player_boxscores/player_box_$y.parquet; done
for y in 2024 2025 2026; do curl -sSL --retry 3 -o data/hist/sch$y.parquet $REL/espn_nba_schedules/nba_schedule_$y.parquet; done
