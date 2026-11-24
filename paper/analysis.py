"""Cross-model analysis for the bias-audit article.

Unit of analysis: the base resume (n = 30). For each model and each base resume,
variant scores (mean of valid samples) are expressed as the difference from that
resume's name-free baseline, then averaged within demographic levels. Every
contrast is therefore a paired comparison across the 30 base resumes.
"""
import itertools, json
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parent.parent
RUNS = [  # (label, family, run dir)
    ("DeepSeek 4.1 Flash", "ARC/vt-arc-llm_2026-11-11"),
    ("GPT-OSS 120B", "ARC/gpt-oss-120b_2026-11-12"),
    ("GLM-5.3", "ARC/glm-5.3_2026-11-17"),
    ("Claude Sonnet 5.5", "anthropic/claude-sonnet-5-5_2026-11-12"),
    ("Claude Haiku 5.5", "anthropic/claude-haiku-5-5_2026-11-13"),
    ("Ornith 1.5 9B", "ollama/ornith-1.5-9b_2026-11-17"),
    ("Qwen 3.8 27B", "ollama/qwen3.8-27b_2026-11-23"),
    ("Granite 4.2 8B", "ollama/granite4.2-8b_2026-11-23"),
]
# cv/high/qmb_resume.md was added to the repository after the first six runs. It has
# no demographic variants and is not one of the 30 base resumes, so it is dropped.
EXTRA_ITEMS = ("high/qm",)
MODELS = [r[0] for r in RUNS]
FACTORS = {
    "race": ["white", "african_american", "middle_eastern"],
    "gender": ["male", "female", "non_binary"],
    "age_band": ["37-40", "41-55", "56-80"],
}
NICE = {"white": "White", "african_american": "African American", "middle_eastern": "Middle Eastern",
        "male": "Male", "female": "Female", "non_binary": "Non-binary",
        "37-40": "37-40", "41-55": "41-55", "56-80": "56-80",
        "race": "Race", "gender": "Gender", "age_band": "Age band"}
TIERS = ["high", "medium", "low"]
MARGIN = 2.0


def load():
    frames, meta, samples = [], [], []
    for label, rd in RUNS:
        d = json.load(open(ROOT / "results" / rd / "scores.json"))
        d["results"] = [r for r in d["results"] if r["resume_id"] not in EXTRA_ITEMS]
        run = d["run"]
        st = [s_.get("status") for r in d["results"] for s_ in r["samples"]]
        run.update(n_calls=len(st), n_ok=st.count("ok"), n_refusal=st.count("refusal"),
                   n_malformed=st.count("malformed"), n_error=st.count("error"))
        df = pd.DataFrame([{k: v for k, v in r.items() if k not in ("samples", "earlier_career")}
                           for r in d["results"]])
        df["model"] = label
        frames.append(df)
        for r in d["results"]:
            for s in r["samples"]:
                samples.append({"model": label, "item_id": r["item_id"], "resume_id": r["resume_id"],
                                "tier": r["tier"], "is_baseline": r["is_baseline"],
                                "status": s.get("status"), "score": s.get("score")})
        meta.append({"model": label, "model_id": run["model"], "source": run["source"],
                     "run": run["run_name"], "temperature": run["temperature"],
                     "n_calls": run["n_calls"], "n_ok": run["n_ok"], "n_refusal": run["n_refusal"],
                     "n_malformed": run["n_malformed"], "n_error": run["n_error"],
                     "isolation": (run.get("isolation_check") or {}).get("passed")})
    df = pd.concat(frames, ignore_index=True)
    df["model"] = pd.Categorical(df["model"], MODELS, ordered=True)
    return df, pd.DataFrame(meta), pd.DataFrame(samples)


def tci(x, level=0.95):
    x = np.asarray(x, float); n = len(x)
    m, se = x.mean(), x.std(ddof=1) / np.sqrt(n)
    h = stats.t.ppf(0.5 + level / 2, n - 1) * se
    return m, se, m - h, m + h


def level_means(var, factor):
    """resume x level matrix of mean diff-from-baseline (one model)."""
    return var.pivot_table(index="resume_id", columns=factor, values="diff_from_baseline",
                           aggfunc="mean", observed=True)[FACTORS[factor]]


def hotelling(D):
    """One-sample Hotelling T^2 that the column means of D (n x p) are all zero."""
    D = np.asarray(D, float); n, p = D.shape
    m = D.mean(0); S = np.cov(D, rowvar=False).reshape(p, p)
    T2 = n * m @ np.linalg.pinv(S) @ m
    F = (n - p) / (p * (n - 1)) * T2
    return F, p, n - p, stats.f.sf(F, p, n - p)


