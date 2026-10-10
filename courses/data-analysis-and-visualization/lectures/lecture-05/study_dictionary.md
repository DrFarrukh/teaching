# Lecture 5 study and data dictionary

All tables contain extracted aggregate evidence. Original extracted values live in `data/`; computed results live in `outputs/`. No row is a reconstructed participant. Source links and extraction locations accompany every data row. Verification date: 7 October 2026.

## HPS

Heart Protection Study Collaborative Group (2002), randomized assignment to 40 mg daily simvastatin or placebo in 20,536 high-risk UK adults aged 40–80, with coronary disease, other occlusive arterial disease or diabetes. Follow-up was approximately five years.

Selected outcome: each participant's first major vascular event, a composite of major coronary events, stroke, or revascularization. Components overlap. Adding their counts double-counts people.

Extracted denominators and endpoint counts: simvastatin 2,033/10,269; placebo 2,585/10,267. These are assigned-arm counts. The class computes cumulative event proportions, their difference and ratio. These introductory binary-count summaries do not handle censoring or event timing as the original analysis does.

The paper's logrank event-rate ratio is 0.76 (95% CI 0.72–0.81). The simple count-based RR is approximately 0.786, so the count-based RRR is approximately 21.4%, compared with the reported 24% event-rate reduction. Keep estimator labels explicit. The treatment comparison directly concerns simvastatin assignment. The wider LDL causal conclusion uses the separate evidence synthesis in `sources.md`.

## AIM-HIGH

Randomized comparison of extended-release niacin versus placebo added to intensive statin therapy in patients with established atherosclerotic cardiovascular disease and low HDL-C. Ezetimibe could also be used to achieve the LDL target. Mean follow-up was three years, and the trial stopped for lack of efficacy.

Primary endpoint: first coronary heart disease death, nonfatal myocardial infarction, ischemic stroke, hospitalization for acute coronary syndrome, or symptom-driven coronary/cerebral revascularization.

Extracted counts: niacin 282/1,718; placebo 274/1,696. Original reported HR: 1.02 (95% CI 0.87–1.21). The class separately computes RR and its approximate interval from the counts. A nonsignificant superiority result does not establish equality, equivalence, or the absence of a biological role for HDL.

`hdl_summary.csv` includes only the documented niacin-arm medians: 35 mg/dL at baseline and 42 mg/dL at two years. The percentage change describes these two group medians. It is not the median of paired participant changes, an outcome effect, or a randomized between-arm contrast. The incomplete exhibit intentionally omits comparator biomarker data. Do not fill that gap with invented values.

## NHANES added-sugar mortality study

Yang et al. (2014) analyzed NHANES III linked mortality evidence for US adults aged at least 20. The mortality analysis included 11,733 participants and 831 CVD deaths, with median follow-up 14.6 years. The lecture reconstructs published Table 2 estimates without refitting the analysis.

Exposure: modeled usual percentage of total energy from added sugar. The authors used an NCI method with repeat dietary recall information to account for day-to-day measurement variation. Baseline exposure was not updated over follow-up. A single day's intake should not silently become usual long-term intake.

Table 2 evaluates estimated HRs at the 10th, 30th, 50th, 70th and 90th percentiles of the modeled exposure distribution, described as quintile midvalues. They are 7.4%, 11.4%, 14.8%, 18.7% and 25.2%. These are not category thresholds or a set of five individual observations. Q5 begins at 21.3%; 25.2% is its midvalue. Reference: Q1 midvalue 7.4%.

The **demographic** model adjusts for age, sex and race/ethnicity. The **full** model adjusts for those plus educational attainment, smoking, alcohol consumption, physical activity, family history of CVD, antihypertensive medication use, Healthy Eating Index score, body mass index, systolic blood pressure, total serum cholesterol, and total calories. Both models are adjusted. Total serum cholesterol is not a separate LDL-C and HDL-C adjustment, and model adjustment does not guarantee removal of all confounding.

The analysis uses Cox proportional hazards models and accounts for the complex survey design. The class plots the authors' estimates and intervals. It cannot reconstruct absolute survival probabilities, perform a participant-level analysis, or refit these models from the aggregate table. The primary source contains additional models and sensitivity analyses beyond this teaching selection.

## File schemas

| File | Key | One row represents | Main fields |
| --- | --- | --- | --- |
| `trial_events.csv` | study + arm | Randomized study arm | `n` assigned participants; `patients_with_event` endpoint count; `role` treatment/control; endpoint, follow-up, source |
| `hdl_summary.csv` | study + arm + months | Documented arm/time summary | `hdl_mg_dl` median concentration; `months` 0 or 24; statistic and source |
| `sugar_estimates.csv` | quintile + model | Published model estimate at an exposure midvalue | `midvalue_pct`, category description, model, HR, 95% limits, reference flag, endpoint and source |
| `reported_estimates.csv` | study + estimand | Published trial ratio summary | estimator type, estimate, 95% limits and source |
| `outputs/trial_calculations.csv` | study | Classroom count-based reanalysis | pT, pC, benefit-positive ARR, RR, RRR, approximate standard errors and intervals |

Sugar Q1 has HR 1 by definition. Its confidence-limit fields are blank, not zero-width estimated intervals. Nonreference intervals are positive and contain their estimates. Reference markers have no drawn error bars.

## Model assumptions and conventions

Binary-count inference assumes independent participants within arms, independent randomized arms and large samples. It estimates observed follow-up proportions, rather than original time-to-event estimators. The selected studies have nonzero event counts. The log-RR formula cannot be used without modification when an arm has zero events.

ARR means control minus treatment, so positive values mean benefit. Percentages and percentage points are distinct. Multiply ARR by 1,000 to express fewer affected participants per 1,000. A ratio's null is 1; a difference's null is 0. HR compares conditional event rates and does not directly provide an absolute event probability.
