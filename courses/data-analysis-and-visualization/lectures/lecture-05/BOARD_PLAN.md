# Lecture 5 board plan

**Medical Evidence — The Mathematics Behind the Chart**

180 minutes including a 15-minute break. Students calculate and sketch on paper. The instructor runs the notebook. This plan follows [SLIDES.md](SLIDES.md) and `lecture_5_live.ipynb`.

## Route and timing

| Minutes | Slides | Board / live notebook | Student work |
|---|---|---|---|
| 0–10 | 1–4 | Record initial votes on three pitches. Keep votes visible. | Verdict + one missing item per pitch |
| 10–20 | 5–8 | Measurement map, designs, source audit, HPS counts | State units, endpoint, denominator |
| 20–45 | 9–12, 18 | Boards 1, 2 and 4. Derive first, substitute second. | HPS risk, ARR, RR and SE |
| 45–65 | 13–17, 19–23 | Board 3. Run HPS chart cells. Slide 22 optional. | Sketch a repair and write its caption |
| 65–90 | 24–36 | Boards 5 and 6. Run HDL cells. Slides 29 and 35 optional. | HDL change, log-RR CI, outcome verdict |
| 90–105 | 37–38 | Board 7. Sketch ratio geometry. | Position 0.5, 1 and 2 on two scales |
| 105–120 | 39 | Break | |
| 120–145 | 40–49 | Boards 8 and 9. Run sugar cells. Slide 48 optional. | Normalize exposure, read full adjusted estimate |
| 145–155 | 50–51 | Write figure specification. Discuss separate panels. | Choose encoding, reference and caption |
| 155–175 | 52 | Workshop and evidence defense | Worksheet and evidence brief |
| 175–180 | 53–54 | Revisit initial votes. Exit ticket | Final finding with numerical support |

Slides 55–56 are reference pages. Four optional data extensions remain available for follow-up learning. The schedule groups derivation slides separately from visual-repair slides, so it deliberately revisits slide 18 during the first math block.

## Board layout

Left third: question, population, endpoint, units and comparison. Middle: derivation. Right third: substitution and plain-language finding. Erase the middle as needed. Keep the question and final findings visible. Keep the initial votes in a small separate area until the closing discussion.

## Board 1 — Why a proportion is an estimator

Let \(Y_i=1\) if a participant has the selected event, otherwise 0.

\[
Y_i\sim\operatorname{Bernoulli}(p),\quad E(Y_i)=p,\quad Y_i^2=Y_i.
\]

\[
\operatorname{Var}(Y_i)=E(Y_i^2)-E(Y_i)^2=p-p^2=p(1-p).
\]

\[
\hat p=\frac{1}{n}\sum_iY_i=\frac en,\qquad E(\hat p)=p.
\]

Before simplifying, show the covariance terms:

\[
\operatorname{Var}(\hat p)=\frac{1}{n^2}\left(\sum_i\operatorname{Var}(Y_i)+2\sum_{i<j}\operatorname{Cov}(Y_i,Y_j)\right).
\]

Under the independent-Bernoulli teaching approximation, the covariance terms vanish and \(\operatorname{Var}(\hat p)=p(1-p)/n\). Substitute \(\hat p\) to estimate the variance.

**Prompt:** Why does the denominator use assigned participants rather than number of events? Why cannot overlapping component outcomes be added?

## Board 2 — What benefit means numerically

Write treatment and control counts before introducing symbols:

\[
\hat p_T=2033/10269=0.1979745,\qquad \hat p_C=2585/10267=0.2517775.
\]

\[
ARR=\hat p_C-\hat p_T=0.0538031,\quad RR=\hat p_T/\hat p_C=0.7863072.
\]

\[
RRR=1-RR=0.2136928,\qquad 1000ARR=53.8031.
\]

**Finding:** About 54 fewer affected participants per 1,000 during HPS's scheduled five-year period. ARR = 5.38 percentage points. Count-based RRR = 21.4%. The published logrank event-rate reduction is approximately 24%, a different estimator.

**Prompt:** How can 5.38 and 21.4 both describe the same count-based result?

## Board 3 — How a baseline changes visible bar lengths

Use percentages throughout:

\[
\frac{p_C-b}{p_T-b}\bigg|_{b=19}=\frac{25.1778-19}{19.7974-19}\approx7.75,
\qquad\frac{p_C}{p_T}\approx1.27.
\]

Sketch the 19% baseline and the zero baseline. The former changes visible height ratios without changing the source values. Distinguish a bar's length encoding from a dot's position encoding. Show the exact axis edit in the notebook.

**Prompt:** Which quantity does 7.75 describe? It describes visible heights, not a risk ratio.

## Board 4 — Why an effect needs an interval

For independent arms:

\[
\operatorname{Var}(\hat p_C-\hat p_T)=\operatorname{Var}(\hat p_C)+\operatorname{Var}(\hat p_T).
\]

\[
\widehat{SE}(ARR)=\sqrt{\frac{\hat p_C(1-\hat p_C)}{n_C}+\frac{\hat p_T(1-\hat p_T)}{n_T}}=0.0058147.
\]

