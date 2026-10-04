# Lecture 5 data dictionary

These files contain published aggregate study data. A row represents a study arm, a subgroup summary, a laboratory summary, or a model estimate. No row represents an individual patient.

## Sources

- HPS Collaborative Group (2002), [randomized trial report](https://doi.org/10.1016/S0140-6736(02)09327-3). High-risk UK adults, assigned simvastatin 40 mg daily or placebo, scheduled five-year treatment period.
- AIM-HIGH Investigators (2011), [randomized trial report](https://doi.org/10.1056/NEJMoa1107579). Patients with established cardiovascular disease and low HDL-C receiving intensive statin treatment, assigned niacin or placebo, mean follow-up three years.
- Yang et al. (2014), [NHANES linked-mortality cohort study](https://doi.org/10.1001/jamainternmed.2013.13563). Observational exposure to added sugar, cardiovascular mortality, median follow-up 14.6 years.

The student package distributes derived numerical tables and source links. Original reports remain available at the links above.

## trial_events.csv

Key: study, arm, outcome. `n` is the assigned participant denominator. `events` counts participants experiencing that specified endpoint. Endpoints reuse the same participants and can overlap. In AIM-HIGH, the secondary teaching rows use the tertiary counts in Table 4, which include events beyond the first composite event. Never add outcome rows to obtain the primary composite.

HPS major vascular events include major coronary events, stroke, and revascularization. AIM-HIGH's primary composite has a different definition. Group assignment remains the basis of comparison irrespective of adherence.

## hps_subgroups.csv

Key: partition, group, arm. `order` records the source's ordering. The LDL-C, HDL-C, age, and sex families each partition the full trial. Every family separately reproduces the overall counts. Adding different families would repeatedly count the same patients.

Lipid groups describe screening measurements before trial statin treatment. Comparisons of baseline lipid categories are observational even though treatment assignment within categories is randomized. The source's event-rate ratios use event timing. Notebook ratios use cumulative event proportions.

## aim_high_lipids.csv

Key: arm, analyte, year. All lipid units are mg/dL. `n_measured` identifies the available laboratory sample at that visit. `mean` and `sd` describe published means and standard deviations where available. `median`, `q1`, and `q3` describe published distribution summaries. Empty mean/SD cells for triglycerides are unreported summaries, not zeros.

The number measured declines with follow-up and trial scheduling. These aggregate summaries do not track an identical complete panel of individual patients. An IQR shows distributional spread. It is not a confidence interval on a median or treatment effect.

## aim_high_reported_changes.csv

The source reports the median of participants' individual HDL percentage changes at year two. This operator differs from the percentage change between the reported baseline and follow-up group medians. Individual change values cannot be recovered from the summary table.

## sugar_estimates.csv

Key: model, quintile. `midvalue_energy_pct` is the published quintile midvalue of usual added-sugar calories as a share of total calories. It is neither grams of sugar nor blood glucose. `exposure_band_pct` holds the actual category boundary.

`hr` is the published hazard ratio for cardiovascular mortality against Q1. `ci_low` and `ci_high` are published 95% confidence bounds. Q1 is the reference and has no estimated interval in this table. Both model versions include adjustment. The demographic model adjusts for age, sex, and race/ethnicity. The full reported model additionally includes education, smoking, alcohol, physical activity, family CVD history, antihypertensive medication, diet quality, BMI, systolic blood pressure, total serum cholesterol, and total calories.

The full model adjusts for total cholesterol, not separately for LDL-C and HDL-C. It does not remove every possible confounder or establish a randomized sugar intervention effect. Model fitting used the study's complex survey analysis and usual-intake methods. The teaching notebook reconstructs published estimates without claiming to refit that analysis.

## reported_effects.csv

Published event-timing estimates for comparison with our count-based calculations. `estimand` distinguishes the HPS logrank event-rate ratio from AIM-HIGH's adjusted HR. Never relabel either as the notebook's cumulative risk ratio.

## Measurement map

Cholesterol is a molecule. LDL and HDL are lipoprotein carriers. LDL-C and HDL-C quantify the cholesterol carried in their respective fractions. Total cholesterol combines fractions. Non-HDL-C equals total cholesterol minus HDL-C. Added-sugar intake is a dietary exposure. Fasting glucose and HbA1c measure aspects of blood glucose and are not substitutes for measured sugar consumption.

## Reproducibility

`dataset_manifest.json` records row counts and SHA-256 checksums. Original source locations remain attached to the tables.