def contrasts(df, exclude=()):
    var = df[~df.is_baseline & ~df.resume_id.isin(exclude)]
    rows, omni, per_resume = [], [], []
    for model in MODELS:
        v = var[var.model == model]
        for f, lv in FACTORS.items():
            W = level_means(v, f)
            F, d1, d2, p = hotelling(np.c_[W[lv[1]] - W[lv[0]], W[lv[2]] - W[lv[0]]])
            fr = stats.friedmanchisquare(*[W[c] for c in lv])
            omni.append({"model": model, "factor": f, "F": F, "df1": d1, "df2": d2, "p": p,
                         "friedman_chi2": fr.statistic, "friedman_p": fr.pvalue})
            for a, b in itertools.combinations(lv, 2):
                d = W[b] - W[a]
                m, se, lo, hi = tci(d)
                n = len(d); t = m / se
                p = 2 * stats.t.sf(abs(t), n - 1)
                p_tost = max(stats.t.sf((m + MARGIN) / se, n - 1), stats.t.cdf((m - MARGIN) / se, n - 1))
                l90, h90 = tci(d, 0.90)[2:]
                try:
                    pw = stats.wilcoxon(d).pvalue
                except ValueError:
                    pw = np.nan
                rows.append({"model": model, "factor": f, "a": a, "b": b,
                             "contrast": f"{NICE[b]} - {NICE[a]}", "est": m, "se": se, "lo": lo, "hi": hi,
                             "lo90": l90, "hi90": h90, "t": t, "df": n - 1, "p": p, "p_wilcoxon": pw,
                             "p_tost": p_tost, "dz": m / d.std(ddof=1)})
                per_resume.append(pd.DataFrame({"model": model, "factor": f, "contrast": f"{NICE[b]} - {NICE[a]}",
                                                "resume_id": d.index, "d": d.values}))
    C = pd.DataFrame(rows)
    C["p_holm_model"] = C.groupby("model", observed=True)["p"].transform(lambda p: multipletests(p, method="holm")[1])
    C["p_holm_all"] = multipletests(C["p"], method="holm")[1]
    C["q_bh_all"] = multipletests(C["p"], method="fdr_bh")[1]
    C["p_tost_holm_model"] = C.groupby("model", observed=True)["p_tost"].transform(lambda p: multipletests(p, method="holm")[1])
    O = pd.DataFrame(omni)
    O["p_holm_all"] = multipletests(O["p"], method="holm")[1]
    return C, O, pd.concat(per_resume, ignore_index=True)


def heterogeneity(PR):
    """Does a contrast differ across models? Resumes are shared, so compare the
    6 per-resume contrast columns with Hotelling T^2 on 5 successive differences
    and with a Friedman test."""
    rows = []
    for (f, c), g in PR.groupby(["factor", "contrast"], sort=False):
        W = g.pivot(index="resume_id", columns="model", values="d")[MODELS]
        F, d1, d2, p = hotelling(np.diff(W.values, axis=1))
        fr = stats.friedmanchisquare(*[W[m] for m in MODELS])
        pooled = W.mean(1)
        m, se, lo, hi = tci(pooled)
        rows.append({"factor": f, "contrast": c, "pooled": m, "lo": lo, "hi": hi,
                     "p_pooled": 2 * stats.t.sf(abs(m / se), len(pooled) - 1),
                     "min": W.mean().min(), "max": W.mean().max(),
                     "F": F, "df1": d1, "df2": d2, "p_het": p, "friedman_p": fr.pvalue})
    H = pd.DataFrame(rows)
    H["p_het_holm"] = multipletests(H["p_het"], method="holm")[1]
    H["p_pooled_holm"] = multipletests(H["p_pooled"], method="holm")[1]
    return H


def named_vs_baseline(df):
    var = df[~df.is_baseline]
    rows = []
    for model in MODELS:
        per = var[var.model == model].groupby("resume_id")["diff_from_baseline"].mean()
        for tier in ["all"] + TIERS:
            x = per if tier == "all" else per[per.index.str.startswith(tier)]
            m, se, lo, hi = tci(x)
            rows.append({"model": model, "tier": tier, "n": len(x), "est": m, "lo": lo, "hi": hi,
                         "p": 2 * stats.t.sf(abs(m / se), len(x) - 1),
                         "p_wilcoxon": stats.wilcoxon(x).pvalue})
    N = pd.DataFrame(rows)
    N["p_holm"] = np.nan
    mask = N.tier == "all"
    N.loc[mask, "p_holm"] = multipletests(N.loc[mask, "p"], method="holm")[1]
    return N


