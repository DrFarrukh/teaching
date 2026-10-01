# Data provenance — expanded Lecture 2

The `raw` folder contains byte-preserving copies of the two existing course files:
`Lecture 1/AQI_Data/AQI-Data-20-22.csv` and `AQI-Data-23.csv`.
Input SHA-256 hashes are recorded during execution in `outputs/run_manifest.json`.

The notebook reads original cell text, counts wholly blank rows, preserves the
filename and CSV line number, parses day-first dates explicitly, and converts
measurement columns. It never overwrites the raw files. The 2023 file has 40
wholly blank records; after their removal there are 1,154 observations.

Coverage: 2020 has 365/366 days (October 31 absent); 2021 and 2022 have 365/365;
2023 contains 59 days, January 1 through February 28. The original CSVs do not
include a station ID, license, acquisition date, or complete extraction history.

| Original column | Meaning / interpretation |
|---|---|
| Date | Reported day, day/month/year in the raw files |
| Temperature | Temperature, °C per existing course interpretation |
| Humidity | Relative humidity, % per existing course interpretation |
| NO2, SO2, PM2.5 | Concentrations, µg/m³ per existing course interpretation |

The CSV files themselves do not encode units or measurement averaging periods.
This teaching calculation assumes daily PM2.5 is a valid 24-hour concentration;
that assumption is not established by code-level validation. No original PDF
transcription verification or monitoring-site representativeness audit is claimed.

The main derived field `aqi` uses a fixed US EPA 2024 breakpoint scheme documented
in the May 2026 guidance; the label remains **provisional PM2.5-based AQI**.
`aqi_legacy` uses the older table with the same nearest-integer rounding so the
comparison isolates rule changes. No full multipollutant AQI is calculated.

Original source-data reuse terms are not recorded locally; check them before
external redistribution. The derived export retains provenance columns and the
method manifest. Files outside `raw`, including the earlier December-only subset,
belong to the previous short lecture and are not inputs to the expanded notebook.
