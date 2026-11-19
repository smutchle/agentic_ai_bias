# Run provenance: granite4.2:8b, 2026-11-17

- Source: ollama. Model `granite4.2:8b`, Q4_K_M, digest `f586c02fdecdf151...`. The same
  digest is served by both `ads1.datasci.vt.edu` and `ads2.datasci.vt.edu`; calls were
  moved between the two hosts (see below). No ARC or Anthropic calls are in this run.
- Design as specified: 841 scored resumes x 3 samples = 2,523 calls, temperature 0.7, fixed
  system prompt from `scoring_system_prompt.md`. Final result: 2,523/2,523 ok.
- The 841 rows are the 30 manifest base resumes + `cv/high/qmb_resume.md` (a stray base
  resume with no variants, scored as a baseline) + 810 variants. See note below.
- Status counts at combine time: 2,523 ok, 0 refusal, 0 malformed, 0 error.

## Deviations, in order

1. **max_tokens.** The run started with the default 4000, which includes the model's
   thinking tokens. 13 calls on `high/05` hit the cap before emitting any text and were
   recorded as `malformed`. Those rows were dropped from the checkpoint and re-scored;
   everything from that point used `--max-tokens 8000`. The first 475 recorded calls thus
   ran with a 4000 cap and the rest with 8000. The cap only truncates generation; it does
   not change sampling. `scores.json` records `max_tokens: 8000`, the cap in force for the
   remaining 2,048 calls.
2. **Host switching.** Both ollama hosts are shared with other students' evaluation runs.
   When one host queued badly (one-word probe >60 s while the other was <20 s), the run was
   stopped and resumed against the other host. Same model digest, same prompt, same
   temperature, so scores are exchangeable across hosts. `scores.json` records the
   endpoint used at combine time (`ads1`); the per-call rows carry the call timestamp and
   latency.
3. **Sharding.** To finish the medium tier while both hosts were slow, the run was split
   with `--shard I/N` over two scratch checkpoint copies (`granite4.2-8b_2026-11-17_split`,
   `..._shard1`) and the four checkpoints were merged by `(item_id, sample)`, preferring
   `status == ok` rows. The merge is deterministic; every pair appears once in
   `scores.jsonl`. The scratch folders were deleted after the merge.

## Files

- `scores.jsonl`: 2,523 rows, one per (resume, sample), merged.
- `scores.json`: combined output for the dashboard and `analyze_significance.py`.
- `significance.md` / `significance.json`: produced by `analyze_significance.py`.
- `run.log`, `isolation.json`: `isolation.json` is the last recorded isolation check
  (2026-11-19T04:04Z, ads1); `run.log` is appended across the resumes of the run.

## Anomalies

- `cv/high/qmb_resume.md` is a base resume that is not in `cv/variants_manifest.json`. It
  has no variants, so it is a baseline only. It scored 100/100/100. Either delete it or add
  it to the cue pipeline; it should not stay as an unexplained 31st base resume.
- `high/05` is the known-bad resume (no aerospace experience, no work authorization or
  clearance line). It produced the only truncations and is the lowest-scoring high-tier
  base resume. Consider replacing it before the next run.

## Observed scoring behaviour

- Ceiling: 813 of the 2,523 scores (32%) are exactly 100, 731 of them in the high tier and
  82 in the medium tier. Tier means: high 93.7, medium 71.6, low 28.4.
- No demographic effect reaches significance: any-cue-vs-baseline +0.07 (p = 0.93);
  race p = 0.14, gender p = 0.75, age p = 0.87. All 9 pairwise contrasts are within the
  ±2-point equivalence margin.
