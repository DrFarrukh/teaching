# Lecture 5 student guide

The class follows three pitches submitted to a health editor. Your task is to reconstruct the evidence, repair the figures and write findings that the study designs support.

Bring paper and a calculator. Laptops are optional. The instructor runs the notebook while you predict, calculate, interpret and defend. You can review the executed notebook after class. The optional practice notebook extends the same authentic aggregate evidence and is ungraded unless the instructor says otherwise.

## What to read and use

- `evidence_pack.md` or the printable worksheet: calculations, figure sketches and exit ticket.
- `slides.pdf`: study copy of the 36 teaching slides.
- `notebook.ipynb`: all computations and figures with stored outputs.
- `study_dictionary.md`: populations, outcomes, observation units and model definitions.
- `sources.md`: primary-source links and extracted values.

## Core quantities

Event risk p = events / participants. Absolute benefit ARR = pC−pT. RR = pT/pC. Relative reduction RRR = 1−RR. Multiply ARR by 1,000 for fewer affected people per 1,000. An ARR of 0.0538 means 5.38 percentage points, not 5.38% relative reduction.

An approximate difference interval uses ARR ±1.96 SE. A count-based ratio interval uses log RR ±1.96 SE(log RR), then exponentiates both limits. Differences use reference 0, ratios reference 1. An interval crossing the null does not establish exact equality.

Risk describes a cumulative probability over a period. Hazard describes an instantaneous event rate among those still at risk. Published adjusted HRs cannot alone tell you an absolute event probability.

## Visual audit

Name the question and quantity. Identify whether the reader compares position, length or area. Check denominators, baseline, reference, units, uncertainty and omitted groups. Read the caption against the study design.

The HPS calculation directly compares assignment to simvastatin with placebo. The HDL exhibit gives a within-arm biomarker summary, while AIM-HIGH tests clinical outcomes under a randomized add-on treatment. The sugar table reports an adjusted cohort association. These three studies have different endpoints and cannot be pooled or ranked by their displayed effect sizes.

## Optional Python practice

With Python 3.10 or later, create a virtual environment, install `requirements.txt`, start JupyterLab inside the extracted lecture folder and open `practice.ipynb`. Keep the `data/` folder beside it. The source tables and slides work offline. Attempt each exercise before consulting the executed reference.
