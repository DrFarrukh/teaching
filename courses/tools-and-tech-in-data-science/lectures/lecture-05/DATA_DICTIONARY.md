# Lecture 5 data dictionary

The `data/evidence/` folder contains unchanged frozen inputs acquired and audited in Lecture 4. The notebook checks their original SHA-256 manifest before analysis. These are saved snapshots; running the lecture does not request updated economic data.

| File | Observation and units |
| --- | --- |
| `worldbank_pk_annual.csv` | Pakistan calendar-year inflation (%) and average exchange rate (PKR/USD) |
| `fred_brent_daily_usd.csv` | Reported observation date and Brent spot quote (USD/barrel); blank quotes are missing |
| `pbs_cpi_monthly.csv` | Indicator and month; CPI index with 2015–16 = 100 |
| `iphone_launch_comparison.csv` | Launch year/model; USD price, same-day PKR/USD and mechanical pre-tax PKR floor |
| `pbs_fresh_fruit_layers.csv` | CPI/WPI fresh-fruit basket, month, index level and published year-on-year change |
| `acquisition_log.json` | Source URLs, retrieval records, units, grain and limitations |
| `evidence_manifest.json` | Original SHA-256 checksums for the evidence files |

`data/practice_prices_raw.csv` and `data/category_lookup.csv` are synthetic teaching fixtures. Their values are invented and are not official CPI. The failure laboratory distinguishes missing values, malformed tokens, invalid dates, confirmed copies and unresolved key conflicts.

Output files contain clean laboratory records, quarantined records, issue events and the monthly CPI/oil join. Index levels and USD/barrel remain separate quantities. CPI basket changes do not measure the price of an individual apple. The iPhone pre-tax floor does not establish a Pakistan retail price. Grouping and joining these series establish no causal inflation estimate.
