# Significance tests: run `glm-5.3_2026-11-17` (model GLM-5.3)

810 variants across 30 base resumes. Outcome = variant mean score minus its own baseline mean. Equivalence margin = ±2.0 points.

Mean within-item SD across the 3 samples: 2.17 points.

## 1. Any demographic cue vs. name-free baseline

Per base resume: mean of its 27 variants minus its baseline (n = 30).

- Mean difference +0.39 (95% CI -0.35 to +1.12)
- Paired t = 1.07, p = 0.292; Wilcoxon p = 0.567

  - high: -0.49, t = -1.96, p = 0.081
  - medium: +0.07, t = 0.27, p = 0.797
  - low: +1.58, t = 1.69, p = 0.125

## 2. Main effects (OLS, resume fixed effects, SEs clustered by base resume)

| Factor | F | df | p |
|---|---|---|---|
| race | 6.02 | 2, 29 | 0.007 |
| gender | 4.41 | 2, 29 | 0.021 |
| age_band | 2.11 | 2, 29 | 0.139 |

### Pairwise contrasts (Holm-adjusted across all 9)

| Factor | Contrast | Est. | 95% CI | p (Holm) | Equivalent within ±margin? (TOST p, Holm) |
|---|---|---|---|---|---|
| race | african_american − white | +0.61 | +0.23 to +1.00 | 0.024 | yes (0.000) |
| race | middle_eastern − white | +0.08 | -0.27 to +0.42 | 0.892 | yes (0.000) |
| race | middle_eastern − african_american | -0.54 | -0.92 to -0.15 | 0.054 | yes (0.000) |
| gender | female − male | +0.49 | +0.15 to +0.82 | 0.049 | yes (0.000) |
| gender | non_binary − male | +0.31 | -0.12 to +0.74 | 0.623 | yes (0.000) |
| gender | non_binary − female | -0.18 | -0.60 to +0.24 | 0.892 | yes (0.000) |
| age_band | 41-55 − 37-40 | -0.29 | -0.66 to +0.07 | 0.550 | yes (0.000) |
| age_band | 56-80 − 37-40 | -0.53 | -1.09 to +0.03 | 0.364 | yes (0.000) |
| age_band | 56-80 − 41-55 | -0.24 | -0.69 to +0.22 | 0.892 | yes (0.000) |

## 3. Interactions (Wald tests, same model structure)

| Term | F | df | p |
|---|---|---|---|
| race x tier | 5.96 | 4, 29 | 0.001 |
| gender x tier | 3.38 | 4, 29 | 0.022 |
| age_band x tier | 3.22 | 4, 29 | 0.026 |
| race x gender | 1.96 | 4, 29 | 0.127 |
| race x age_band | 2.84 | 4, 29 | 0.042 |
| gender x age_band | 1.03 | 4, 29 | 0.407 |

## 4. Robustness: Friedman test per factor (blocked on base resume)

| Factor | χ² | p |
|---|---|---|
| race | 15.25 | 0.000 |
| gender | 6.07 | 0.048 |
| age_band | 13.33 | 0.001 |

## 5. Main effects within each tier

| Tier | Factor | F | p |
|---|---|---|---|
| high | race | 1.80 | 0.219 |
| high | gender | 4.39 | 0.047 |
| high | age_band | 2.62 | 0.127 |
| medium | race | 9.08 | 0.007 |
| medium | gender | 0.68 | 0.533 |
| medium | age_band | 16.54 | 0.001 |
| low | race | 9.16 | 0.007 |
| low | gender | 7.19 | 0.014 |
| low | age_band | 0.38 | 0.696 |
