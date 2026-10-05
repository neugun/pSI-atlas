from pathlib import Path
import itertools
import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "SLM_generalization_six_behavior_and_latent_features_v1.csv"
OUT = ROOT / "data" / "SLM_generalization_latent_vs_behavior_double_mapping_v1.csv"
PAIR_OUT = ROOT / "data" / "SLM_generalization_behavior_double_mapping_pairs_v1.csv"

df = pd.read_csv(SRC).sort_values("animal").reset_index(drop=True)
assert len(df) == 6

food = df["food_fast"].to_numpy(float)
fear = df["shock_velocity_all30"].to_numpy(float)
credit = df["credit_sep_delta"].to_numpy(float)
ape = df["ape_abs_late"].to_numpy(float)

behavior_features = ["sri_late", "sri_delta", "conversion_late", "conversion_delta"]

def zr(v):
    r = rankdata(np.asarray(v, float), method="average")
    z = (r - r.mean()) / r.std(ddof=0)
    return z

Z = {c: zr(df[c].to_numpy(float)) for c in behavior_features}
Z["credit_sep_delta"] = zr(credit)
Z["ape_abs_late"] = zr(ape)
zf, zh = zr(food), zr(fear)

perms = np.array(list(itertools.permutations(range(len(df)))), dtype=int)
# Each row is one exact permutation of mouse identity within a later-behavior domain.
F = zf[perms]
H = zh[perms]

def corr_all(zx, Y):
    return (Y * zx[None, :]).mean(axis=1)

def score_grid(xname, yname):
    x, y = Z[xname], Z[yname]
    # matched: x->food + y->fear; mismatched: x->fear + y->food
    xf = corr_all(x, F)
    yf = corr_all(y, F)
    xh = corr_all(x, H)
    yh = corr_all(y, H)
    return (xf - yf)[:, None] + (yh - xh)[None, :]

def observed_score(xname, yname):
    x, y = Z[xname], Z[yname]
    return float(np.mean(x*zf) + np.mean(y*zh) - np.mean(x*zh) - np.mean(y*zf))

latent_grid = score_grid("credit_sep_delta", "ape_abs_late")
latent_obs = observed_score("credit_sep_delta", "ape_abs_late")
latent_p = float(np.mean(latent_grid >= latent_obs - 1e-12))

pair_rows = []
behavior_grids = []
for bf in behavior_features:
    for bh in behavior_features:
        g = score_grid(bf, bh)
        obs = observed_score(bf, bh)
        p = float(np.mean(g >= obs - 1e-12))
        pair_rows.append(dict(food_feature=bf, fear_feature=bh, observed_double_mapping=obs, p_exact_one_sided=p))
        behavior_grids.append(g)

pair_df = pd.DataFrame(pair_rows).sort_values("observed_double_mapping", ascending=False).reset_index(drop=True)
pair_df.to_csv(PAIR_OUT, index=False)

best_behavior_obs = float(pair_df.iloc[0]["observed_double_mapping"])
best_behavior_food = str(pair_df.iloc[0]["food_feature"])
best_behavior_fear = str(pair_df.iloc[0]["fear_feature"])

# Selection-aware behavior null: at every exact permutation, take the best of all 16 ordered behavior pairs.
behavior_max_grid = np.maximum.reduce(behavior_grids)
best_behavior_family_p = float(np.mean(behavior_max_grid >= best_behavior_obs - 1e-12))

# Direct latent-vs-best-behavior specificity contrast with the same selection correction.
diff_grid = latent_grid - behavior_max_grid
obs_diff = latent_obs - best_behavior_obs
diff_p = float(np.mean(diff_grid >= obs_diff - 1e-12))

# Also report simple matched correlations for interpretability.
def rho(a,b):
    return float(spearmanr(a,b).statistic)

summary = pd.DataFrame([{
    "n": len(df),
    "latent_food_feature": "credit_sep_delta",
    "latent_fear_feature": "ape_abs_late",
    "latent_credit_food_rho": rho(credit, food),
    "latent_credit_fear_rho": rho(credit, fear),
    "latent_ape_food_rho": rho(ape, food),
    "latent_ape_fear_rho": rho(ape, fear),
    "latent_double_mapping": latent_obs,
    "latent_p_exact_one_sided": latent_p,
    "best_behavior_food_feature": best_behavior_food,
    "best_behavior_fear_feature": best_behavior_fear,
    "best_behavior_double_mapping": best_behavior_obs,
    "best_behavior_family_selection_p_exact": best_behavior_family_p,
    "latent_minus_best_behavior": obs_diff,
    "latent_vs_behavior_selection_corrected_p_exact": diff_p,
    "n_behavior_ordered_pairs": len(behavior_grids),
    "n_domain_permutations": int(len(perms)**2),
}])
summary.to_csv(OUT, index=False)
print(summary.to_string(index=False))
print("\nTop behavior pairs")
print(pair_df.head(8).to_string(index=False))
