# Significance tests: run `gpt-oss-120b_2026-11-18` (model gpt-oss-120b)

810 variants across 30 base resumes. Outcome = variant mean score minus its own baseline mean. Equivalence margin = ±2.0 points.

Mean within-item SD across the 3 samples: 3.83 points.

## 1. Any demographic cue vs. name-free baseline

Per base resume: mean of its 27 variants minus its baseline (n = 30).

- Mean difference +1.13 (95% CI +0.03 to +2.24)
- Paired t = 2.09, p = 0.045; Wilcoxon p = 0.040

  - high: -0.31, t = -0.63, p = 0.543
  - medium: +2.42, t = 1.75, p = 0.113
  - low: +1.30, t = 2.46, p = 0.036

## 2. Main effects (OLS, resume fixed effects, SEs clustered by base resume)

| Factor | F | df | p |
|---|---|---|---|
| race | 1.51 | 2, 29 | 0.237 |
| gender | 1.33 | 2, 29 | 0.280 |
| age_band | 1.23 | 2, 29 | 0.307 |

### Pairwise contrasts (Holm-adjusted across all 9)

| Factor | Contrast | Est. | 95% CI | p (Holm) | Equivalent within ±margin? (TOST p, Holm) |
|---|---|---|---|---|---|
| race | african_american − white | +0.36 | -0.19 to +0.91 | 1.000 | yes (0.000) |
| race | middle_eastern − white | +0.76 | -0.14 to +1.65 | 0.845 | yes (0.004) |
| race | middle_eastern − african_american | +0.40 | -0.24 to +1.03 | 1.000 | yes (0.000) |
| gender | female − male | -0.11 | -0.72 to +0.49 | 1.000 | yes (0.000) |
| gender | non_binary − male | +0.14 | -0.30 to +0.57 | 1.000 | yes (0.000) |
| gender | non_binary − female | +0.25 | -0.12 to +0.62 | 1.000 | yes (0.000) |
| age_band | 41-55 − 37-40 | +0.54 | -0.16 to +1.25 | 1.000 | yes (0.000) |
| age_band | 56-80 − 37-40 | +0.22 | -0.69 to +1.13 | 1.000 | yes (0.001) |
| age_band | 56-80 − 41-55 | -0.32 | -1.27 to +0.62 | 1.000 | yes (0.001) |

## 3. Interactions (Wald tests, same model structure)

| Term | F | df | p |
|---|---|---|---|
| race x tier | 1.64 | 4, 29 | 0.190 |
| gender x tier | 0.28 | 4, 29 | 0.887 |
| age_band x tier | 1.62 | 4, 29 | 0.196 |
| race x gender | 1.21 | 4, 29 | 0.329 |
| race x age_band | 0.19 | 4, 29 | 0.940 |
| gender x age_band | 0.95 | 4, 29 | 0.452 |

## 4. Robustness: Friedman test per factor (blocked on base resume)

| Factor | χ² | p |
|---|---|---|
| race | 0.72 | 0.697 |
| gender | 1.23 | 0.541 |
| age_band | 0.20 | 0.905 |

## 5. Main effects within each tier

| Tier | Factor | F | p |
|---|---|---|---|
| high | race | 0.53 | 0.606 |
| high | gender | 2.52 | 0.135 |
| high | age_band | 0.57 | 0.587 |
| medium | race | 2.18 | 0.169 |
| medium | gender | 0.51 | 0.616 |
| medium | age_band | 1.94 | 0.200 |
| low | race | 0.35 | 0.714 |
| low | gender | 0.24 | 0.793 |
| low | age_band | 1.22 | 0.339 |
