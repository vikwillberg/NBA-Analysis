# NBA Analysis

NBA data stories by **Viktor Berg**: each folder is one project with its data, code, calculations and output, rebuildable from scratch.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-DuckDB-FFF000?logo=duckdb&logoColor=black)
![R](https://img.shields.io/badge/R-ggplot2-276DC3?logo=r&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-217346?logo=microsoftexcel&logoColor=white)

| [Luka vs NBA: the 2026-27 hot start](luka-hot-start-2026-27/) | [The 2-for-1 Ledger](nba-2for1-analysis/) |
|---|---|
| <img src="luka-hot-start-2026-27/slides/Luka_vs_NBA_1.png" alt="Slide 1: Luka leads the NBA in scoring by 8.3 a game" width="400"> | <img src="nba-2for1-analysis/output/figures/fig1_effect_by_start.png" alt="Chart: the 2-for-1 pays once you gain the ball with 33 or more seconds left" width="400"> |

| Project | Question | Output | Tools |
|---|---|---|---|
| [Luka vs NBA: the 2026-27 hot start](luka-hot-start-2026-27/) | Luka opened at 38.3 PPG. How unusual is it, can he keep it up, and is he the MVP favorite? | 5-slide LinkedIn carousel | Python, Excel |
| [The 2-for-1 Ledger](nba-2for1-analysis/) | How much is going 2-for-1 at the end of a quarter worth, and when does it stop working? | Case-study report, 3 charts (simulated play-by-play) | SQL (DuckDB), R, Python |

**Toolkit:** Python (pandas, NumPy, matplotlib), SQL (DuckDB), R (ggplot2, sandwich), Excel, ESPN and sportsdataverse public data. Every project folder has a `run_all.sh` that rebuilds its numbers and output from scratch. Carousel projects also have a `setup.sh` and a workbook where each number on a slide traces back to a formula.
