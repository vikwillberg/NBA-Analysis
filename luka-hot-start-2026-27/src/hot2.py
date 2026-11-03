import pandas as pd, numpy as np
s = pd.read_parquet("data/seasons.parquet")
x = s[(s.g7 == 7) & (s.gr >= 30) & (s.p7 >= 25)].copy()
print("n hot starts >=25:", len(x))
b = np.polyfit(x.p7, x.pr, 1); print("rest ~ first7:", b, "r", np.corrcoef(x.p7, x.pr)[0,1])
x["dr"] = x.p7 - x.pr
for lo in (25, 30, 33, 35):
    y = x[x.p7 >= lo]; print(lo, len(y), "avg first7 %.1f rest %.1f drop %.1f  med drop %.1f  share kept within 3: %.2f" % (y.p7.mean(), y.pr.mean(), y.dr.mean(), y.dr.median(), (y.dr <= 3).mean()))
print(x[x.p7 >= 33].sort_values("p7", ascending=False)[["season","name","p7","pr","ppg","prev_ppg","gp"]].round(1).to_string(index=False))
# model with prior season
z = x.dropna(subset=["prev_ppg"]); z = z[z.prev_gp >= 40]
A = np.column_stack([np.ones(len(z)), z.p7, z.prev_ppg]); coef, *_ = np.linalg.lstsq(A, z.pr, rcond=None)
pred = A @ coef; res = z.pr - pred
print("rest ~ 1 + p7 + prev:", coef.round(3), "R2", 1 - res.var()/z.pr.var(), "RMSE", np.sqrt((res**2).mean()), "n", len(z))
print("prev-only R2", np.corrcoef(z.prev_ppg, z.pr)[0,1]**2, " p7-only R2", np.corrcoef(z.p7, z.pr)[0,1]**2)
# Luka
luka_prev = 33.5; p7 = 268/7
mu = coef @ [1, p7, luka_prev]; print("Luka projection rest:", mu)
# season total after 7 games: (268 + mu*(G-7))/G for G=70
for G in (65, 70, 75):
    print(G, (268 + mu*(G-7))/G)
# residual band 80%
print("80% band", np.percentile(res, [10, 90]), "95%", np.percentile(res,[2.5,97.5]))
z.assign(pred=pred, res=res).to_parquet("data/hot_model.parquet")
# Luka's own history
L = s[s.name.str.contains("Luka Don")][["season","p7","pr","ppg","gp"]]; print(L.round(1).to_string(index=False))
# seasons 35+ ppg in data, and 38+
print(s[(s.gp >= 0.7*s.team_g) & (s.ppg >= 34)][["season","name","ppg","gp"]].round(1))