def tier_contrasts(PR):
    """Per-tier estimates of each contrast and a one-way test that they differ by tier."""
    PR = PR.assign(tier=PR.resume_id.str.split("/").str[0])
    rows = []
    for (model, f, c), g in PR.groupby(["model", "factor", "contrast"], sort=False, observed=True):
        groups = [g[g.tier == t]["d"].values for t in TIERS]
        kw = stats.kruskal(*groups)
        an = stats.f_oneway(*groups)
        r = {"model": model, "factor": f, "contrast": c, "F": an.statistic, "p": an.pvalue, "kw_p": kw.pvalue}
        for t, x in zip(TIERS, groups):
            m, se, lo, hi = tci(x)
            r.update({f"{t}_est": m, f"{t}_lo": lo, f"{t}_hi": hi})
        rows.append(r)
    T = pd.DataFrame(rows)
    T["p_holm_all"] = multipletests(T["p"], method="holm")[1]
    return T


def two_way(df):
    """Factor x factor interactions per model: Hotelling on the 4 interaction contrasts per resume."""
    var = df[~df.is_baseline]
    rows = []
    for model in MODELS:
        v = var[var.model == model]
        for f1, f2 in itertools.combinations(FACTORS, 2):
            W = v.pivot_table(index="resume_id", columns=[f1, f2], values="diff_from_baseline", aggfunc="mean")
            a, b = FACTORS[f1], FACTORS[f2]
            cols = [(W[(a[i], b[j])] - W[(a[0], b[j])] - W[(a[i], b[0])] + W[(a[0], b[0])])
                    for i in (1, 2) for j in (1, 2)]
            F, d1, d2, p = hotelling(np.c_[tuple(cols)])
            rows.append({"model": model, "term": f"{NICE[f1]} x {NICE[f2]}", "F": F, "df1": d1, "df2": d2, "p": p})
    I = pd.DataFrame(rows)
    I["p_holm_all"] = multipletests(I["p"], method="holm")[1]
    return I


def noise(df, S):
    ok = S[S.status == "ok"]
    rows = []
    for model in MODELS:
        s = ok[ok.model == model]
        d = df[df.model == model]
        within = np.sqrt(s.groupby("item_id")["score"].var(ddof=1).mean())
        base = d[d.is_baseline]
        var = d[~d.is_baseline]
        rows.append({"model": model, "within_sd": within,
                     "base_high": base[base.tier == "high"].mean_score.mean(),
                     "base_medium": base[base.tier == "medium"].mean_score.mean(),
                     "base_low": base[base.tier == "low"].mean_score.mean(),
                     "pct_ge95_high": (s[s.tier == "high"].score >= 95).mean() * 100,
                     "n_distinct": s.score.nunique(),
                     "abs_diff_gt5": (var.diff_from_baseline.abs() > 5).mean() * 100,
                     "sd_diff": var.diff_from_baseline.std()})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    pd.set_option("display.width", 250, "display.max_rows", 200, "display.max_columns", 40, "display.float_format", "{:.3f}".format)
    df, meta, S = load()
    print(meta.to_string())
    print(df.groupby(["model"], observed=True).n_ok.agg(["min", "sum"]))
    print(noise(df, S))
    C, O, PR = contrasts(df)
    print(O)
    print(C[["model", "contrast", "est", "lo", "hi", "p", "p_holm_model", "p_holm_all", "q_bh_all", "p_tost_holm_model", "dz", "p_wilcoxon"]])
    print(heterogeneity(PR))
    print(named_vs_baseline(df))
    T = tier_contrasts(PR); print(T[T.p < 0.05])
    I = two_way(df); print(I)
    C2, O2, _ = contrasts(df, exclude=("high/05",))
    print("max abs change excluding high/05:", (C2.est - C.est).abs().max(), "| sig flips (holm model):", ((C2.p_holm_model < .05) != (C.p_holm_model < .05)).sum())


TIMELINE_RE = r"earlier[- ]career|retail|customer[- ]service|\b(?:19[6-9]\d|20[01]\d)\b"


def timeline_mentions():
    """Share of rationales that cite the Earlier Career line or a calendar year (keyword match)."""
    import re
    rx = re.compile(TIMELINE_RE, re.I)
    rows = []
    for label, rd in RUNS:
        d = json.load(open(ROOT / "results" / rd / "scores.json"))
        for r in d["results"]:
            if r["is_baseline"]:
                continue
            rats = [s["rationale"] for s in r["samples"] if s.get("rationale")]
            rows.append({"model": label, "tier": r["tier"], "age_band": r["age_band"],
                         "resume_id": r["resume_id"],
                         "has_line": r["earlier_career"] is not None,
                         "mention": np.mean([bool(rx.search(x)) for x in rats]) if rats else np.nan,
                         "diff": r["diff_from_baseline"]})
    return pd.DataFrame(rows)
