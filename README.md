<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-agentic__ai__bias-181717?logo=github&logoColor=white)](https://github.com/smutchle/agentic_ai_bias)
[![Quarto](https://img.shields.io/badge/Quarto-Research%20documents-75AADB?logo=quarto&logoColor=white)](https://quarto.org/)

# Agentic AI Bias

**A counterfactual audit of demographic bias in LLM résumé screening**

ADS 5984

</div>

## Overview

This research project studies whether language models score equally qualified candidates differently when demographic signals in their résumés change. Each candidate is evaluated against the same aerospace Chief Technology Officer job posting. The planned audit includes models hosted on Virginia Tech ARC and, subject to access, Anthropic and Grok models.

## Study design

The current methodology is documented in [improved_prompt.md](improved_prompt.md). It proposes:

1. Create name-free base résumés across high, borderline, mid, and low qualification tiers.
2. Score the base résumés to check that the tiers separate, then create demographic variants while holding qualifications and other job-relevant information constant.
3. Score one résumé per fresh model context against the fixed job posting, with repeated samples and a consistent scoring prompt.
4. Compare scores across variants and with their name-free baselines, including analysis by qualification tier.

The [job posting](cto_job_listing.qmd) is the study's control document; changing its wording would affect comparisons across runs. The [scoring prompt](scoring_system_prompt.md) requests a score from 0 to 100 and a short rationale in JSON.

## Repository contents

| Path | Purpose |
| --- | --- |
| [improved_prompt.md](improved_prompt.md) | Current study design and planned analysis |
| [cto_job_listing.qmd](cto_job_listing.qmd) | Fixed CTO job posting; rendered [HTML](cto_job_listing.html) and [PDF](cto_job_listing.pdf) are also included |
| [scoring_system_prompt.md](scoring_system_prompt.md) | System prompt and input template for résumé scoring |
| [cv/high/](cv/high/) | Three high-fit sample résumés |
| [prompt.md](prompt.md), [prompt_resume.md](prompt_resume.md), [prompt_evaluation.md](prompt_evaluation.md) | Original and task-specific prompts |
| [backup/](backup/) | Superseded drafts kept for reference |

The project is at an early stage: the other résumé tiers, demographic variants, scoring pipeline, and analysis are not yet implemented. `prompt_evaluation.md` describes demographic categories and a variation strategy that differ from the current study design; reconcile them before running the experiment.

## Render the job posting

Install [Quarto](https://quarto.org/docs/get-started/), then run from the repository root:

```sh
quarto render cto_job_listing.qmd          # HTML and PDF
quarto render cto_job_listing.qmd --to pdf # PDF only
```

PDF rendering also requires a working LaTeX installation. Keep API credentials in a local `.env` file, which is ignored by Git.

## Resume a scoring run

`score_resumes.py` supports `ANTHROPIC_ENDPOINT`, `ANTHROPIC_API_KEY`, and
`ANTHROPIC_MODEL` in `.env`. It also accepts `OPEN_AI_ENDPOINT`,
`OPEN_AI_API_KEY`, and `OPEN_AI_MODEL` as fallbacks. An optional second key may
be supplied as `ANTHROPIC_API_KEY_2` or `OPEN_AI_API_KEY_2`; keys must be
personal and must not be shared. ARC limits GPT-OSS 120B to 10 concurrent
requests per user, regardless of how many keys are used.

```sh
python3 score_resumes.py --run-dir results/ARC/gpt-oss-120b_2026-11-12 --workers 10
tail -f results/ARC/gpt-oss-120b_2026-11-12/run.log
```

The JSONL checkpoint records each call as it completes, and the scorer resumes
unfinished calls when restarted with the same run directory. A snapshot in a
commit is incomplete until all planned calls have finished.
