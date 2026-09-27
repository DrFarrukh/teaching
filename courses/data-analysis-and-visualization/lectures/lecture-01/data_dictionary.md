# Lecture 1 prepared data dictionary

## Source

`pama_monthly_production_sales.xlsx`

Pakistan Automotive Manufacturers Association monthly production and sales data:

https://pama.org.pk/monthly-production-sales-of-vehicles/

## passenger_cars_long.csv

| Column | Meaning |
|---|---|
| fiscal_year | Fiscal year worksheet label |
| date | First day of the represented fiscal month |
| manufacturer | Manufacturer normalized from the model label |
| model_group | Model label as presented in the source, with whitespace cleaned |
| measure | Production or Sales |
| units | Number of units recorded in the source cell |
| source_sheet | Original worksheet name |
| source_row | Original worksheet row number |

## annual_brand_sales.csv

| Column | Meaning |
|---|---|
| fiscal_year | Fiscal year |
| manufacturer | Normalized manufacturer |
| recorded_sales | Sum of twelve monthly passenger car sales records |

## annual_market_summary.csv

| Column | Meaning |
|---|---|
| fiscal_year | Fiscal year |
| total_recorded_sales | Sum of extracted passenger car sales |
| big_three_recorded_sales | Recorded sales for Suzuki, Toyota, and Honda |
| big_three_recorded_share | Big Three sales divided by total recorded passenger car sales |
| recorded_ev_sales | Sales in the separately reported Honri-Ve electric car row |
| recorded_ev_share | Recorded electric car sales divided by total recorded passenger car sales |

## source_total_validation.csv

This file compares the sum of the twelve extracted monthly values with the cached cumulative value in the source workbook. A zero difference supports extraction accuracy. It does not establish that the source covers the complete Pakistani market.

## Known limitations

- Manufacturer normalization uses model names in the workbook.
- Source labels and categories change across fiscal years.
- Combined model rows cannot be separated without another source.
- Recorded zeros may require source interpretation.
- The PAMA workbook should not automatically be treated as a census of all new vehicle sales in Pakistan.

