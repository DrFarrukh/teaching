# CS-808 Tools and Technologies in Data Science

## Individual Assignment 1: Acquire a Dataset and Audit Whether It Can Be Trusted

| Item | Details |
|---|---|
| Release | After Lecture 4 (Thursday 1 October 2026) |
| Due | **Thursday 8 October 2026, 23:59 Pakistan time** |
| Mode | Individual take-home assignment |
| Maximum marks | 20 |
| Submit | **One PDF report** (`CS808_A1_<StudentID>.pdf`) and **one small ZIP** with your raw data snapshot (`CS808_A1_<StudentID>_raw.zip`) |
| Required tools | Python, Pandas, Matplotlib, Jupyter or any editor. `requests` for downloads; BeautifulSoup or browser automation only if no more direct permitted route exists |
| Optional starter | `CS808_A1_Starter/`: a scaffold of the workflow (folders, templates, an empty notebook). It contains **no solutions** |

## The question

In Lecture 4 every dataset loaded without an error, and yet each one was unfit for something. A feed returned HTTP `200` but its newest item was ten months old. An author column held `none@none.com (Name)`: a placeholder, not a null. A machine-readable feed was a month behind the PDF of the same statistic. The same year label meant *calendar year* in one source and *fiscal year* in another, so two official numbers for "2025" disagreed. A "fresh fruit" index stood in for apples, which were never measured. In each case the raw file, its provenance and its SHA-256 checksum let us show exactly what we had.

**The message: a dataset can load without error and still be unsuitable for the intended use.**

**Your task is to collect one dataset yourself, audit it, and decide in writing what it can and cannot be used for.** You are marked on the *evidence and the reasoning*, not on how large or exciting the dataset is. An honest "this data is not fit for that purpose, and here is the proof" earns full marks.

## Choose one source

