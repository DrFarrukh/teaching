## 1. Can a correct visualization still mislead?

- Medical evidence: the mathematics behind the chart
- AI-854 · Lecture 5
- Cholesterol, HDL and added sugar
---

## 2. Three pitches for a health editor

- A: “Cholesterol is dangerous.”
- B: “Raising HDL protects the heart.”
- C: “Sugar is the culprit, so cholesterol was wrongly blamed.”
- For each pitch: initial verdict, missing evidence, and a figure you would need.
---

## 3. Funding and selected evidence

- A historical analysis documents an industry-funded review that emphasized fat and cholesterol and downplayed sucrose evidence.
- The sponsor helped shape the review and received drafts. The review omitted its funding disclosure.
- This motivates an evidence audit. The medical claims still need testing.
---

## 4. The measurements in the story

| Quantity | Unit or encoding |
| --- | --- |
| LDL-C / HDL-C | mg/dL |
| Cardiovascular endpoint | 0 or 1 per participant |
| Added sugar | % of total energy |
| Published HR | Dimensionless ratio |

- LDL-C and HDL-C measure cholesterol carried in different lipoprotein fractions.
- Total serum cholesterol and blood glucose are distinct laboratory measurements.
- Added sugar is a dietary exposure, expressed here as a percentage of energy.
- A biomarker change and a patient outcome answer different questions.
---

## 5. Study design sets the claim’s scope

| Evidence | Design | Classroom quantity |
| --- | --- | --- |
| HPS | Randomized trial | Risk difference and RR |
| AIM-HIGH | Randomized add-on trial | RR and published HR |
| NHANES | Observational cohort | Published adjusted HRs |

- Randomization supports a comparison of assigned treatments.
- A cohort model reports an association under its adjustment assumptions.
- Endpoint, population and follow-up must accompany the estimate.
---

## 6. HPS: participants and first events

| Assigned arm | Participants n | With major vascular event e |
| --- | --- | --- |
| Simvastatin | 10,269 | 2,033 |
| Placebo | 10,267 | 2,585 |

- Composite outcome: major coronary event, stroke or revascularization.
- Each affected participant contributes once to this composite. Component counts can overlap.
---

## 7. Binary outcomes estimate event risk

- Yᵢ = 1 if participant i experiences the selected event, otherwise 0
- p̂ = (1/n) Σᵢ Yᵢ = e/n
- E(Yᵢ) = p     Var(Yᵢ) = p(1 − p)
- E(p̂) = p
---

## 8. Variance of an estimated risk

- Var(p̂) = Var(ΣᵢYᵢ)/n²
- Independence removes the covariance terms
- Var(p̂) = np(1 − p)/n² = p(1 − p)/n
- Estimated SE(p̂) = √[p̂(1 − p̂)/n]
---

## 9. Absolute and relative effects

- ARR = p̂C − p̂T
- RR = p̂T / p̂C     RRR = 1 − RR
- 1000 × ARR estimates fewer affected people per 1,000
- ARR has probability units. RR and RRR are ratios.
---

## 10. HPS: the hand calculation

- Simvastatin: 2,033 / 10,269 = 19.80%
- Placebo: 2,585 / 10,267 = 25.18%
- ARR = 5.38 percentage points
- RR = 0.786     RRR = 21.4%
---

## 11. An interval for absolute benefit

- SE(ARR) = √[p̂C(1 − p̂C)/nC + p̂T(1 − p̂T)/nT]
- Approximate 95% CI = ARR ± 1.96 × SE(ARR)
- HPS: 4.24 to 6.52 percentage points
- About 54 fewer affected people per 1,000 (interval 42–65)
---

## 12. A shortened baseline exaggerates length

![A shortened baseline exaggerates length](public/figures/02_hps_truncated_bars.svg)

- At a 15% baseline, visible heights have ratio 2.12
- The actual control/treatment risk ratio is 1.27
- Apparent ratio = (p̂C − b) / (p̂T − b)
---

## 13. A repair follows the encoding

![A repair follows the encoding](public/figures/03_hps_repaired_encodings.svg)

- Zero-baseline bars preserve magnitude through length.
- Restricted-axis dots can expose a small difference through position.
- Axis labels and the comparison’s units stay visible.
---

## 14. Absolute benefit on a common denominator

![Absolute benefit on a common denominator](public/figures/01_hps_absolute_benefit.svg)

- Approximately 198 versus 252 affected participants per 1,000
- Estimated benefit: 53.8 per 1,000
- The display scales the observed risks to equal denominators.
---

## 15. The HPS caption and causal scope

- Assignment to simvastatin reduced major vascular events by 5.38 percentage points during approximately five years.
- The count-based estimate uses affected participants and assigned-arm denominators.
- Wider evidence supports LDL as a causal contributor to atherosclerotic disease.
---

## 16. HDL: a biomarker pitch

![HDL: a biomarker pitch](public/figures/05_hdl_incomplete_exhibit.svg)

- Median HDL-C in the niacin arm rose from 35 to 42 mg/dL at two years.
- (42 − 35) / 35 = 20%
- What evidence would connect this rise to protection?
---

## 17. AIM-HIGH: the clinical outcome

| Assigned add-on | Participants n | With primary endpoint e |
| --- | --- | --- |
| Niacin | 1,718 | 282 |
| Placebo | 1,696 | 274 |

- Niacin arm risk = 16.41%     Placebo arm risk = 16.16%
- Both groups received intensive statin treatment.
- The primary endpoint is a composite cardiovascular outcome.
---

## 18. The delta method for log risk

