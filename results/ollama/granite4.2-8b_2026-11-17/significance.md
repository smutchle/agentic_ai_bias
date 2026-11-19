# Significance tests: run `granite4.2-8b_2026-11-17` (model granite4.2:8b)

810 variants across 31 base resumes. Outcome = variant mean score minus its own baseline mean. Equivalence margin = ±2.0 points.

Mean within-item SD across the 3 samples: 3.91 points.

## 1. Any demographic cue vs. name-free baseline

Per base resume: mean of its 27 variants minus its baseline (n = 30).

- Mean difference +0.07 (95% CI -1.57 to +1.71)
- Paired t = 0.08, p = 0.934; Wilcoxon p = 0.879

  - high: +1.25, t = 1.27, p = 0.236
  - medium: +0.52, t = 0.31, p = 0.762
  - low: -1.56, t = -1.10, p = 0.298

## 2. Main effects (OLS, resume fixed effects, SEs clustered by base resume)

| Factor | F | df | p |
|---|---|---|---|
| race | 2.09 | 2, 29 | 0.142 |
| gender | 0.29 | 2, 29 | 0.749 |
| age_band | 0.14 | 2, 29 | 0.869 |

### Pairwise contrasts (Holm-adjusted across all 9)

| Factor | Contrast | Est. | 95% CI | p (Holm) | Equivalent within ±margin? (TOST p, Holm) |
|---|---|---|---|---|---|
| race | african_american − white | -0.84 | -1.69 to +0.00 | 0.459 | yes (0.005) |
| race | middle_eastern − white | -0.25 | -0.80 to +0.31 | 1.000 | yes (0.000) |
| race | middle_eastern − african_american | +0.60 | -0.14 to +1.33 | 0.854 | yes (0.001) |
| gender | female − male | -0.25 | -1.01 to +0.52 | 1.000 | yes (0.000) |
| gender | non_binary − male | -0.09 | -1.02 to +0.83 | 1.000 | yes (0.000) |
| gender | non_binary − female | +0.16 | -0.50 to +0.81 | 1.000 | yes (0.000) |
| age_band | 41-55 − 37-40 | +0.02 | -0.77 to +0.80 | 1.000 | yes (0.000) |
| age_band | 56-80 − 37-40 | +0.20 | -0.84 to +1.25 | 1.000 | yes (0.001) |
| age_band | 56-80 − 41-55 | +0.18 | -0.53 to +0.90 | 1.000 | yes (0.000) |

## 3. Interactions (Wald tests, same model structure)

| Term | F | df | p |
|---|---|---|---|
| race x tier | 1.75 | 4, 29 | 0.166 |
| gender x tier | 0.49 | 4, 29 | 0.746 |
| age_band x tier | 0.78 | 4, 29 | 0.546 |
| race x gender | 0.86 | 4, 29 | 0.501 |
| race x age_band | 1.14 | 4, 29 | 0.358 |
| gender x age_band | 0.17 | 4, 29 | 0.950 |

## 4. Robustness: Friedman test per factor (blocked on base resume)

| Factor | χ² | p |
|---|---|---|
| race | 3.39 | 0.183 |
| gender | 0.16 | 0.925 |
| age_band | 1.13 | 0.568 |

## 5. Main effects within each tier

| Tier | Factor | F | p |
|---|---|---|---|
| high | race | 1.46 | 0.282 |
| high | gender | 1.74 | 0.229 |
| high | age_band | 1.68 | 0.239 |
| medium | race | 1.30 | 0.319 |
| medium | gender | 0.26 | 0.775 |
| medium | age_band | 0.31 | 0.741 |
| low | race | 1.31 | 0.316 |
| low | gender | 0.22 | 0.810 |
| low | age_band | 0.19 | 0.833 |
