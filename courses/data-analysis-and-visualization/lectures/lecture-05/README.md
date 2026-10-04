# Lecture 5 · Medical Evidence — The Mathematics Behind the Chart

Does cholesterol harm the heart? Does raising HDL protect patients? Does the added-sugar evidence overturn the LDL finding? We answer these questions using three authentic studies, worked mathematics, and 28 visualizations.

| Slides | Notebook | Run the notebook |
|---|---|---|
| [PowerPoint](slides.pptx) · [Slide manuscript](SLIDES.md) | [Notebook with saved outputs](notebook.ipynb) | [Open in Google Colab](https://colab.research.google.com/github/DrFarrukh/teaching/blob/main/courses/data-analysis-and-visualization/lectures/lecture-05/notebook.ipynb) |

The notebook is saved with its outputs so you can read it without running code. The slides include intentionally incomplete exhibits, followed by corrected figures and explicit conclusions. Source links are in the notebook, PowerPoint notes, and [data dictionary](data_dictionary.md).

## What you will do

Calculate event risk, absolute benefit, risk ratios and confidence intervals. Derive the variance of a proportion and the log-risk-ratio interval. Compare visual encodings, zero and restricted baselines, absolute and relative effects, IQR and confidence intervals, linear and logarithmic scales, and risk versus hazard. Repair one pitch in the [evidence workshop](STUDENT_WORKSHEET.md).

## The evidence closes the story

HPS demonstrates fewer major vascular events with assigned LDL-lowering treatment. AIM-HIGH increased HDL with niacin without demonstrating additional cardiovascular benefit in its studied setting. Higher added sugar retained an adjusted cardiovascular-mortality association, including adjustment for total cholesterol. “Sugar versus cholesterol” is a false choice. Preserve each study’s design, population, endpoint and comparison when stating its finding.

## Run it yourself

- **Google Colab:** open the link above and run from the first cell. It clones this repository and installs the packages.
- **Locally:** open this folder, run `python -m pip install -r requirements.txt`, and start Jupyter here.

`data/` holds verified published aggregate numerical tables. These rows are study-arm summaries, laboratory summaries, subgroup summaries, or published estimates. They are not individual patient records. `outputs/figures/` holds PNG and SVG figures. Running the notebook regenerates figures and calculated results.

[Board plan with worked derivations](BOARD_PLAN.md) is available for revision. The PowerPoint has 56 slides, including four optional data extensions and two reference pages.
