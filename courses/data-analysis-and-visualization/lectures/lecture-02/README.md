# Lecture 2 · Python, pandas and a real Excel workbook

Python basics, row and column selection, cleaning and reshaping one worksheet, a reusable function across all nineteen fiscal-year sheets, and validation against the source totals before saving.

| Slides | Notebook | Run the notebook |
|---|---|---|
| [PowerPoint (slides.pptx)](slides.pptx) | [notebook.ipynb](notebook.ipynb) | [Open in Google Colab](https://colab.research.google.com/github/DrFarrukh/teaching/blob/main/courses/data-analysis-and-visualization/lectures/lecture-02/notebook.ipynb) |

The notebook is saved with its outputs, so you can read it without running anything.

## Run it yourself

- **Google Colab:** open the link above and run the notebook from the top. The first code cell downloads this lecture's folder and installs the packages.
- **Locally:** from this folder, `python -m pip install -r requirements.txt`, then start Jupyter here and open `notebook.ipynb`.

## Files

`five-years-12.xlsx` is the unchanged PAMA source workbook. Running the notebook writes `data/passenger_cars_long.csv`, `data/validation.csv` and `data/conversion_issues.csv`. The openpyxl warning about a header/footer concerns print decoration and does not affect the cells read.
