# Data Analysis and Visualization

## Lecture 1 · Data, evidence, and market-share claims

**Question:** Did Suzuki, Toyota, and Honda lose dominance in the passenger-car sales recorded in the PAMA workbook?

The answer depends on the population and denominator being measured.

---

# Start with a precise claim

“Dominance” is made measurable here as the **combined share of recorded passenger-car sales** for Suzuki, Toyota, and Honda.

A lower combined share over time would support a claim that their position weakened **within these records**.

It would not, by itself, explain why the share changed or establish the share of every car sold in Pakistan.

---

# The population and the records are different

| Term | Meaning in this analysis |
|---|---|
| Intended population | All new passenger cars sold in Pakistan |
| Observed records | Passenger-car production and sales rows found in the PAMA workbook |
| Denominator used | Total passenger-car sales recorded in the workbook for a fiscal year |

The workbook is a reporting frame. It is not documented here as a complete census of every seller, import, or vehicle registration.

---

# Source and time span

The source is PAMA’s monthly production and sales workbook, organized into fiscal-year worksheets.

- 19 fiscal years, from **2007–08 through 2025–26**
- 12 fiscal months per year, from July through June
- Separate production and sales measures
- Passenger-car model rows with labels and layouts that vary over time

The prepared data preserves fiscal year, date, manufacturer, model group, measure, units, and source location.

---

# What one prepared row represents

A row in the long-format table represents one recorded value for:

**model group × fiscal month × measure**

| fiscal year | date | manufacturer | model group | measure | units |
|---|---|---|---|---|---:|
| 2025–26 | 2025-07-01 | Honda | Honda Cars | Sales | 1,143 |

Keeping production and sales in a `measure` column prevents the two quantities from being added together by mistake.

---

# From a worksheet to an analysis table

A source worksheet stores months across columns. The analysis table stores one month per row.

| Source row | July | August | September |
|---|---:|---:|---:|
| Honda Cars · Production | 1,169 | 968 | 1,939 |
| Honda Cars · Sales | 1,143 | 699 | 1,977 |

The prepared rows retain the date, manufacturer, model group, measure, and value for each month. This structure makes filtering and grouping explicit.

---

# Check the extraction before interpreting it

| Check on prepared records | Result |
|---|---:|
| Long-format rows | 4,560 |
| Missing values | 0 |
| Duplicate records using the proposed key | 0 |
| Monthly source-total comparisons | 380 |
| Comparisons with a nonzero difference | 0 |

These checks support the accuracy of the workbook extraction. They cannot show that the workbook includes every seller in the intended population.

---

# Aggregate sales before calculating shares

For manufacturer $m$ in fiscal year $t$, add its recorded sales rows:

$$S_{m,t}=\sum_{j\in(m,t,\,\mathrm{Sales})} \mathrm{units}_j$$

Then add the recorded manufacturer totals to get the workbook denominator:

$$T_t=\sum_m S_{m,t}$$

A manufacturer’s recorded share is $S_{m,t}/T_t$. All manufacturers in a year use the same denominator.

---

# Define the Big Three concentration ratio

The three manufacturers are Suzuki, Toyota, and Honda. Their combined recorded share is the **CR3**:

$$\mathrm{CR3}_t=\frac{S_{\mathrm{Suzuki},t}+S_{\mathrm{Toyota},t}+S_{\mathrm{Honda},t}}{T_t}$$

This is equivalent to adding their individual shares because those shares use the same denominator.

CR3 describes concentration in the recorded passenger-car sales; it does not identify causes or market coverage.

---

# Worked calculation · fiscal year 2025–26

Recorded sales by the three manufacturers:

$$91{,}634+35{,}831+24{,}416=151{,}881$$

Total recorded passenger-car sales: **155,631**

$$\mathrm{CR3}=\frac{151{,}881}{155{,}631}=0.9759\approx97.6\%$$

The remaining recorded sales are 3,750, or about 2.4% of this denominator.

---

# The latest recorded manufacturer shares

| Manufacturer or group | 2025–26 recorded sales | Share of 155,631 |
|---|---:|---:|
| Suzuki | 91,634 | 58.88% |
| Toyota | 35,831 | 23.02% |
| Honda | 24,416 | 15.69% |
| All other recorded manufacturers | 3,750 | 2.41% |

The three named shares sum to **97.59%**. The values describe records in the workbook, not a verified national-market total.

---

# Recorded passenger-car sales vary sharply by year

![Annual passenger-car sales recorded in the workbook](public/outputs/annual_total_sales.png)

Recorded sales peak at **234,180 in 2021–22**, fall to **81,579 in 2023–24**, and rise to **155,631 in 2025–26**. The workbook describes the pattern; it does not establish its causes.

---

# How the recorded CR3 changed

![Big Three share of recorded passenger-car sales by fiscal year](public/outputs/big_three_share.png)

CR3 was **91.2% in 2007–08**, reached **100% in 2017–18**, and was **97.6% in 2025–26**.

The current value is 2.4 percentage points below the recorded peak, but 6.4 points above the first year. It does not show a sustained decline across the full period.

---

# What the trend supports

**Supported by these records:** Suzuki, Toyota, and Honda continue to account for nearly all recorded passenger-car sales; their combined recorded share remains very high.

**Not established by these records alone:** that the Big Three lost dominance in the complete Pakistani market, or why any change occurred.

The difference comes from the reporting frame and denominator, not from the arithmetic of CR3.

---

# A denominator sensitivity example

Hold Big Three recorded sales at 151,881 and hypothetically add sales outside the workbook’s 155,631 total:

| Hypothetical additional sales | Expanded denominator | Recalculated CR3 |
|---:|---:|---:|
| 0 | 155,631 | 97.6% |
| 10,000 | 165,631 | 91.7% |
| 25,000 | 180,631 | 84.1% |
| 50,000 | 205,631 | 73.9% |

These are scenarios, **not estimates of missing sales**. They show why a proportion depends on who is included in its denominator.

---

# A recorded electric-car example

![Separately reported Honri-Ve sales in the workbook](public/outputs/recorded_ev_sales.png)

The workbook contains a separate Honri-Ve sales row for 2024–25 and 2025–26: **186** and **343** units. These are 0.17% and 0.22% of the workbook’s recorded passenger-car totals.

An absent earlier row means “not separately recorded here,” not “no electric cars were sold.” The ratio is not a national EV market share.

---

# A defensible conclusion

The PAMA passenger-car workbook shows **continued, very high recorded concentration** among Suzuki, Toyota, and Honda. CR3 rose from 91.2% in 2007–08 to a 100% recorded peak, then stood at 97.6% in 2025–26.

The data do not show a sustained decline over the full period, and the workbook alone cannot establish the Big Three’s share of every new passenger car sold in Pakistan.

A broader market claim needs a denominator that covers the intended sellers and vehicles, such as documented registration or import records.

---

# Analysis workflow

**Question → population → source → row definition → validation → aggregation → denominator → result → limitation**

Each step changes what the final number means. Correct arithmetic cannot repair a source that does not represent the population named in the claim.

---

# Source and definitions

- Pakistan Automotive Manufacturers Association, [Monthly Production and Sales of Vehicles](https://pama.org.pk/monthly-production-sales-of-vehicles/)
- Fiscal year: July through June, using the workbook’s fiscal-year labels
- CR3: combined share of the three named manufacturers, calculated from recorded sales
- Prepared columns and known source limitations: [`data_dictionary.md`](data_dictionary.md)

The analysis is descriptive. It measures the records supplied by the workbook and does not infer causes.
