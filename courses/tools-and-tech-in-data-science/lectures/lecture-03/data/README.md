# Lecture 3 data and provenance

The two teaching CSVs contain source columns only. Their dates are converted to ISO `YYYY-MM-DD`; missing numeric cells remain blank. No dates are invented and no measurement is filled with zero.

| File | Source | Grain | Key | Rows |
|---|---|---|---|---:|
| `epa_daily.csv` | `new_data.csv` | one air-quality record per reported date | `date` | 2,555 |
| `meteostat_temp_humidity_daily.csv` | `raw/meteostat_daily_weather.csv` | one weather summary per reported date | `date` | 2,946 |

The air-quality input has `Date`, `Temperature`, `Humidity`, `NO2`, `SO2`, and `PM2.5`. We renamed the temperature and humidity columns to `epa_temperature_c` and `epa_humidity_pct` to keep them distinct from Meteostat weather. The pollutant columns are `no2_ug_m3`, `so2_ug_m3`, and `pm25_ug_m3`; these units follow the research file's working interpretation and should be checked against the original source before publication. The source CSV does not include a monitoring station identifier or coordinates. Pak-EPA's published yearbook describes its fixed air-quality station in H-8/2, Islamabad.

The weather input comes from the separately downloaded Meteostat daily file, derived in the research workflow from hourly values for station 41571, Islamabad Airport. This lecture retains only `Meteostat_Temp_Mean` and `Meteostat_RH_Mean` as `meteostat_temperature_c` and `meteostat_humidity_pct`. The original 33-column weather file is kept under `raw/` for reproducibility. The teaching CSVs have unique dates; the code checks that assumption before writing them.

The EPA date range is 2018-05-17 to 2026-08-31, with gaps. The weather file has the same endpoints and its own gaps. Exactly 2,472 dates appear in both files; 83 EPA dates have no weather row. Fifteen EPA rows have a blank PM2.5 value. A left join from EPA to weather retains 2,555 dates. The research result `complete_epa_meteostat_ml_ready.csv` (not included in this public copy) has 3,029 dates because its pipeline first creates a complete daily calendar and then joins both sources. That file also contains feature engineering and is a reference output, not a join input.

Joining by date aligns calendar days, but the air-quality input itself does not identify exact sensor coordinates or measurement protocol. The two named sites are different. Do not present the joined values as colocated measurements or infer weather causes pollution changes from this descriptive exercise. Source references: [Pak-EPA 2022–23 yearbook](https://environment.gov.pk/SiteImage/Publication/Year%20Book%202022-23.pdf); [Meteostat station 41571](https://meteostat.net/en/station/41571).
