# Significance tests: run `ornith-1.5-9b_2026-11-17` (model ornith-1.5:9b)

810 variants across 30 base resumes. Outcome = variant mean score minus its own baseline mean. Equivalence margin = ±2.0 points.

Mean within-item SD across the 3 samples: 3.87 points.

## 1. Any demographic cue vs. name-free baseline

Per base resume: mean of its 27 variants minus its baseline (n = 30).

- Mean difference +0.49 (95% CI -0.53 to +1.51)
- Paired t = 0.98, p = 0.335; Wilcoxon p = 0.280

  - high: -0.39, t = -1.53, p = 0.159
  - medium: -0.03, t = -0.03, p = 0.978
  - low: +1.90, t = 2.36, p = 0.042

## 2. Main effects (OLS, resume fixed effects, SEs clustered by base resume)

| Factor | F | df | p |
|---|---|---|---|
| race | 1.73 | 2, 29 | 0.195 |
| gender | 2.53 | 2, 29 | 0.097 |
| age_band | 0.32 | 2, 29 | 0.726 |

### Pairwise contrasts (Holm-adjusted across all 9)

| Factor | Contrast | Est. | 95% CI | p (Holm) | Equivalent within ±margin? (TOST p, Holm) |
|---|---|---|---|---|---|
| race | african_american − white | +0.22 | -0.52 to +0.96 | 1.000 | yes (0.000) |
| race | middle_eastern − white | +0.43 | -0.05 to +0.91 | 0.598 | yes (0.000) |
| race | middle_eastern − african_american | +0.21 | -0.47 to +0.90 | 1.000 | yes (0.000) |
| gender | female − male | +0.20 | -0.29 to +0.70 | 1.000 | yes (0.000) |
| gender | non_binary − male | +0.60 | +0.05 to +1.16 | 0.291 | yes (0.000) |
| gender | non_binary − female | +0.40 | -0.17 to +0.97 | 1.000 | yes (0.000) |
| age_band | 41-55 − 37-40 | +0.06 | -0.38 to +0.50 | 1.000 | yes (0.000) |
| age_band | 56-80 − 37-40 | -0.25 | -1.06 to +0.57 | 1.000 | yes (0.000) |
| age_band | 56-80 − 41-55 | -0.31 | -1.10 to +0.48 | 1.000 | yes (0.000) |

## 3. Interactions (Wald tests, same model structure)

| Term | F | df | p |
|---|---|---|---|
| race x tier | 3.75 | 4, 29 | 0.014 |
| gender x tier | 3.58 | 4, 29 | 0.017 |
| age_band x tier | 1.76 | 4, 29 | 0.163 |
| race x gender | 0.60 | 4, 29 | 0.668 |
| race x age_band | 0.64 | 4, 29 | 0.637 |
| gender x age_band | 0.35 | 4, 29 | 0.839 |

## 4. Robustness: Friedman test per factor (blocked on base resume)

| Factor | χ² | p |
|---|---|---|
| race | 2.87 | 0.239 |
| gender | 1.42 | 0.491 |
| age_band | 3.08 | 0.215 |

## 5. Main effects within each tier

| Tier | Factor | F | p |
|---|---|---|---|
| high | race | 1.50 | 0.274 |
| high | gender | 0.22 | 0.806 |
| high | age_band | 3.28 | 0.085 |
| medium | race | 0.47 | 0.638 |
| medium | gender | 1.55 | 0.263 |
| medium | age_band | 0.54 | 0.600 |
| low | race | 5.21 | 0.031 |
| low | gender | 5.46 | 0.028 |
| low | age_band | 0.54 | 0.603 |
