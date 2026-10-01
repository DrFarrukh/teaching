# Lecture 4 · Data acquisition and data quality

Why did local apples and imported iPhones both become expensive? Feeds, structured data, PDFs, official pages and browser collection; provenance and checksums; six data-quality dimensions; and stopping where the evidence stops.

| Slides | Notebook | Run the notebook |
|---|---|---|
| [PowerPoint (slides.pptx)](slides.pptx) | [notebook.ipynb](notebook.ipynb) | [Open in Google Colab](https://colab.research.google.com/github/DrFarrukh/teaching/blob/main/courses/tools-and-tech-in-data-science/lectures/lecture-04/notebook.ipynb) |

The notebook is saved with its outputs, so you can read it without running anything.

## Run it yourself

- **Google Colab:** open the link above and run the first code cell. It downloads this lecture's folder and installs the packages.
- **Locally:** from this folder, `python -m pip install -r requirements.txt`, then start Jupyter here and open `notebook.ipynb`. Paths are relative to this folder.

## Files

The notebook runs offline from saved snapshots in `data/`, each with its source URL, retrieval time and SHA-256. News records are feed metadata and short summaries, not full articles. `demo_browser.py` is the browser demo (practice sites only); its saved run is in `demo_output/`. Assignment 1 is in [`../../assignments/assignment-01/`](../../assignments/assignment-01/README.md).