Pick **one** option. Do not use Brent crude oil (the lecture's series) as your audited dataset.

| Option | Dataset | Minimum size | Notes |
|---|---|---|---|
| A | A numeric time series from **FRED** (any series except Brent crude oil; record the series ID) | At least 500 observations | Daily or weekly series suit best. |
| B | A **news-feed dataset**: items from the RSS/Atom feeds of at least **two outlets** whose terms allow automated reading of the feed | At least **100 unique items**, from **snapshots on at least 3 different days spanning at least 48 hours** | Feeds are rolling windows, so **start early** (see the timeline). Keep headline, link, time, category, author and the short summary only. The goal is to see rolling-window behaviour, repeated and new items, and stale feeds, not to maximise volume. |
| C | **World Bank** indicators for Pakistan and at least three comparison countries | At least 200 country-year values | Choose indicators carefully; definitions differ. |
| D | A **weather** record for one Pakistani city from a documented open API | At least 500 daily or 2,000 hourly values | Daily or hourly. |
| E | A source of your own choice | Comparable to the above | **Written approval from the instructor by email at least 3 days before the due date.** |

You are responsible for **documenting the source's licence or terms of use** (and, for a documented API, its rate limits). A source whose terms prohibit automated access is not allowed, however easy it looks. In particular, do **not** scrape the PSX Data Portal, Instagram or any site behind a login you do not own.

### Rules of polite collection (breaking them forfeits the acquisition marks)

1. **At most one request every 5 seconds to any one website or API host.** Different websites may be contacted in parallel; the same website may not.
2. Send an **honest `User-Agent`** that names the course and a contact email (where the service allows it).
3. If a site answers **HTTP 429 (Too Many Requests)**, stop, wait, and retry with a longer pause. Do not hammer it, rotate addresses or hide your identity.
4. **Check `robots.txt` where it is relevant**: when you read ordinary web pages or feeds from a website. For an official, documented API (FRED, World Bank and similar), the licence, terms and API documentation are what matter; you do not need to quote `robots.txt`.
5. **Never store full article text** from a news feed (some feeds include it). Headline, link, date, category, author and short summary only.
6. **Never put a password, API key or token** in your PDF, ZIP or code listing.
7. Save every response **exactly as received** (raw), and never edit that file.

## What to submit

### 1. The PDF report: `CS808_A1_<StudentID>.pdf`

The **analysis comes first; the code goes in the annex.** Main report: **at most 5 A4 pages**, 11 pt font, margins at least 2 cm. Then the annexes (no page limit for annexes). A skeleton is in `CS808_A1_Starter/report_structure.md`.

**Main report (pages 1-5)**

| Section | What it must contain | Guide |
|---|---|---|
| **1. Introduction** | The topic, why someone would use this data, and one sentence stating your option and source. | about 120 words |
| **2. Problem** | The exact question the data is meant to help answer (the *intended use*), and what "trustworthy for that use" would mean. State what would make you reject the data **before** you look at results. | about 150 words |
| **3. Method** | (a) Which rung of the acquisition ladder you used, **why it was the most direct permitted route**, and why a more fragile method such as HTML scraping or browser automation was unnecessary. (b) The exact steps: URL and parameters, request headers, pacing, what you did on errors, and how you checked the licence or terms (and `robots.txt` where relevant). (c) The raw snapshot and its checksum. (d) The quality checks you ran, grouped under the six dimensions, and **the rules you set before running them** (for example, "a daily value needs at least 20 of 24 hourly readings"). (e) Any cleaning, each step justified. | about 400 words + a short table of checks |
| **4. Results** | A **summary table of every check with its count** (at least 8 checks, covering all six dimensions); **at least two figures** made in Python (one that exposes a quality problem, one about the content); the three option-specific extras (below); and a ranked list of findings. At least **one finding must be something a null-count would not have caught.** | tables, figures, about 300 words |
| **5. Discussion** | Your verdict for the intended use: **Fit**, **Fit with stated caveats**, or **Not fit**, with the evidence. What the data can support; what it cannot; **one specific claim a careless analyst would make and you refuse to** (state it in a sentence beginning "I refuse to claim that..."); what additional data or checks would change your verdict; and any ethical or legal limit you respected. | about 250 words |

**Annexes**

| Annex | Contents |
|---|---|
| **A. Code** | The **complete** code, in the order it ran: collection, provenance record, checks, figures. It must run top-to-bottom, offline, from your raw snapshot. Comments explain *why*, not *what*. Use a monospaced font and keep lines readable. No keys or passwords. |
| **B. Provenance record and data dictionary** | The provenance record (see below) and a table of every column you used: name, type, unit, meaning, known problems. |
| **C. Sources, terms and assistance statement** | Every URL you used with the date you accessed it; the licence or terms wording you relied on (quote it, with its URL), and the `robots.txt` finding where relevant; and a statement of any AI tool or external code you used and **what you checked yourself**. |

### 2. The raw snapshot: `CS808_A1_<StudentID>_raw.zip` (at most 10 MB)

The untouched files exactly as received, a `provenance.json`, and your code as a `.py` or `.ipynb` file. Your code must run from this ZIP **without internet access**. (If a snapshot is larger than 10 MB, submit a deterministic sample and say so in Annex C.)

### The provenance record (Annex B and `provenance.json`)

Seven fields at minimum: **source URL · query parameters · retrieval time (UTC) · who or what retrieved it (your script name and `User-Agent`) · licence or terms (quoted) · SHA-256 checksum of each raw file · known limitations.** A template is in `CS808_A1_Starter/provenance_template.json`. For Option B, record **each snapshot** separately.

## Required analysis, by option

Everyone must complete the **core audit**. Then complete the **three extras** for your option. Every extra is a data-quality task and none needs text-analysis methods or special libraries.

### Core audit (all options)

1. **Uniqueness:** duplicate keys and duplicate records.
2. **Completeness:** missing values, **and missing rows** (a date, country or item that never appears is invisible to a null check, so compare the data against the full set of keys you expect).
3. **Validity:** impossible or meaningless values (negative prices, future dates, placeholder text such as `none@none.com`).
4. **Consistency:** units, scales, encodings, time zones, and definitions that differ across files, outlets or years.
5. **Timeliness:** how old is the newest item, when did the source say it was built, and is the data revised after publication?
6. **Representativeness:** who or what is *not* in the data, and what did your choice of source or filter exclude?
7. **Status is not quality:** state which of your checks would have passed even though the data was unfit (for example, a successful HTTP status or a clean download).

### Extras (three per option)

**Option A (FRED series)**
1. **Aggregation:** compare the raw frequency with a monthly or yearly aggregate and show what the aggregate hides; report the largest single-period changes.
2. **Units and adjustment:** state the unit and whether the series is seasonally adjusted, and what that does and does not allow you to claim.
3. **Gaps and revisions:** report gaps in the calendar and what the source says about revisions to published values.

**Option B (news feeds)**
1. **Freshness and timestamps:** the age of the newest item in each feed, the feed's own build date versus its newest item, and how date formats and time zones differ and were converted to UTC.
2. **New versus repeated across snapshots:** how many items are new, repeated, or gone between snapshots; duplicate links and repeated stories; malformed or placeholder fields. **State your rule for "repeated" before applying it, and manually inspect a small sample (up to 20) of the records it flags** to estimate its errors.
3. **Representativeness:** explain why the resulting feed dataset cannot automatically represent "the news", public opinion or the importance of any topic (which outlets, which window, headline and summary only).

**Option C (World Bank)**
1. **Definitions:** the indicator definition, base year and units, and whether they differ across countries or years.
2. **Missingness:** a full country-by-year grid showing which values are missing.
3. **Aggregation:** if you combine countries, show how a naive average differs from a population-weighted one; if neither is meaningful for your indicator, explain why not.

**Option D (weather)**
1. **Units and time zone:** the unit of each variable and how timestamps relate to local time.
2. **Daily values:** if you use hourly data, state your coverage rule **before** building daily values and keep failing days as missing; if the data are daily, document how the provider aggregated them.
3. **Representativeness:** what a grid-point or station value does and does not represent for the city.

**Option E:** agree three comparable extras with the instructor when you request approval.

## Marking rubric

| Criterion | Marks | Full-credit evidence |
|---|---:|---|
| Introduction and problem | 2 | A precise question, a stated intended use, and rejection criteria set **before** the results |
| Acquisition and provenance | 5 | The most direct permitted route, and why a more fragile one was unnecessary; licence or terms documented (and `robots.txt` where relevant); polite collection; raw snapshot kept; SHA-256 verified; complete provenance record |
| Quality audit | 6 | At least 8 explicit checks across all six dimensions with counts; missing rows (not only nulls) found; rules set before looking; one problem a null-count would not catch; status not treated as quality |
| Results and visualisation | 3 | At least two clear Python figures with titles, units and labels (one exposes a quality problem); the three extras done; findings ranked |
| Discussion and decision | 3 | A verdict (Fit, Fit with caveats, Not fit) supported by the evidence; a specific refused claim; limits and ethics stated honestly |
| Reproducibility and presentation | 1 | Code in Annex A runs offline from the ZIP; main report within 5 pages; annexes complete |
| **Total** | **20** | |

**What the top band looks like:** the report reads like something you could hand to a colleague who has never seen the data. Every number in the text appears in a table or figure, and every claim is limited to what the evidence supports. **What the bottom band looks like:** the dataset is downloaded, a few `.head()` and `.describe()` outputs are pasted in, and the conclusion is "the data is good".

## Common mistakes (each costs marks)

- Treating **HTTP 200**, or a download that "worked", as proof the data is correct or current.
- Counting only **blank cells** and never checking for **absent rows**.
- Choosing the pass/fail rules **after** seeing the results.
- Editing the raw file, or overwriting it with the cleaned version.
- Ignoring **units, time zones or definitions**, or confusing a **calendar year** with a **fiscal year**.
- Assuming a **category aggregate represents a specific item** (a fresh-fruit index is not an apple price).
- Reporting a **monthly mean** that hides the spike the question is about.
- Claiming **causation** from two series that move together.
- Using a source **outside its permitted terms**, or collecting faster than it allows.
- Putting **secrets or full copyrighted text** into the submission.
- A report that is a **code dump**: the analysis belongs in sections 1-5; the code belongs in Annex A.

## Suggested timeline

| When | What |
|---|---|
| Thursday 1 Oct (today) | Choose your option and read its licence or terms. **Option B students: take your first snapshot today or tomorrow (Friday 2 Oct).** |
| By Sunday 4 Oct | Options A, C, D: raw snapshot saved, provenance record drafted, terms documented. **Option B: second snapshot on a different day; the third at least 48 hours after the first and no later than Monday 5 Oct**, on at least three different calendar days. |
| Monday 5 - Tuesday 6 Oct | Quality checks, figures, findings. (Option B: audit once the third snapshot is saved.) |
| Wednesday 7 Oct | Write sections 1-5; assemble annexes; export to PDF; check the 5-page limit. |
| Thursday 8 Oct, 23:59 | Submit the PDF and the ZIP. |

Late submissions follow the course late policy announced by the instructor.

## Academic integrity

This is an individual assignment. You may discuss ideas, but the code, tables, figures and writing must be your own, and your data must be collected by you. You must declare any AI assistance or external code in Annex C **and state what you verified yourself**; an unverifiable claim in the report counts against you. Copying another student's snapshot, figures or text is treated as misconduct.

## Submission checklist

- [ ] I chose one option, **not Brent crude oil**, and documented the source's licence or terms myself (and its rate limits, if it is an API).
- [ ] I collected the data politely: at most one request every 5 seconds per host, an honest `User-Agent` where allowed, backoff on 429; I checked `robots.txt` **where relevant** (web pages or feeds, not official APIs).
- [ ] I saved the raw files exactly as received and recorded their SHA-256 checksums.
- [ ] My provenance record has all seven fields (Option B: one record per snapshot), and I quoted the terms I relied on.
- [ ] I met my option's minimum size (Option B: at least 100 unique items, two outlets, snapshots on at least 3 different days spanning at least 48 hours).
- [ ] I set my pass/fail rules **before** running my checks.
- [ ] My summary table has at least 8 checks across all six dimensions, and I looked for **missing rows**, not only nulls.
- [ ] I did not treat a successful HTTP status or download as evidence of quality.
- [ ] I found at least one problem that a null-count would not have caught.
- [ ] I completed my option's three extras.
- [ ] I have at least two Python figures, and one of them exposes a quality problem.
- [ ] My discussion gives a verdict (Fit, Fit with caveats, Not fit) and states one specific claim I refuse to make.
- [ ] The main report is at most 5 pages with the code in Annex A, and the code runs offline from my ZIP.
- [ ] No password, API key or full article text appears anywhere in my submission.
- [ ] I declared all AI or external-code help in Annex C and said what I verified.
