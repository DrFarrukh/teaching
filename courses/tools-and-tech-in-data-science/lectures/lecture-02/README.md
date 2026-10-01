# Lecture 2 · PM2.5 to a reproducible AQI dashboard

Auditing coverage, rolling means, implementing and testing a PM2.5 AQI function, comparing breakpoint rules and like periods, seasonality, and exporting a static Plotly dashboard.

| Slides | Notebook | Run the notebook |
|---|---|---|
| [PowerPoint (slides.pptx)](slides.pptx) | [notebook.ipynb](notebook.ipynb) | [Open in Google Colab](https://colab.research.google.com/github/DrFarrukh/teaching/blob/main/courses/tools-and-tech-in-data-science/lectures/lecture-02/notebook.ipynb) |

The notebook is saved with its outputs, so you can read it without running anything.

## Run it yourself

- **Google Colab:** open the link above and run the first code cell. It downloads this lecture's folder and installs the packages.
- **Locally:** from this folder, `python -m pip install -r requirements.txt`, then start Jupyter here and open `notebook.ipynb`. Paths are relative to this folder.

## Files

`data/raw/` holds the working CSVs; `dashboard/template.html` is the page template. Running the notebook writes `outputs/` and `docs/`. [Open the finished dashboard](https://drfarrukh.github.io/teaching/courses/tools-and-tech-in-data-science/lectures/lecture-02/dashboard/).
