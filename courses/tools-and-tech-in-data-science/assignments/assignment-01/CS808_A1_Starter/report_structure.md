# Report structure (main report: at most 5 A4 pages, 11 pt, margins at least 2 cm)

Analysis first, code in the annex. These are prompts for what each section must contain, not model answers.

## 1. Introduction (about 120 words)
The topic; why someone would use this data; one sentence naming your option and source.

## 2. Problem (about 150 words)
The exact question the data should help answer (the *intended use*). What would "trustworthy for that use" mean? **What would make you reject the data, written before you saw any results.**

## 3. Method (about 400 words + a short table of checks)
- The acquisition rung you used, why it was the most direct permitted route, and why a more fragile route (HTML scraping, browser automation) was unnecessary.
- The exact steps: URL and parameters, headers, pacing, what you did on errors, how you checked the licence or terms (and `robots.txt` where relevant).
- The raw snapshot(s) and checksum(s).
- The checks, grouped under the six dimensions, and the **rules you set before running them**.
- Any cleaning, each step justified.

## 4. Results (tables, figures, about 300 words)
- A summary table of every check with its count (at least 8 checks, all six dimensions).
- At least two figures (one exposes a quality problem; one is about the content).
- Your option's three extras.
- Ranked findings, including at least one that a null-count would not have caught.

## 5. Discussion (about 250 words)
- Verdict for the intended use: **Fit**, **Fit with stated caveats** or **Not fit**, with the evidence.
- What the data can support; what it cannot.
- **"I refuse to claim that ..."**: one specific claim a careless analyst would make.
- What additional data or checks would change your verdict; any ethical or legal limit you respected.

## Annexes (no page limit)
- **A. Code**: the complete code, in the order it ran; runs offline from your raw snapshot; no keys.
- **B. Provenance record and data dictionary**: all seven provenance fields (Option B: per snapshot); every column you used (name, type, unit, meaning, known problems).
- **C. Sources, terms and assistance statement**: every URL with its access date; the licence or terms wording you relied on, quoted with its URL (and the `robots.txt` finding where relevant); any AI tool or external code you used and what you checked yourself.

## Before you export to PDF
Page count (main report at most 5); every number in the text appears in a table or figure; figures have titles, units and labels; nothing from a secret (keys, passwords) or full copyrighted article text appears anywhere.
