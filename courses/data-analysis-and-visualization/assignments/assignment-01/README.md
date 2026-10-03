# AI-854 Data Analysis and Visualization

## Individual Assignment 1: Does a Higher Average Mean More Reliable Powerplay Scoring?

| Item | Details |
|---|---|
| Coverage | Lectures 1–4: questions and coverage, tidy data, visual arguments, distributions and independent units |
| Due | **Thursday 8 October 2026, 23:59 Pakistan time** |
| Mode | Individual take-home assignment |
| Maximum marks | 20 |
| Submit | `AI854_A1_<StudentID>.pdf` and `AI854_A1_<StudentID>.zip` |
| Tools | Python, pandas, NumPy and Matplotlib; Jupyter optional |
| Starter | [AI854_A1_Starter](AI854_A1_Starter/) — supplied CSV snapshot, report outline and notebook scaffold; no analytical solutions |

## The question

A commentator says: “The team with the higher average powerplay score is the more reliable batting side.” An average is only one description. Teams may differ in spread, low-scoring outcomes, and the number of matches represented.

**Compare Islamabad United and Lahore Qalandars in the supplied PSL 2019 powerplay records and decide how far the claim is supported.** This is a new comparison: do not reproduce the Lecture 4 death-over example. You do not need cricket expertise. Explain the population, denominator and meaning of reliability before reporting results.

## Supplied data and scope

Use `AI854_A1_Starter/data/powerplay_2019.csv`, an unmodified row subset of the prepared Lecture 4 `psl_overs.csv`: season year 2019, phase Powerplay, the two named batting teams. The subset retains incomplete overs so you can audit eligibility. Provenance and the source file's checksum are in `data/provenance.json`. The original records are derived from Cricsheet's PSL archive; preserve that attribution. No collection or internet access is required.

`match_id`, `innings` and `over_number` identify an over. `total_runs` includes extras; `legal_balls` counts legal deliveries. `complete_over` indicates six legal balls. Powerplay overs are numbered 1–6. Read the supplied data dictionary before analysis. A missing over is not a zero-run over. The supplied archive is the observed source, not a guarantee of all possible matches or players.

## Part A — Frame the comparison and audit eligibility [4 marks]

Before calculating team results, write the question, observed population, over-level unit and match-level independent unit. Define “reliable” operationally as a lower rate of complete-powerplay totals **below 40 runs**. Define the primary center effect as Islamabad minus Lahore mean complete-powerplay total. The threshold is fixed; do not tune it after looking at results. [1]

Audit row counts, missing required values, duplicate `(match_id, innings, over_number)` keys, date/season agreement, team labels, over numbers, negative runs and legal-ball counts. Summarize all checks with counts and action taken. Investigate failures rather than silently deleting them. [1]

Create a match/innings eligibility table. An eligible batting innings has exactly one record for each over 1–6 and every over has six legal balls and `complete_over=True`. Retain excluded innings in the audit with reasons; do not impute missing overs. Show eligible/excluded counts by team. Trace two summary totals back to their source over rows. [2]

## Part B — Summarize the distributions [4 marks]

For each eligible innings sum the six `total_runs` values to obtain a complete-powerplay total. Produce one tidy summary row per `(match_id, innings, batting_team)` with date and total. For each team report number of eligible innings, mean, median, sample standard deviation (`ddof=1`), Q1, Q3, IQR, minimum and maximum, and the proportion below 40. Use linear interpolation for quantiles and state that convention. [2]

Calculate the mean difference and the below-40 rate difference (Islamabad minus Lahore). Describe one center finding and one spread/tail finding with units and denominators. Separately calculate the mean over score for all complete overs, including those from ineligible innings. Compare that ranking with the complete-powerplay result and explain how the eligibility rule and weighting can change the answer. A rank reversal is not required for full marks. [2]

## Part C — Build a visual argument [4 marks]

Include **exactly three final numbered figures**; readable panels are permitted:

1. Eligible powerplay totals by team, showing individual innings with a boxplot or another clearly justified distribution summary.
2. ECDFs of those totals, marking 40 runs and explaining what the curves reveal about low outcomes.
3. Powerplay totals against match date for both teams, showing within-season variation and eligible sample sizes. Points are sufficient; lines must not imply observations between matches.

Every figure needs readable labels, units, season, a caption stating a finding and limitation, and a brief explanation of its chart type and encoding. Keep comparable axes consistent. Do not use 3D effects or unexplained dual axes. Bar charts, if used in panels, start at zero. [3]

In an appendix, show an earlier version of one figure, identify two concrete design weaknesses and explain the changes. Use identical data in both versions. The earlier figure is additional to the three final figures. [1]

