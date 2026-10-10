# CS-808 Lecture 5 study guide

Read the 32-slide deck, then review the saved outputs in `notebook.ipynb`. Run the cells in order to repeat the parsing, data-quality checks, joins, grouping and reshaping. State the observation unit, key, missing-value policy and validation condition before each transformation.

The real inputs are unchanged Lecture 4 snapshots in `data/evidence/`. The 15-record failure laboratory is explicitly synthetic. Every persisted input is verified against its checksum. Review `DATA_DICTIONARY.md` and the source URLs in `data/evidence/acquisition_log.json` when interpreting results.

Use the **Open in Colab** link in the course page, or extract the student ZIP, install `requirements.txt` and start Jupyter from this lecture folder. Colab downloads the published inputs once; the local package runs offline. The notebook writes outputs into `outputs/`.

The laboratory yields 11 clean keys, 7 observed values, 3 quarantined records and 8 issue events; one confirmed copy is removed. The real monthly join has 36 rows and no unmatched oil values. Missing prices remain missing, and duplicate-key validation stops unsafe joins.

`METHODS_REFERENCE.md` summarizes pandas operations. Attempt `METHODS_PRACTICE.md` before reviewing the worked notebook examples. Practice is ungraded unless the instructor announces otherwise.
