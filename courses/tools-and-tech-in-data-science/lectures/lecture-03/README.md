# Lecture 3 · Can airport weather fill gaps in Islamabad air-quality data?

Relational data, grain and keys, SQL with DuckDB alongside pandas, left joins, agreement between two weather sources, and a transparent, labelled candidate fill.

| Slides | Notebook | Run the notebook |
|---|---|---|
| [PowerPoint (slides.pptx)](slides.pptx) | [notebook.ipynb](notebook.ipynb) | [Open in Google Colab](https://colab.research.google.com/github/DrFarrukh/teaching/blob/main/courses/tools-and-tech-in-data-science/lectures/lecture-03/notebook.ipynb) |

The notebook is saved with its outputs, so you can read it without running anything.

## Run it yourself

- **Google Colab:** open the link above and run the first code cell. It downloads this lecture's folder and installs the packages.
- **Locally:** from this folder, `python -m pip install -r requirements.txt`, then start Jupyter here and open `notebook.ipynb`. Paths are relative to this folder.

## Files

`data/` holds the teaching CSVs and their provenance (`data/README.md`). Country boundaries are Natural Earth (public domain); the Islamabad basemap is © OpenStreetMap contributors © CARTO. Keep `lecture_visuals.py` beside the notebook.
