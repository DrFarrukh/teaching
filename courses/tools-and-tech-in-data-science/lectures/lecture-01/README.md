# Lecture 1 · Data science as a complete workflow

From difficult PDFs (text extraction, table extraction, OCR) to validated CSVs and a ladder of pollutant plots; measured concentration versus derived AQI; joining Meteostat weather by local date.

| Slides | Notebook | Run the notebook |
|---|---|---|
| [PowerPoint (slides.pptx)](slides.pptx) | [notebook.ipynb](notebook.ipynb) | [Open in Google Colab](https://colab.research.google.com/github/DrFarrukh/teaching/blob/main/courses/tools-and-tech-in-data-science/lectures/lecture-01/notebook.ipynb) |

The notebook is saved with its outputs, so you can read it without running anything.

## Run it yourself

- **Google Colab:** open the link above and run the first code cell. It downloads this lecture's folder and installs the packages.
- **Locally:** from this folder, `python -m pip install -r requirements.txt`, then start Jupyter here and open `notebook.ipynb`. Paths are relative to this folder.

## Files

`AQI_Data/` holds the Pak-EPA monthly report PDFs and working CSVs. The weather cell downloads live data from Meteostat; its merged result is saved in `outputs/`. OCR needs the Tesseract program as well as `pytesseract` (the Colab cell installs it).
