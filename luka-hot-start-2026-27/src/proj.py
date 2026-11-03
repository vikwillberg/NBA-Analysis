import pandas as pd, numpy as np, json
z = pd.read_parquet("data/hot_model.parquet")
X = np.column_stack([np.ones(len(z)), z.p7, z.prev_ppg]); y = z.pr.values
coef = np.linalg.lstsq(X, y, rcond=None)[0]
# leave-one-out
loo = []
for i in range(len(z)):
    m = np.ones(len(z), bool); m[i] = False; c = np.linalg.lstsq(X[m], y[m], rcond=None)[0]; loo.append(y[i] - X[i] @ c)
loo = np.array(loo); print("LOO RMSE %.2f MAE %.2f" % (np.sqrt((loo**2).mean()), np.abs(loo).mean()))
naive = y - z.p7.values; print("naive 'keeps pace' MAE %.2f, mean bias %.2f" % (np.abs(naive).mean(), naive.mean()))
prevonly = y - z.prev_ppg.values; print("prev-season-only MAE %.2f" % np.abs(prevonly).mean())
mu = coef @ [1, 268/7, 33.5]; print("rest proj", mu)
G = 70
q = np.percentile(loo, [10, 50, 90]); print("loo pct", q)
season = lambda r: (268 + r*(G-7))/G
print("season proj %.2f, 80%% %.2f-%.2f" % (season(mu), season(mu+q[0]), season(mu+q[2])))
need35 = (35*G-268)/(G-7); need38 = (38.3*G-268)/(G-7)
print("P(season>=35) %.3f  P(season>=38.3) %.3f  P(season>=36.1 Harden) %.3f" % ((mu+loo >= need35).mean(), (mu+loo >= need38).mean(), (mu+loo >= (36.1*G-268)/(G-7)).mean()))
print("P season>=30:", (mu+loo >= (30*G-268)/(G-7)).mean())
# robustness: G 60/75
for GG in (60, 65, 75): print(GG, round((268 + mu*(GG-7))/GG,2))
json.dump(dict(coef=coef.tolist(), mu=mu, loo_rmse=float(np.sqrt((loo**2).mean())), loo_p10=q[0], loo_p90=q[2], G=G), open("data/proj.json","w"))
z.assign(loo=loo).to_parquet("data/hot_model.parquet")