## Part D — Respect the independent unit [4 marks]

Estimate uncertainty for the mean-total difference with **2,000 bootstrap replicates and seed 854**. Resample unique eligible `match_id` values with replacement from their union. For each selected match, carry all its eligible team innings together, including repeated copies when selected more than once. This preserves any within-match dependence when the two teams face each other. Compute Islamabad-minus-Lahore means in each replicate. If a replicate contains no eligible innings for one team, discard it and redraw; report how many redraws occurred. Report the 2.5th and 97.5th percentiles of the 2,000 valid differences as a percentile interval. [2]

Explain why treating six overs from one innings as six independent matches would change the question and overstate information. Interpret the interval as uncertainty under this resampling procedure, not proof of a causal team effect or a guarantee about future seasons. [1]

Run one declared sensitivity check: lower-tail thresholds 35 and 45 instead of 40, with eligibility unchanged. Report all three rates by team and whether the substantive reliability conclusion changes. Keep 40 as the primary threshold; do not choose the most flattering one. [1]

## Part E — Write a decision and deliver reproducible evidence [4 marks]

In 350–500 words, give a verdict on the commentator's claim. Include three quantified findings: center, spread/tail, and uncertainty. If definitions disagree, report that disagreement. Distinguish description from explanation; discuss at least two material limitations such as opponents, venue, eligibility, coverage or small sample size. State one specific claim beginning **“I refuse to claim that…”** and name additional evidence needed to support it. Do not infer that team membership causes scoring differences. [2]

Your ZIP must include the supplied CSV and provenance, a notebook or script with saved outputs, `eligible_innings.csv`, `eligibility_audit.csv`, result tables, figures, README and package requirements. Use relative paths and run offline from a clean start. Cite Cricsheet, the lecture's preparation pipeline and external help. Include an AI assistance statement with what you checked yourself, or state that none was used. [2]

## Report and submission

Follow the portal's report-first format: **at most five A4 pages for the main report**, 11 pt font, margins at least 2 cm. Annexes have no page limit:

1. Introduction — the claim and why the distinction matters.
2. Problem — population, independent unit, primary effect and reliability definition.
3. Method — source, checks, eligibility, summaries and bootstrap.
4. Results — audit counts, distribution/effect tables, three final figures and sensitivity results.
5. Discussion — verdict, limitations, refused claim and further evidence.

Annex A: complete readable code. Annex B: data dictionary, audit details and chart redesign. Annex C: sources and assistance statement. Submit the PDF and ZIP separately; keep the ZIP below 10 MB. Every numerical claim must appear in a saved table or figure. This assignment's 20 marks do not announce or alter course assessment weights.

## Marking rubric

| Criterion | Marks | Evidence |
|---|---:|---|
| Framing and eligibility audit | 4 | Defined estimands, complete checks, justified exclusions and source tracing |
| Distribution summaries | 4 | Correct totals/statistics, denominators and comparison of aggregation choices |
| Visual argument | 4 | Three informative figures, captions, design reasoning and redesign |
| Independent units and sensitivity | 4 | Match-cluster bootstrap, correct interpretation and fixed threshold checks |
| Decision and reproducibility | 4 | Quantified verdict, limitations, offline workflow and attribution |
| **Total** | **20** | |

## Common mistakes

- Using the supplied lecture summary tables as your answer instead of calculating from over records.
- Replacing absent overs with zero or treating partial powerplays as complete.
- Comparing a per-over mean with a six-over total without identifying different units.
- Resampling overs independently or retaining only one team's innings from a sampled shared match.
- Calling the mean “reliability” without examining the predeclared lower-tail measure.
- Turning an observational comparison into a causal or future-season claim.

## Suggested timeline and checklist

By 4 October: frame the comparison and audit records. By 5–6 October: calculate summaries, figures, bootstrap and sensitivity. On 7 October: write, rerun and assemble the report. Submit by **8 October, 23:59 Pakistan time**. Late submissions follow the instructor's announced course policy.

- [ ] Eligibility includes all six complete overs and exclusions are documented.
- [ ] Statistics use the specified units, thresholds and conventions.
- [ ] Three final figures and one appendix redesign are included.
- [ ] Bootstrap resamples match IDs and retains all eligible innings in each selected match.
- [ ] Conclusions include quantified evidence, uncertainty and a refused claim.
- [ ] PDF meets the main-report page limit and ZIP runs offline.
- [ ] Source attribution and assistance disclosure are included.

This is individual work. You may discuss concepts; submitted code, calculations, figures and prose must be your own and explainable by you. Lectures 1–4 and their notebooks are the primary study references.
