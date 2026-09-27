# Lecture 1: Data and evidence

**Question:** Can the data show whether Pakistan’s Big Three are losing dominance?

## Materials

- [Present the Reveal.js slides](revealjs/README.md)
- [Open the slide source](slides.md)
- [Open the detailed notebook](lecture_demo_detailed.ipynb)
- [Open the compact notebook](lecture_demo.ipynb)
- [View the student evidence pack](student_evidence_pack.html)
- [View the projected group activity](projected_activity.md)
- [View the exit ticket](exit_ticket.md)
- [Read the data dictionary and limitations](data_dictionary.md)

## Run the notebook locally

Use Python 3.10 or newer, install the packages in `requirements.txt`, then open either notebook in Jupyter. The original workbook and prepared CSV files are included in `data/` and `pama_monthly_production_sales.xlsx`. The notebooks read prepared files from `data/`; `prepare_data.py` rebuilds those CSV files from the workbook.

```bash
python -m pip install -r requirements.txt
python prepare_data.py
```

The analysis describes the records represented in the PAMA passenger-car workbook. It should not be interpreted as a census of every vehicle sold in Pakistan. Source and limitations are documented in [data_dictionary.md](data_dictionary.md).
