# Significance tests: run `gpt-oss-120b_2026-11-20` (model gpt-oss-120b)

837 variants across 31 base resumes. Outcome = variant mean score minus its own baseline mean. Equivalence margin = ±2.0 points.

Mean within-item SD across the 3 samples: 3.70 points.

## 1. Any demographic cue vs. name-free baseline

Per base resume: mean of its 27 variants minus its baseline (n = 30).

- Mean difference -0.86 (95% CI -2.61 to +0.90)
- Paired t = -1.00, p = 0.326; Wilcoxon p = 0.809

  - high: -0.61, t = -1.03, p = 0.326
  - medium: -2.15, t = -0.84, p = 0.424
  - low: +0.16, t = 0.30, p = 0.770

## 2. Main effects (OLS, resume fixed effects, SEs clustered by base resume)

| Factor | F | df | p |
|---|---|---|---|
| race | 1.82 | 2, 30 | 0.179 |
| gender | 1.92 | 2, 30 | 0.165 |
| age_band | 0.40 | 2, 30 | 0.675 |

### Pairwise contrasts (Holm-adjusted across all 9)

| Factor | Contrast | Est. | 95% CI | p (Holm) | Equivalent within ±margin? (TOST p, Holm) |
|---|---|---|---|---|---|
| race | african_american − white | -0.39 | -0.95 to +0.17 | 1.000 | yes (0.000) |
| race | middle_eastern − white | +0.03 | -0.53 to +0.60 | 1.000 | yes (0.000) |
| race | middle_eastern − african_american | +0.43 | -0.07 to +0.92 | 0.712 | yes (0.000) |
| gender | female − male | -0.36 | -0.74 to +0.02 | 0.538 | yes (0.000) |
| gender | non_binary − male | -0.30 | -0.81 to +0.21 | 1.000 | yes (0.000) |
| gender | non_binary − female | +0.06 | -0.35 to +0.48 | 1.000 | yes (0.000) |
| age_band | 41-55 − 37-40 | +0.28 | -0.57 to +1.12 | 1.000 | yes (0.000) |
| age_band | 56-80 − 37-40 | +0.08 | -0.81 to +0.97 | 1.000 | yes (0.000) |
| age_band | 56-80 − 41-55 | -0.20 | -0.75 to +0.36 | 1.000 | yes (0.000) |

## 3. Interactions (Wald tests, same model structure)

| Term | F | df | p |
|---|---|---|---|
| race x tier | 1.16 | 4, 30 | 0.346 |
| gender x tier | 4.10 | 4, 30 | 0.009 |
| age_band x tier | 1.01 | 4, 30 | 0.419 |
| race x gender | 0.34 | 4, 30 | 0.848 |
| race x age_band | 1.09 | 4, 30 | 0.379 |
| gender x age_band | 0.43 | 4, 30 | 0.786 |

## 4. Robustness: Friedman test per factor (blocked on base resume)

| Factor | χ² | p |
|---|---|---|
| race | 1.61 | 0.446 |
| gender | 1.52 | 0.467 |
| age_band | 0.64 | 0.726 |

## 5. Main effects within each tier

| Tier | Factor | F | p |
|---|---|---|---|
| high | race | 0.06 | 0.940 |
| high | gender | 0.64 | 0.546 |
| high | age_band | 1.46 | 0.278 |
| medium | race | 2.55 | 0.132 |
| medium | gender | 4.17 | 0.052 |
| medium | age_band | 0.66 | 0.539 |
| low | race | 0.53 | 0.608 |
| low | gender | 5.08 | 0.033 |
| low | age_band | 0.08 | 0.928 |