\[
ARR\pm1.96SE=[0.0424062,0.0651999].
\]

Per 1,000: estimate 53.8, approximate interval 42.4–65.2. Reference 0 = no absolute benefit. Explain the repeated-sampling confidence procedure. The normal curve is a sampling approximation, not a patient distribution or posterior.

## Board 5 — The summary operator matters

\[
100\frac{42-35}{35}=20\%.
\]

The source's 25% is the **median of individual percentage changes**. Write the operators explicitly:

\[
100\frac{\operatorname{median}(H_2)-\operatorname{median}(H_0)}{\operatorname{median}(H_0)}
\quad\ne\quad
\operatorname{median}\left(100\frac{H_{2i}-H_{0i}}{H_{0i}}\right)
\]

in general. Available visit samples also vary. We cannot reconstruct participant changes from group summaries. Show median/IQR versus outcome CI as distinct intervals with distinct questions.

## Board 6 — Deriving a log-RR confidence interval

\[
\log(\hat p)\approx\log(p)+\frac{\hat p-p}{p}.
\]

\[
\operatorname{Var}(\log\hat p)\approx\frac1{p^2}\operatorname{Var}(\hat p)=\frac{1-p}{np}.
\]

Substitute \(\hat p=e/n\) to obtain \(1/e-1/n\). For independent arms:

\[
SE(\log RR)=\sqrt{1/e_T-1/n_T+1/e_C-1/n_C}.
\]

For AIM-HIGH: \(e_T=282,n_T=1718,e_C=274,n_C=1696\).

\[
RR=1.0160176,\quad SE(\log RR)=0.0776147,
\]

\[
CI=\exp\{\log(RR)\pm1.96SE\}=[0.8726383,1.1829549].
\]

The source reports adjusted HR 1.02 (0.87–1.21). Keep that reported event-timing estimator separate. Nonzero counts and large samples support the teaching approximation. Crossing 1 does not demonstrate exact equality.

**Finding:** Niacin raised HDL but did not demonstrate added cardiovascular benefit in this setting.

## Board 7 — Ratio geometry

\[
u(r)=\log(r),\quad u(1)=0,\quad u(2)=-u(1/2),\quad u(r_2)-u(r_1)=\log(r_2/r_1).
\]

Sketch labeled **ratio** ticks 0.5, 1 and 2 at equal distances on the log axis. On a linear axis, the distances to 1 differ. Exponentiation maps a symmetric log interval into an asymmetric ratio interval. Difference reference = 0. Ratio reference = 1.

## Board 8 — Sugar exposure normalization

\[
S_\%=100\frac{4g_{added}}{E_{total}}.
\]

Invented arithmetic: 50 g / 2,000 kcal and 100 g / 4,000 kcal both yield 10%. Explicitly label both examples hypothetical.

Published quintile midvalues: 7.4, 11.4, 14.8, 18.7, 25.2%. Actual category bands are in the CSV. A midvalue is not a clinical threshold. Plot all groups at numeric positions. Q1 is the reference, with no CI estimated for it in the table.

**Finding:** Full-model Q5/Q1 cardiovascular-mortality HR = 2.03 (1.26–3.27). The reported adjustment includes total cholesterol. Both model versions are adjusted, and their difference does not isolate one covariate's contribution.

## Board 9 — Hazard versus cumulative risk

\[
R(t)=P(T\le t),\quad
h(t)=\lim_{\Delta t\to0}\frac{P(t\le T<t+\Delta t\mid T\ge t)}{\Delta t}.
\]

The denominator conditions on remaining event-free. A hazard is a rate, whereas cumulative risk is a probability.

Optional proportional-hazards extension, using cumulative hazard \(H\):

\[
S(t)=e^{-H(t)},\quad H_E(t)=HR\,H_{ref}(t),\quad S_E(t)=S_{ref}(t)^{HR}.
\]

\[
R_E(t)=1-[1-R_{ref}(t)]^{HR}.
\]

Any baseline risks shown in this illustration are hypothetical. Do not call these empirical NHANES survival curves. The cohort estimate does not identify why the association exists or establish a randomized intervention effect.

## Closing board — Publication recommendation

Keep the three findings separate, then connect them:

1. LDL is a causal contributor in broader evidence. HPS establishes a benefit from assigned LDL-lowering treatment.
2. HDL increased, but the niacin add-on did not demonstrate additional patient benefit in AIM-HIGH.
3. Higher added sugar retained an adjusted cardiovascular-mortality association, including adjustment for total cholesterol.

**Moral:** A single “good/bad” label or a sugar-versus-cholesterol contest hides the quantities and outcomes. The analyst can produce a reproducible, numerical conclusion, repair a misleading display, and specify what the editor can responsibly publish.

## Notebook route

Run setup and data audit first. Each named figure cell writes a PNG, SVG, and native-chart data descriptor. Use figures 01–09 for HPS, 10–20 for HDL and ratios, 21–27 for sugar, and 28 for the final evidence. Computed effect tables live in `outputs/`. The executed notebook remains available for students who do not run code in class.