- log(p̂) ≈ log(p) + (p̂ − p)/p
- Var(log p̂) ≈ Var(p̂)/p² = (1 − p)/(np)
- Substitute p̂ = e/n: estimated variance = 1/e − 1/n
- Independent arms: variances add for log(RR)
---

## 19. A confidence interval for a risk ratio

![A confidence interval for a risk ratio](public/figures/07_aim_ratio_intervals.svg)

- SE(log RR) = √[1/eT − 1/nT + 1/eC − 1/nC]
- Log interval: log(RR) ± 1.96 × SE(log RR)
- Exponentiating both limits returns the ratio scale.
- AIM-HIGH count-based RR: 1.016 (0.873–1.183)
---

## 20. An interval crossing 1 leaves uncertainty

- The trial did not demonstrate additional clinical benefit from the niacin add-on.
- Its reported HR interval spans 0.87–1.21.
- Compatible effects include some benefit and some harm.
- An equivalence claim requires a defined margin and suitable analysis.
---

## 21. Logarithmic ratio geometry

![Logarithmic ratio geometry](public/figures/08_ratio_geometry.svg)

- u(r) = log(r)     u(1) = 0
- u(2) = −u(1/2)
- u(r₂) − u(r₁) = log(r₂/r₁)
- Ratio plots use reference 1. Difference plots use reference 0.
---

## 22. Checkpoint and 15-minute break

- 1. Why do bars and restricted-axis dots require different baseline decisions?
- 2. Why does the HDL rise fail to establish a treatment benefit?
- 3. Place 0.5, 1 and 2 on a log-ratio axis.
- Break: minutes 105–120
---

## 23. Added sugar as a share of energy

- S% = 100 × (4 × grams of added sugar) / total kcal
- 50 g at 2,000 kcal = 10%
- 100 g at 4,000 kcal = 10%
- These two diets are invented arithmetic examples.
---

## 24. Cumulative risk and hazard

- Risk by time t: P(T ≤ t)
- Hazard: event rate at t conditional on survival to t
- h(t) = limΔt→0 P(t ≤ T < t + Δt | T ≥ t) / Δt
- HR(t) = hE(t) / hR(t)
---

## 25. Two selected points make an incomplete pitch

![Two selected points make an incomplete pitch](public/figures/09_sugar_selected_endpoints.svg)

- Q5 versus Q1: reported full-adjustment HR = 2.03
- The pitch hides intermediate exposure summaries and interval width.
- Which visual omissions could turn this association into advice?
---

## 26. The full sugar evidence

![The full sugar evidence](public/figures/10_sugar_full_evidence.svg)

- Numeric exposure positions preserve unequal spacing.
- Intervals show precision at each reported midvalue.
- Q1 is the reference. Its marker has no fabricated interval.
- Q5’s 25.2% is a midvalue. Its category starts at 21.3%.
---

## 27. Both published adjustment models

![Both published adjustment models](public/figures/11_sugar_model_comparison.svg)

- The first model adjusts for age, sex and race/ethnicity.
- The full model adds behavioral, clinical and dietary covariates.
- Full adjustment includes total serum cholesterol.
- A changed estimate alone cannot identify which covariate caused it.
---

## 28. The sugar finding’s scope

- Higher modeled usual added-sugar intake remained associated with higher CVD mortality after full adjustment.
- Residual confounding and changing intake limit causal interpretation.
- Total serum cholesterol adjustment does not equal adjustment for LDL-C and HDL-C separately.
- This association does not erase the randomized treatment evidence.
---

## 29. A visualization specification

- Question: what comparison should the reader make?
- Quantity and encoding: risk difference, ratio, concentration or exposure
- Scale and reference: zero for differences, one for ratios
- Uncertainty and caption: study design, endpoint, comparison and period
---

## 30. Color, units and captions

- Direct labels preserve meaning when color disappears.
- HDL concentration and event risk need separate axes and panels.
- An interval belongs beside its estimate and null reference.
- A caption states the finding and the evidence that supports its scope.
---

## 31. Evidence workshop: one pitch to repair

- 5 min: calculate an effect and identify the omission
- 7 min: sketch a repaired figure with labeled units and reference
- 5 min: write the finding, numerical evidence and study scope
- 3 min: defend the repair against a reviewer challenge
---

## 32. Reviewer challenges

- “Your figure shows a biomarker change. Where are the clinical outcomes?”
- “Your interval crosses the null. Why does the caption claim equality?”
- “Your sugar plot shows only Q1 and Q5. What did you omit?”
- “Your axes show different quantities. Why are you ranking them?”
---

## 33. Three findings with separate scopes

![Three findings with separate scopes](public/figures/12_final_evidence.svg)

- HPS: treatment benefit on an absolute scale
- AIM-HIGH: reported outcome HR with its interval
- NHANES: adjusted cohort association across exposure summaries
---

## 34. The editor’s publication brief

- HPS: about 54 fewer affected people per 1,000 during approximately five years.
- AIM-HIGH: the niacin add-on did not demonstrate additional clinical benefit in the studied setting.
- NHANES: the positive sugar association remained after full adjustment.
- Publish the specific results and replace the single-culprit headline.
---

## 35. Exit ticket

- 1. Translate the HPS absolute benefit into affected people per 1,000.
- 2. Explain why improved HDL does not establish protection.
- 3. Explain why the sugar association does not acquit LDL.
- 4. Give the null reference for a difference and for a ratio.
---

## 36. Sources and further reading

- HPS Collaborative Group (2002), Lancet 360:7–22
- AIM-HIGH Investigators (2011), NEJM 365:2255–2267
- Yang et al. (2014), JAMA Internal Medicine 174:516–524
- Ference et al. (2017), European Heart Journal 38:2459–2472
- Kearns et al. (2016), JAMA Internal Medicine 176:1680–1685
